# Nuclear

## Project Updates

### 18/05/23
#### Code Improvements
- Added a custom BSOD screen.
- Made the buttons easier to click and spaced out the text nicely.

#### Magic Numbers
- The code has been updated to remove magic numbers by assigning values to variables with descriptive names. For example, `(screen_width // 2 - title_surface.get_width() // 2)` and `button_width // 2 - login_surface.get_width() // 2`.

#### Code Repetition
- Refactored the code for drawing buttons into a single function, `draw_button`. This function takes the button text and position as arguments, eliminating code repetition and improving maintainability.

#### Error Handling
- Added error handling to handle potential errors that may occur when loading or playing sound files. This ensures graceful handling of errors and prevents crashes.

#### Code Formatting
- Formatted the code consistently with proper indentation and whitespace for improved readability and maintainability.

### Missile Launch System Addition
#### 23/05/23
- Added a missile launch system to the project.
- Integrated the `geopy.geocoders` module's `Nominatim` functionality to find locations for the missile launch system.
- Included warhead libraries to support different warhead configurations.
- Implemented calculations for air density, drag, thrust, length, diameter, stage 1 mass, stage 2 mass, stage 3 mass, yield, and range.

#### 16/05/23
- Added python programs for initializing and the menu screen.
- When using these programs, please remember to change the file path for the menu screen in the initializing script.

### Adding maps
#### 14/10/23
- Added maps using folium
- Allows you to select a destination to launch and hit.
- Flask web application that takes two city names as input, retrieves their coordinates using the Geopy library, and then uses Folium to create a map showing a geodesic path between those two points.

#### 07/11/23
- Retired some features of thw missile launch, Starting a basic trajectory calculator 
