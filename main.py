from flask import Flask, render_template, request, url_for, session, redirect, abort
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
app.secret_key = 'b7a23qsasd45454d2b71c4a5c7c121272' #random key that i need to make for some reason


geolocator = Nominatim(user_agent="thesimltor")


@app.route('/', methods=['GET', 'POST'])


def home():
    print(f"Request method: {request.method}")
    injured = 0
    killed = 0
    depth=0
    lip_radius=0
    inside_radius=0
    cloud_altitude=0
    cloud_head_radius=0
    cloud_head_height=0
    location1 = None
    location2 = None
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

        if location1 is None or location2 is None:
                abort(400, description="One or both of the locations could not be found. Please make sure you enter both locations correctly and try again.")



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

        if selected_missile is None and (not new_payload or new_payload.strip() == ''):
                abort(400, description="No missile selected and new payload is blank. Please select a missile or provide a payload.")


        height = request.form.get('height')
        

        # Check if the 'surface' checkbox is ticked
        is_surface = 'surface' in request.form
        print(f"Is surface: {is_surface}")

        # Set 'is_airburst' to the opposite of 'is_surface'
        is_airburst = not is_surface
        print(f"Is airburst: {is_airburst}")


        # Calculate the distance affected by 1psi
        hob = height if height is not None else 0

        nukeEffects = NukeEffects()
        distance1psi = nukeEffects.psi_distance(selected_missile.payload, 1, is_airburst)  
        distance5psi = nukeEffects.psi_distance(selected_missile.payload, 5, is_airburst) 
        distance20psi = nukeEffects.psi_distance(selected_missile.payload, 20, is_airburst) 
        distance200psi = nukeEffects.psi_distance(selected_missile.payload, 200, is_airburst) 
        distance3000psi = nukeEffects.psi_distance(selected_missile.payload, 3000, is_airburst) 

        # Convert the distance to meters
        radius1psi = distance1psi * 1609.34 # since 1 mile is approximately 1609.34 meters
        radius5psi = distance5psi * 1609.34 
        radius20psi = distance20psi * 1609.34 
        radius200psi = distance200psi * 1609.34 
        radius3000psi = distance3000psi * 1609.34 

        # Check if the '1psi' checkbox is ticked
        is_1psi_ticked = '1psi' in request.form
        is_5psi_ticked = '5psi' in request.form
        is_20psi_ticked = '20psi' in request.form
        is_200psi_ticked = '200psi' in request.form
        is_3000psi_ticked = '3000psi' in request.form

        if is_1psi_ticked:
            print("The '1psi' checkbox is ticked.")
            
            # Assuming you have the latitude and longitude of the explosion
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius1psi,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="#FFC0C0",
                fill=False,  # gets overridden by fill_color
                popup="{} meters".format(radius1psi),
                tooltip="1 PSI ",
            ).add_to(m)
        else:
            print("The '1psi' checkbox is not ticked.")


        if is_5psi_ticked:
            print("The '5psi' checkbox is ticked.")

            latitude = location2.latitude 
            longitude = location2.longitude 

            folium.Circle(
                location=[latitude, longitude],
                radius=radius5psi,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="#FF8080",
                fill=False,  
                popup="{} meters".format(radius5psi),
                tooltip="5 PSI ",
            ).add_to(m)
        else:
            print("The '5psi' checkbox is not ticked.")

        if is_20psi_ticked:
            print("The '20psi' checkbox is ticked.")

            latitude = location2.latitude 
            longitude = location2.longitude 

            folium.Circle(
                location=[latitude, longitude],
                radius=radius20psi,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="#FF0000",
                fill=False,  
                popup="{} meters".format(radius20psi),
                tooltip="20 PSI ",
            ).add_to(m)
        else:
            print("The '20psi' checkbox is not ticked.")

        if is_200psi_ticked:
            print("The '200psi' checkbox is ticked.")

            latitude = location2.latitude 
            longitude = location2.longitude 

            folium.Circle(
                location=[latitude, longitude],
                radius=radius200psi,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="#B20000",
                fill=False,  
                popup="{} meters".format(radius200psi),
                tooltip="200 PSI ",
            ).add_to(m)
        else:
            print("The '200psi' checkbox is not ticked.")

        if is_3000psi_ticked:
            print("The '3000psi' checkbox is ticked.")

            latitude = location2.latitude 
            longitude = location2.longitude 

            folium.Circle(
                location=[latitude, longitude],
                radius=radius3000psi,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="#660000",
                fill=False,  
                popup="{} meters".format(radius3000psi),
                tooltip="3000 PSI ",
            ).add_to(m)
        else:
            print("The '3000psi' checkbox is not ticked.")


        is_100rem_ticked = '100rem' in request.form
        is_500rem_ticked = '500rem' in request.form
        is_600rem_ticked = '600rem' in request.form
        is_1000rem_ticked = '1000rem' in request.form
        is_5000rem_ticked = '5000rem' in request.form

        distance100rem = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 100, is_airburst)
        distance500rem = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 500, is_airburst)
        distance600rem = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 600, is_airburst)
        distance1000rem = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 1000, is_airburst)
        distance5000rem = nukeEffects.initial_nuclear_radiation_distance(selected_missile.payload, 5000, is_airburst)

        # Convert the distance to meters
        radius100rem = distance100rem * 1609.34 # since 1 mile is approximately 1609.34 meters
        radius500rem = distance500rem * 1609.34 
        radius600rem = distance600rem * 1609.34 
        radius1000rem = distance1000rem * 1609.34 
        radius5000rem = distance5000rem * 1609.34 


        if is_100rem_ticked:
            print("The '100rem' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius100rem,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFFFE0",
                fill=False,
                popup="{} meters".format(radius100rem),
                tooltip="100 REM ",
            ).add_to(m)
        else:
            print("The '100rem' checkbox is not ticked.")

        if is_500rem_ticked:
            print("The '500rem' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius500rem,
                color="#FFFACD",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFFACD",
                fill=False,
                popup="{} meters".format(radius500rem),
                tooltip="500REM",
            ).add_to(m)
        else:
            print("The '500rem' checkbox is not ticked.")

        if is_600rem_ticked:
            print("The '600rem' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius600rem,
                color="#F0E68C",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#F0E68C",
                fill=False,
                popup="{} meters".format(radius600rem),
                tooltip="600REM",
            ).add_to(m)
        else:
            print("The '600rem' checkbox is not ticked.")

        if is_1000rem_ticked:
            print("The '1000rem' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius1000rem,
                color="#FFD700",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFD700",
                fill=False,
                popup="{} meters".format(radius1000rem),
                tooltip="1000REM",
            ).add_to(m)
        else:
            print("The '1000rem' checkbox is not ticked.")

        if is_5000rem_ticked:
            print("The '5000rem' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius5000rem,
                color="#FFFF00",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFFF00",
                fill=False,
                popup="{} meters".format(radius5000rem),
                tooltip="5000REM",
            ).add_to(m)
        else:
            print("The '5000rem' checkbox is not ticked.")


        is_1st_degree_ticked = 'firstDegreeBurns50' in request.form
        is_2nd_degree_ticked = 'secondDegreeBurns50' in request.form
        is_3rd_degree_ticked = 'thirdDegreeBurns50' in request.form
        is_3rd100_degree_ticked = 'thirdDegreeBurns100' in request.form
        is_noburn_ticked = 'noBurn100' in request.form
     

        distance_no_harm = nukeEffects.thermal_distance(selected_missile.payload, "_noharm-100", is_airburst)
        distance_1st_degree = nukeEffects.thermal_distance(selected_missile.payload, "_1st-50", is_airburst)
        distance_2nd_degree = nukeEffects.thermal_distance(selected_missile.payload, "_2nd-50", is_airburst)
        distance_3rd_degree = nukeEffects.thermal_distance(selected_missile.payload, "_3rd-50", is_airburst)
        distance_3rd100_degree = nukeEffects.thermal_distance(selected_missile.payload, "_3rd-100", is_airburst)


        radius1stdegree = distance_1st_degree * 1609.34
        radius2nddegree = distance_2nd_degree * 1609.34
        radius3rddegree = distance_3rd_degree * 1609.34
        radius3rd100degree = distance_3rd100_degree * 1609.34
        radius_no_harm = distance_no_harm * 1609.34

        if is_noburn_ticked:
            print("The 'no harm' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius_no_harm,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFDAB9",
                fill=False,
                popup="{} meters".format(radius_no_harm),
                tooltip=" No harm ",
            ).add_to(m)
        else:
            print("The 'no harm' checkbox is not ticked.")


        if is_1st_degree_ticked:
            print("The 'first degree' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius1stdegree,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FFA07A",
                fill=False,
                popup="{} meters".format(radius1stdegree),
                tooltip=" First degree ",
            ).add_to(m)
        else:
            print("The 'radius1stdegree' checkbox is not ticked.")

        if is_2nd_degree_ticked:
            print("The 'second degree' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius2nddegree,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#F4A460",
                fill=False,
                popup="{} meters".format(radius2nddegree),
                tooltip=" Second degree ",
            ).add_to(m)
        else:
            print("The 'second degree' checkbox is not ticked.")



        if is_3rd_degree_ticked:
            print("The 'third degree' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius3rddegree,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FF8C00",
                fill=False,
                popup="{} meters".format(radius3rddegree),
                tooltip=" Third degree ",
            ).add_to(m)
        else:
            print("The 'third degree' checkbox is not ticked.")


        if is_3rd100_degree_ticked:
            print("The '100% third degree' checkbox is ticked.")
            
            latitude = location2.latitude # latitude of the explosion
            longitude = location2.longitude # longitude of the explosion

            folium.Circle(
                location=[latitude, longitude],
                radius=radius3rd100degree,
                color="black",
                weight=1,
                fill_opacity=0.1,
                opacity=1,
                fill_color="#FF4500",
                fill=False,
                popup="{} meters".format(radius3rd100degree),
                tooltip=" 100% Third degree ",
            ).add_to(m)
        else:
            print("The '100% third degree' checkbox is not ticked.")




