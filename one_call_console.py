"""
    Name: one_call_console.py
    Author: William A Loring
    Created: 06/20/2021
    Purpose: Main program
    Get one call weather data from OpenWeatherMap.org API with requests and json
"""

import weather_utils
import one_call_class


#-------------------------------- MENU -------------------------------------#
def menu():
    """
        Print menu for user, return menu choice
    """
    print("-"*70)
    print(f"[1] Get current weather and AQI")
    print(f"[2] Get 12 hour forecast")
    print(f"[3] Get 48 hour forecast")
    print(f"[4] Get 7 day forecast")
    print(f"[5] Get new location")
    menu_choice = input(f"[Enter] to quit. Enter your choice: ")
    return menu_choice


#------------------------ MAIN PROGRAM -------------------------------------#
def main():
    # Create program object
    one_call = one_call_class.OneCall()

    # Get initial location for one call weather data and AQI
    # These are the only methods that make an API call
    # The other methods display the data in different formats
    one_call.get_location()
    one_call.get_air_quality()

    # Menu loop
    while True:
        # Display menu choices
        menu_choice = menu()

        # If the user presses the enter key, exit program
        if menu_choice == "":
            # Exit loop
            break

        # Get and display the current weather and air quality
        elif menu_choice == "1":
            one_call.get_current_weather()
            one_call.display_current_weather()
        # Get and display 12 hour forecast
        elif menu_choice == "2":
            one_call.get_twelve_hour()
        # Get and display 48 hour forecast
        elif menu_choice == "3":
            one_call.get_forty_eight_hour()
        # Get and display 7 day forecast
        elif menu_choice == "4":
            one_call.get_seven_day()
        # Make API call for a new location
        elif menu_choice == "5":
            one_call.get_location()

    # Say goodbye to the user as the program exits
    weather_utils.goodbye()


# Call main method to start the program
main()
