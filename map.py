import folium
from geopy.geocoders import Nominatim
from geographiclib.geodesic import Geodesic

# initialize the geopy geocoder
geolocator = Nominatim(user_agent="geopy_example")

# function to get coordinates from a city name
def get_coordinates(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return [location.latitude, location.longitude]
    else:
        print(f"Coordinates not found for {city_name}")
        return None

# get start and end city names from the user
start_city = input("Enter the start city: ")
end_city = input("Enter the end city: ")

# get coordinates for the start and end cities
start = get_coordinates(start_city)
end = get_coordinates(end_city)

# create a new Folium map centered on the start location
m = folium.Map(location=start, zoom_start=2)

# add markers for the start and end locations
folium.Marker(start, popup=start_city).add_to(m)
folium.Marker(end, popup=end_city).add_to(m)

# calculate a series of intermediate points on the geodesic path
num_points = 100
geod = Geodesic.WGS84  
g = geod.Inverse(start[0], start[1], end[0], end[1])

points = [geod.Direct(g['lat1'], g['lon1'], g['azi1'], i * g['s12'] / num_points) for i in range(num_points+1)]

# Add the geodesic path to the map
folium.PolyLine([(point['lat2'], point['lon2']) for point in points], color="red", weight=2.5, opacity=1).add_to(m)

# Display the map
m.save('maps.html')
