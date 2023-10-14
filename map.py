from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geographiclib.geodesic import Geodesic
import folium


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

        # get coordinates for the start and end cities
        start = get_coordinates(start_city)
        end = get_coordinates(end_city)

   
        m = folium.Map(location=start, zoom_start=2)

   
        folium.Marker(start, popup=start_city).add_to(m)
        folium.Marker(end, popup=end_city).add_to(m)

        
        num_points = 100
        geod = Geodesic.WGS84  # define the WGS84 ellipsoid
        g = geod.Inverse(start[0], start[1], end[0], end[1])

        points = [geod.Direct(g['lat1'], g['lon1'], g['azi1'], i * g['s12'] / num_points) for i in range(num_points+1)]

        # dd the geodesic path to the map
        folium.PolyLine([(point['lat2'], point['lon2']) for point in points], color="red", weight=2.5, opacity=1).add_to(m)

        #save map to file
        m.save(r'C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/static/map.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

