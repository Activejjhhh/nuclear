# nuclear



18/05/23
## Code Improvements
Added a custom BSOD screen. Made the buttons easier to click and the text has been spaced out nicely
### Magic Numbers

The code has been updated to remove magic numbers. The values such as `(screen_width // 2 - title_surface.get_width() // 2)` and `button_width // 2 - login_surface.get_width() // 2` have been assigned to variables with descriptive names.

### Code Repetition

The code for drawing buttons has been refactored into a single function, `draw_button`, which takes the button text and position as arguments. This eliminates code repetition and improves maintainability.

### Error Handling

Error handling has been added to handle potential errors that may occur when loading or playing the sound file. This ensures that the application gracefully handles such errors and prevents crashes.

### Code Formatting

The code has been formatted consistently, using proper indentation and whitespace, to improve readability and maintain a clean code style.

## Credits
16/05/23
Added python programs Initialising and menu screen. When using them, make sure to change the file path for menu screen in initialising
