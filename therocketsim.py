
import math
import pygame
from pygame.locals import *
from geopy.geocoders import Nominatim

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 850, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Constants
RADIUS_EARTH = 6371e3  # meters
GRAVITY = 9.81  # m/s^2
STANDARD_AIR_DENSITY = 1.225  # kg/m^3 at sea level and 15°C
DRAG_COEFFICIENT = 0.47  # drag coefficient for a sphere, adjust based on missile type

launch_lat = None
launch_lon = None
missile_lat = None
missile_lon = None
missile_altitude = None
v_lat = 0 
v_lon = 0  
v_lat = 0
v_lon = 0
v = 0      
angle = None 
g = 0


# Font
font = pygame.font.SysFont(None, 24)

# Geocoder
geolocator = Nominatim(user_agent="rocket-simulation")

# Input boxes
launch_box = pygame.Rect(10, 10, 200, 30)
strike_box = pygame.Rect(10, 50, 200, 30)
launch_text = ""
strike_text = ""

# Missile variables
v_lat = None
v_lon = None

# Simulation variables
t = 0
dt = 0.001  # Larger dt for slower motion

# Previous position variables
prev_position_x = None
prev_position_y = None

# Missile cross-sectional area (assumed constant for this example)
cross_sectional_area = math.pi * (1.85 / 2) ** 2  # m^2, based on Minuteman III diameter

# Air density calculation
def air_density(altitude):
    temperature = 288.15 - 0.0065 * altitude  # Kelvin, linear approximation
    pressure = 101325 * (1 - 0.0065 * altitude / temperature) ** 5.255  # Pa
    density = pressure / (287.05 * temperature)  # kg/m^3, using ideal gas law
    return density

# Calculate the drag force
def drag_force(air_density, velocity, drag_coefficient, cross_sectional_area):
    return 0.5 * air_density * velocity ** 2 * drag_coefficient * cross_sectional_area

# Update the missile's acceleration
def update_acceleration(v_lat, v_lon, drag_force, angle):
    g_lat = -GRAVITY * math.sin(angle)
    g_lon = -GRAVITY * math.cos(angle)
    a_lat = g_lat - drag_force * math.sin(angle)
    a_lon = g_lon - drag_force * math.cos(angle)
    return a_lat, a_lon

# Update the missile's velocity and position
def update_velocity_and_position(v_lat, v_lon, a_lat, a_lon, dt):
    v_lat_new = v_lat + a_lat * dt
    v_lon_new = v_lon + a_lon * dt
    missile_lat_new = missile_lat + v_lat * dt
    missile_lon_new = missile_lon + v_lon * dt
    return v_lat_new, v_lon_new, missile_lat_new, missile_lon_new


class Warhead:
    def __init__(self, name, length, diameter, stage1_mass, stage2_mass, stage3_mass, yield_, range_):
        self.name = name
        self.length = length
        self.diameter = diameter
        self.stage1_mass = stage1_mass
        self.stage2_mass = stage2_mass       
        self.stage3_mass = stage3_mass
        self.yield_ = yield_
        self.range_ = range_



    def get_name(self):
        return self.name

    def get_length(self):
        return self.length

    def get_diameter(self):
        return self.diameter

    def get_stage1_mass(self):
        return self.stage1_mass

    def get_stage2_mass(self):
        return self.stage2_mass

    def get_stage3_mass(self):
        return self.stage3_mass

    def get_payload(self):
        return self.payload

    def get_range(self):
        return self.range_

topol_m = Warhead("Topol-M", 22.7, 1.9, 18000, 14000, 9000, 800, 11000)
minuteman_iii = Warhead("Minuteman III", 18.2, 1.85, 12000, 10000, 8000, 475, 13000)


def get_coordinates_from_city_name(city_name):
    location = geolocator.geocode(city_name)
    if location:
        # Add the print statement here
        print(f"{city_name} coordinates: {location.latitude}, {location.longitude}")
        return math.radians(location.latitude), math.radians(location.longitude)
    else:
        # Add the print statement here
        print(f"{city_name} not found")
        return None, None

    location = geolocator.geocode(city_name)
    if location:
        return math.radians(location.latitude), math.radians(location.longitude)
    else:
        return None, None

