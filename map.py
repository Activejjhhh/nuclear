import folium
from geographiclib.geodesic import Geodesic

# Define the start and end locations
start = [51.5074, -0.1278]  # London
end = [39.9042, 116.4074]  # Beijing

# Create a new Folium map centered on the start location
m = folium.Map(location=start, zoom_start=2)

# Add markers for the start and end locations
folium.Marker(start).add_to(m)
folium.Marker(end).add_to(m)

# Calculate a series of intermediate points on the geodesic path
num_points = 100
geod = Geodesic.WGS84  # define the WGS84 ellipsoid
g = geod.Inverse(start[0], start[1], end[0], end[1])

line = geod.Line(g['lat1'], g['lon1'], g['azi1'])
points = [line.Position(i * g['s12'] / num_points) for i in range(num_points+1)]

# Add the geodesic path to the map
folium.PolyLine([(point['lat2'], point['lon2']) for point in points], color="red", weight=2.5, opacity=1).add_to(m)

# Display the map


m.save('map.html')

