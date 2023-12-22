from flask import Flask, render_template, request, url_for
from geopy.geocoders import Nominatim
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
import os
from datetime import datetime
from icbm import ICBM, missiles
import matplotlib.pyplot as plt
import copy
from nucleareffects import NukeEffects

from fallout import Fallout
import numpy as np
app = Flask(__name__, template_folder='C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\templates', static_folder='C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\static')

geolocator = Nominatim(user_agent="thesimltor")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        message = None
        i = 0

        speeds = []
        default_speeds = []
        default_coordinates = []
        selected_missile = None
        coordinates = []

        # Use geopy to get coordinates for two cities
        geolocator = Nominatim(user_agent="geoapiExercise")

        city1 = request.form.get('start-city')
        location1 = geolocator.geocode(city1)

        city2 = request.form.get('end-city')
        location2 = geolocator.geocode(city2)

        speed = request.form.get('speed')

        # Create a new map centered at the average of the points
        m = folium.Map(location=[0, 0], zoom_start=2)


        missile_number = request.form.get('missile')
        new_payload = request.form.get('new-payload')  # Get the new payload from the form
        print(new_payload)

        if missile_number is not None:
            missile_number = int(missile_number)
            selected_missile = copy.deepcopy(missiles[missile_number - 1])  # Create a copy of the selected missile
        elif new_payload is not None:
        	missile_number = int(0)
        	selected_missile = copy.deepcopy(missiles[0])
        	selected_missile.payload = new_payload
        	print(selected_missile.payload)


        if selected_missile:
            time = selected_missile.calculate_flight_time(selected_missile.max_speed, location1.latitude, location1.longitude, location2.latitude, location2.longitude)
            time_seconds = time * 3600  # Convert hours to seconds # Convert hours to seconds
            print(f"The flight time of the missile is approximately {time_seconds} seconds.")
            
            # Calculate final_time with air resistance
            final_time = time_seconds
            
            # Now pass final_time as an argument
            speeds, velocity, time = selected_missile.calculate_speeds_with_resistance(final_time)

            if location1 and location2:
                # Calculate the flight time
                flight_time = selected_missile.calculate_flight_time(selected_missile.max_speed, location1.latitude, location1.longitude, location2.latitude, location2.longitude)

                # Convert flight time from hours to seconds
                flight_time_seconds = int(flight_time * 3600)

                # Define the number of increments based on the flight time
                num_increments = flight_time_seconds
                print(num_increments)
                lat_increment = (location2.latitude - location1.latitude) / num_increments
                print(num_increments)
                lon_increment = (location2.longitude - location1.longitude) / num_increments



                counter1 = 0  # Initialize the counter
                for i in range(num_increments + 1):
                    coord = [location1.longitude + i * lon_increment, location1.latitude + i * lat_increment]
                    timestamp = (datetime.now() + timedelta(seconds=i)).isoformat()
                    speed = speeds[i][1] if i < len(speeds) else None
                    coordinates.append({"coordinates": coord, "time": timestamp, "popup": f"Step {i}", "speed": speed, "counter1": counter1})

                    print(f"At time {i} seconds, the speed is {speed} m/s, timestamp is {timestamp}, counter1 is {counter1}, and coordinates are {counter1}. ")

                    counter1 += 1  # Increment the counter

            else:
                message = "Could not find the selected missile."


        else:
            message = "No missile selected."



        height = request.form.get('height')
        

        # Check if the 'surface' checkbox is ticked
        is_surface = 'surface' in request.form
        print(f"Is surface: {is_surface}")

        # Set 'is_airburst' to the opposite of 'is_surface'
        is_airburst = not is_surface
        print(f"Is airburst: {is_airburst}")



        is_3000psi_ticked = '3000psi' in request.form


        # Print out whether the checkbox is ticked
        if is_3000psi_ticked:
            print("The '3000psi' checkbox is ticked.")
            
            # Assuming you have the yield of the explosion and the height of burst
            yield_ = 300
            hob = height if height is not None else 0
            
            # Create an instance of NukeEffects
            nukeEffects = NukeEffects()
            
            # Calculate the distance affected by 3000psi
            distance = nukeEffects.psi_distance(selected_missile.payload, 1, is_airburst)  

            
            # Convert the distance to meters
            radius = distance * 1609.34 # since 1 mile is approximately 1609.34 meters
            print(f"The radius affected by 3000psi is {radius} meters.")
            
            # Assuming you have the latitude and longitude of the explosion
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion


            folium.Circle(
                location=[latitude, longitude],
                radius=radius,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="green",
                fill=False,  # gets overridden by fill_color
                popup="{} meters".format(radius),
                tooltip="I am in meters",
            ).add_to(m)
            
            
        else:
            print("The '3000psi' checkbox is not ticked.")

        is_100rem_ticked = '100rem' in request.form

        if is_100rem_ticked:
            print("The '100rem' checkbox is ticked.")
            
            # Create an instance of NukeEffects
            nukeEffects = NukeEffects()
            
            # Calculate the distance affected by 100 rem
            distance = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 100, False) # assuming it's an airburst
            
            # Convert the distance to meters
            radius = distance * 1609.34 # since 1 mile is approximately 1609.34 meters
            print(f"The radius affected by 100 rem is {radius} meters.")
            
            # Assuming you have the latitude and longitude of the explosion
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="green",
                fill=False,  # gets overridden by fill_color
                popup="{} meters".format(radius),
                tooltip="I am in meters",
            ).add_to(m)
        else:
            print("The '100rem' checkbox is not ticked.")







        

        def generate_oval(focus, major_axis, minor_axis, angle):
            """
            Generate points for an oval (teardrop shape).

            Parameters:
            - focus: The [latitude, longitude] of one of the foci of the oval.
            - major_axis: this is given by the code max_downwind_distance_meters
            - minor_axis: this is given by the code max_width_meters
            - angle: This is given by the code wind_direction

            Returns:
            - points: A list of [latitude, longitude] points that make up the oval.
            """
            # Convert degrees to radians
            angle = np.deg2rad(angle)

            # Calculate the coordinates of the center of the oval
            center = [focus[0] + major_axis/2 * np.cos(angle), focus[1] + major_axis/2 * np.sin(angle)]

            # Generate t values
            t = np.linspace(0, 2*np.pi, 100)

            # Generate the oval points
            x = center[0] + major_axis/2 * np.sin(t) * np.cos(angle) - minor_axis/2 * np.cos(t) * np.sin(angle)
            y = center[1] + major_axis/2 * np.sin(t) * np.sin(angle) + minor_axis/2 * np.cos(t) * np.cos(angle)

            # Combine x and y into a list of points
            points = list(zip(x, y))

            return points



        is_fallouts_ticked = 'fallouts' in request.form


        print(request.form)
        if is_fallouts_ticked:
        	print("The 'fallout' checkbox is ticked.")


        	fo = Fallout()

        	wind_speed, wind_direction = fo.get_wind_data(location2.latitude, location2.longitude)

        	fission_fraction = 0.9 

        	rad_doses= [1] 


        	# Calculate the fallout parameters
        	fallout_params_list = fo.SFSS_fallout(selected_missile.payload, rad_doses, fission_fraction, wind_speed)

        	# Get the first (and only) item in the list
        	fallout_params = fallout_params_list[0]

        	# Now you can access 'downwind_cloud_distance' and 'max_cloud_width'
        	max_downwind_distance_meters = fallout_params['downwind_cloud_distance'] * 0.0160934 
        	max_width_meters = fallout_params['max_cloud_width']  * 0.0160934


        	print(f"max_downwind_distance_meters: {max_downwind_distance_meters}")
        	print(f"max_width_meters: {max_width_meters}")
        	print(f"location2.latitude: {location2.latitude}")
        	print(f"location2.longitude: {location2.longitude}")
        	print(f"wind_direction: {wind_direction}")

        	points = generate_oval(focus=[location2.latitude, location2.longitude], major_axis=max_downwind_distance_meters, minor_axis=max_width_meters, angle=wind_direction)

        	# Add the oval to the map
        	folium.vector_layers.Polygon(locations=points, color="yellow", fill=True).add_to(m)

        else:
        	print("not ticked")
     



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
                     "speeds": [coord["speed"] for coord in coordinates] * 2,  # Add speeds for each time
                     "style": {"color": "green", "weight": 5},  # Line style
                 }
                }
            ]},
            period="PT1S", 
            auto_play=True,
            loop=False,
            max_speed=5,
            loop_button=True,
            date_options='YYYY-MM-DDTHH:mm:ss',
            time_slider_drag_update=True
        )
        tgj.add_to(m)

        # Add a red geodesic line to the map
        folium.PolyLine(
            locations=[[location1.latitude, location1.longitude], [location2.latitude, location2.longitude]],
            color="red"
        ).add_to(m)

        m.save('C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\static\\map.html')

    else:
        message = "Could not find one or both of the cities."


    if 'speeds' in locals() and speeds:  # Check if speeds is defined and has data
            speeds_to_pass = speeds
    else:
            default_speeds = []  # Assign a value to default_speeds before referencing it
            speeds_to_pass = default_speeds


    if 'selected_missile' not in locals() or selected_missile is None:  # Check if selected_missile is defined and has data
                selected_missile = None


    if 'coordinates' not in locals() or not coordinates:  # Check if coordinates is defined and has data
                coordinates = [] 


    return render_template('index.html', message=None, i=0, speeds=speeds_to_pass, selected_missile=selected_missile, coordinates=coordinates)

if __name__ == '__main__':
    app.run(debug=True)



'''
        # Check if the checkbox for '3000psi' is ticked
        is_3000psi_ticked = '3000psi' in request.form
        is_200psi_ticked = '200psi' in request.form
        is_20psi_ticked = '20psi' in request.form
        is_5psi_ticked = '5psi' in request.form
        is_1psi_ticked = '1psi' in request.form

        is_5000rem_ticked = '3000psi' in request.form
        is_1000rem_ticked = '1000psi' in request.form
        is_600psi_ticked = '600psi' in request.form
        is_500psi_ticked = '500psi' in request.form
        is_100psi_ticked = '3000psi' in request.form

        is_3000psi_ticked = '3000psi' in request.form
        is_3000psi_ticked = '3000psi' in request.form
        is_3000psi_ticked = '3000psi' in request.form
        is_3000psi_ticked = '3000psi' in request.form
        is_3000psi_ticked = '3000psi' in request.form

'''