#FFD700


        def calculate_casualties(population_density, radius20psi, radius5psi, radius1stdegree): #needs fine tuning
            # Calculate the area for each radius
            area_20psi = 3.14159 * (radius20psi ** 2)
            area_3psi = 3.14159 * (radius5psi ** 2)
            area_1st_degree_burns = 3.14159 * (radius1stdegree ** 2)

            # Calculate the number of people in each area
            people_20psi = population_density * area_20psi
            people_3psi = population_density * (area_3psi - area_20psi)
            people_1st_degree_burns = population_density * (area_1st_degree_burns - area_3psi)

            # Calculate casualties
            killed = people_20psi
            injured = people_3psi + 0.5 * people_1st_degree_burns

            return killed, injured

        # Example usage:
        killed, injured = calculate_casualties(5000, radius20psi, radius5psi, radius1stdegree)
        print(f"Killed: {killed}, Injured: {injured}")


        craterDimensions = nukeEffects.crater(selected_missile.payload, False) # soil or not soil
        depth = int(craterDimensions[2] * 1000) 
        lip_radius = int(craterDimensions[0] * 1000)
        inside_radius = int(craterDimensions[1] * 1000) 

        cloud_altitude = int(nukeEffects.cloud_final_height(selected_missile.payload))
        cloud_head_radius = int(nukeEffects.cloud_final_horizontal_semiaxis(selected_missile.payload))
        cloud_head_height = int(nukeEffects.cloud_final_vertical_semiaxis(selected_missile.payload))



        def generate_oval(focus, major_axis, minor_axis, angle):
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

        	# Define the list of radiation doses
        	rad_doses = [1, 10, 100, 1000]

        	# Define a dictionary to map radiation doses to colors
        	colors = {1: "yellow", 10: "orange", 100: "red", 1000: "purple"}

        	# Iterate over the list of radiation doses
        	for rad_dose in rad_doses:
        	    # Calculate the fallout parameters
        	    fallout_params_list = fo.SFSS_fallout(selected_missile.payload, [rad_dose], fission_fraction, wind_speed)

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

        	    # Add the oval to the map with the color corresponding to the radiation dose
        	    folium.vector_layers.Polygon(locations=points, color=colors[rad_dose], fill=True).add_to(m)

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
            loop=True,
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



    return render_template('index.html', i=0, speeds=speeds_to_pass, selected_missile=selected_missile, coordinates=coordinates, injured=injured, killed=killed, depth=depth ,
     lip_radius=lip_radius, inside_radius=inside_radius,  cloud_altitude=cloud_altitude, cloud_head_radius=cloud_head_radius, cloud_head_height=cloud_head_height)

 



@app.route('/refresh', methods=['POST'])
def clear_data():
    session.clear()  # Clear session data

    # Create a new blank Folium map
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Save it to 'map.html'
    m.save('C:\\Users\\Danie\\OneDrive\\Desktop\\Sublime Coding\\Nuclear\\static\\map.html')

    return redirect(url_for('home'))  # Redirect to home page

if __name__ == '__main__':
    app.run(debug=True)


