import math

class ICBM:
    def __init__(self, name, payload, max_range, max_altitude, fuel_type, mirvs, payload_type, cross_section, weight_missile, weight_fuel, max_speed, origin, year, blast_height, stage1, stage2, stage3):
        self.name = name
        self.payload = payload
        self.max_range = max_range
        self.max_altitude = max_altitude
        self.fuel_type = fuel_type
        self.mirvs = mirvs
        self.payload_type = payload_type
        self.cross_section = cross_section
        self.weight_missile = weight_missile
        self.weight_fuel = weight_fuel
        self.max_speed = max_speed
        self.origin = origin
        self.year = year
        self.blast_height = blast_height
        self.stage1 = stage1
        self.stage2 = stage2
        self.stage3 = stage3
        self.air_density = 1.225  # kg/m^3 at sea level
        self.drag_coefficient = 0.47  # for a sphere

    def calculate_drag_force(self, velocity, altitude):
        # Adjust air density based on altitude
        adjusted_air_density = self.air_density * math.exp(-altitude / 8000)  # Scale height of Earth's atmosphere is approximately 8000m
        return 0.5 * self.drag_coefficient * adjusted_air_density * self.cross_section * velocity**2

    def calculate_acceleration(self, thrust, drag_force):
        net_force = thrust - drag_force
        return net_force / self.weight_missile

    def calculate_flight_time_with_resistance(self):
        time = 0
        velocity = 0
        distance = 0
        altitude = 0
        total_distance = float(self.max_range.replace(",", "").split(" ")[0])  # remove commas before converting to float

        while distance < total_distance:
            # Adjust thrust based on the stage of the journey
            if distance < total_distance / 3:
                thrust = float(self.stage1)
            elif distance < 2 * total_distance / 3:
                thrust = float(self.stage2)
            else:
                thrust = float(self.stage3)

            drag_force = self.calculate_drag_force(velocity, altitude)
            acceleration = self.calculate_acceleration(thrust, drag_force)
            initial_velocity = velocity
            velocity += acceleration

            if velocity > self.max_speed:
                velocity = self.max_speed

            # Calculate distance traveled during this time step
            distance += initial_velocity + 0.5 * acceleration

            # Update time and altitude
            time += 1
            altitude += velocity

        return time

    def calculate_flight_time(self, speed, lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Differences
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in kilometers
        distance = R * c

        # Time = Distance/Speed
        time = distance / speed

        return time

minuteman_III = ICBM(
    name="Minuteman III",
    payload=300,
    max_range="14,000 km",
    max_altitude="1,126 km",
    fuel_type="Solid",
    mirvs="Yes",
    payload_type="Nuclear",
    cross_section=1.68,
    weight_missile=36000,
    weight_fuel=0,
    max_speed=24000,
    origin="USA",
    year=1961,
    blast_height=None,
    stage1 = "99790",
    stage2= "27487",
    stage3= "15422",
)
launch_lat = float(input("Enter the latitude of the launch location: "))
launch_lon = float(input("Enter the longitude of the launch location: "))
target_lat = float(input("Enter the latitude of the target location: "))
target_lon = float(input("Enter the longitude of the target location: "))
time = minuteman_III.calculate_flight_time(minuteman_III.max_speed, launch_lat, launch_lon, target_lat, target_lon)

print(f"The flight time of the missile is approximately {time} hours.")
