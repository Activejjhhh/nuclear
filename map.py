from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geographiclib.geodesic import Geodesic
import folium

# Initialize the geopy geocoder
geolocator = Nominatim(user_agent="geopy_example")

def get_coordinates(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return [location.latitude, location.longitude]
    else:
        print(f"Coordinates not found for {city_name}")
        return None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        start_city = request.form.get('start-city')
        end_city = request.form.get('end-city')


        start = get_coordinates(start_city)
        end = get_coordinates(end_city)

        # Create a new Folium map centered on the start location
        m = folium.Map(location=start, zoom_start=2)

     
        folium.Marker(start, popup=start_city).add_to(m)
        folium.Marker(end, popup=end_city).add_to(m)
        # Add circles for the start and end locations
        folium.Circle(end, radius=50000, color='blue', fill=True).add_to(m)


  
        num_points = 100
        geod = Geodesic.WGS84  
        g = geod.Inverse(start[0], start[1], end[0], end[1])

        points = [geod.Direct(g['lat1'], g['lon1'], g['azi1'], i * g['s12'] / num_points) for i in range(num_points+1)]

        # split path into segments that do not cross IDL
        segments = []
        segment = []
        for i in range(len(points) - 1):
            segment.append((points[i]['lat2'], points[i]['lon2']))
            if abs(points[i]['lon2'] - points[i+1]['lon2']) > 180:
                segments.append(segment)
                segment = []
        segment.append((points[-1]['lat2'], points[-1]['lon2']))
        segments.append(segment)

        for segment in segments:
            m.add_child(folium.PolyLine(locations=segment, color='red', dash_array='5, 5'))


        # Save the map to a file
        m.save(r'C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/static/map.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