def launch_missile():
    global launch_lat, launch_lon, missile_lat, missile_lon, missile_altitude, prev_position_x, prev_position_y, angle, v_lat, v_lon, g_lat, g_lon

    print("launch_missile called")

    launch_lat, launch_lon = get_coordinates_from_city_name(launch_text)
    strike_lat, strike_lon = get_coordinates_from_city_name(strike_text)

    if launch_lat is not None and launch_lon is not None and strike_lat is not None and strike_lon is not None:
        delta_lat = strike_lat - launch_lat
        delta_lon = strike_lon - launch_lon
        a = math.sin(delta_lat / 2) ** 2 + math.cos(launch_lat) * math.cos(strike_lat) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = RADIUS_EARTH * c

        speed = 1000  # m/s
        time = distance / speed

        lat_mean = (launch_lat + strike_lat) / 2
        lon_mean = (launch_lon + strike_lon) / 2
        v_lat = (strike_lat - launch_lat) / time
        v_lon = (strike_lon - launch_lon) / time
        v = math.sqrt(v_lat ** 2 + v_lon ** 2)

        angle = math.atan2(v_lat, v_lon)

        # Calculate the direction and components of gravity
        g_angle = math.atan2(-v_lat, -v_lon)
        g_lat = -GRAVITY * math.sin(g_angle)
        g_lon = -GRAVITY * math.cos(g_angle)

        missile_lat = launch_lat
        missile_lon = launch_lon
        missile_altitude = 10000  # meters

        t = 0
        prev_position_x = None
        prev_position_y = None


def draw_missile():
    global prev_position_x, prev_position_y

    # Calculate the position on the screen
    delta_lat = missile_lat - launch_lat
    delta_lon = missile_lon - launch_lon

    # Convert latitude and longitude differences to meters
    delta_x = RADIUS_EARTH * delta_lon * math.cos(launch_lat)
    delta_y = RADIUS_EARTH * delta_lat

    # Calculate the scale based on the screen size and the maximum distance
    scale = min(WIDTH, HEIGHT) / (2 * math.pi * RADIUS_EARTH)

    # Calculate the position on the screen
    position_x = int(WIDTH // 2 + delta_x * scale)
    position_y = int(HEIGHT // 2 - delta_y * scale)  # Subtract from HEIGHT to flip the y-axis

    # Draw the missile with a check to make sure position_x and position_y are numbers
    if isinstance(position_x, (int, float)) and isinstance(position_y, (int, float)):
        pygame.draw.circle(screen, RED, (position_x, position_y), 5)
    else:
        print(f"position_x: {position_x}, position_y: {position_y}")

    # Draw the trajectory line
    if prev_position_x is not None and prev_position_y is not None:
        pygame.draw.line(screen, RED, (prev_position_x, prev_position_y), (position_x, position_y), 2)

    # Update the previous position
    prev_position_x = position_x
    prev_position_y = position_y


# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if launch_text and strike_text:
                    launch_missile()
            elif event.key == pygame.K_BACKSPACE:
                if launch_box.collidepoint(pygame.mouse.get_pos()):
                    launch_text = launch_text[:-1]
                elif strike_box.collidepoint(pygame.mouse.get_pos()):
                    strike_text = strike_text[:-1]
            else:
                if launch_box.collidepoint(pygame.mouse.get_pos()):
                    launch_text += event.unicode
                elif strike_box.collidepoint(pygame.mouse.get_pos()):
                    strike_text += event.unicode

    screen.fill(WHITE)

    # Draw the input boxes, Earth, and missile trajectory
    pygame.draw.rect(screen, BLUE, launch_box, 2)
    pygame.draw.rect(screen, BLUE, strike_box, 2)
    launch_surface = font.render("Launch City:", True, BLUE)
    strike_surface = font.render("Strike City:", True, BLUE)
    launch_text_surface = font.render(launch_text, True, BLUE)
    strike_text_surface = font.render(strike_text, True, BLUE)
    screen.blit(launch_surface, (launch_box.x + 5, launch_box.y - 20))
    screen.blit(strike_surface, (strike_box.x + 5, strike_box.y - 20))
    screen.blit(launch_text_surface, (launch_box.x + 5, launch_box.y + 5))
    screen.blit(strike_text_surface, (strike_box.x + 5, strike_box.y + 5))
    pygame.draw.circle(screen, BLUE, (WIDTH // 2, HEIGHT // 2), HEIGHT // 2, 2)

    if missile_lat is not None and missile_lon is not None and missile_altitude is not None:
        draw_missile()

        # Calculate air density at the current altitude
        current_air_density = air_density(missile_altitude)

        # Calculate drag force
        drag = drag_force(current_air_density, v, DRAG_COEFFICIENT, cross_sectional_area)

        # Update acceleration
        a_lat, a_lon = update_acceleration(v_lat, v_lon, drag, angle)

        # Update velocity and position
        v_lat, v_lon, missile_lat, missile_lon = update_velocity_and_position(v_lat, v_lon, a_lat, a_lon, dt)

        # Add the print statements here
        print(f"missile_lat: {missile_lat}, missile_lon: {missile_lon}")
        print(f"v_lat: {v_lat}, v_lon: {v_lon}")

        # Update the simulation time
        t += dt

    pygame.display.flip()
    clock.tick(60)
