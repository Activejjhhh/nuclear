from flask import Flask, render_template, request, url_for
from geopy.geocoders import Nominatim
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
import os
from nucleareffects.py import NukeEffects





app = Flask(__name__, template_folder='C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\templates', static_folder='C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\static')




@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    i = 0
    if request.method == 'POST':
        # Use geopy to get coordinates for two cities
        geolocator = Nominatim(user_agent="geoapiExercises")

        city1 = request.form.get('start-city')
        location1 = geolocator.geocode(city1)

        city2 = request.form.get('end-city')
        location2 = geolocator.geocode(city2)

        if location1 and location2:
            # Define the number of increments and calculate the increment size
            num_increments = 100
            lat_increment = (location2.latitude - location1.latitude) / num_increments
            lon_increment = (location2.longitude - location1.longitude) / num_increments

            # Generate the coordinates for each increment
            coordinates = []
            for i in range(num_increments + 1):
                coord = [location1.longitude + i * lon_increment, location1.latitude + i * lat_increment]
                time = (datetime(2023, 1, 1) + timedelta(days=i)).strftime("%Y-%m-%d")
                coordinates.append({"coordinates": coord, "time": time, "popup": f"Step {i}"})

            # Create a new map centered at the average of the points
            m = folium.Map(location=[0, 0], zoom_start=2)

            # Add a marker for the start location
            folium.Marker(
                location=[location1.latitude, location1.longitude],
                popup="Start Location",
                icon=folium.Icon(icon="cloud"),
            ).add_to(m)

            # Add a marker for the end location
            folium.Marker(
                location=[location2.latitude, location2.longitude],
                popup="End Location",
                icon=folium.Icon(color="red"),
            ).add_to(m)



            # Create a TimestampedGeoJson object and add it to the map
            tgj = TimestampedGeoJson(
                {"type": "FeatureCollection",
                "features": [
                    {"type": "Feature",
                     "geometry": {
                         "type": "LineString",
                         "coordinates": [coord["coordinates"] for coord in coordinates],
                     },
                     "properties": {
                         "times": [coord["time"] for coord in coordinates] * 2,  # Repeat times for start and end of line
                         "style": {"color": "green", "weight": 5},  # Line style
                     }
                    }
                ]},
                period="P1D",
                auto_play=False,
                loop=False,
                max_speed=1,
                loop_button=True,
                date_options='YYYY/MM/DD',
                time_slider_drag_update=True
            )
            tgj.add_to(m)

            # Add a red geodesic line to the map
            folium.PolyLine(
                locations=[[location1.latitude, location1.longitude], [location2.latitude, location2.longitude]],
                color="red"
            ).add_to(m)

            # Save it to a file
            # Save it to a file
            m.save('C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\static\\map.html')



        else:
            message = "Could not find one or both of the cities."

    return render_template('index.html', message=message, i=i)

if __name__ == '__main__':
    app.run(debug=True)
