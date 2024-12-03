"""
    Name: weather_utils.py
    Author: William A Loring
    Created: 06/20/2021
    Purpose: Store OpenWeatherMap API key and other items
    for easy import into OpenWeatherMap based apps
"""
import datetime
import math


#----------------------- OPENWEATHERMAP API KEY ---------------------------#
API_KEY = 'Put your OpenWeatherMap Key Here'

# One Call Parameters
PARAMETERS_WEATHER = {
    "appid": API_KEY,
    "units": "imperial"
}


#--------------------------------- URLS --------------------------------------#
URL = "http://api.openweathermap.org/data/2.5/weather?appid=" + \
    API_KEY + "&units=imperial&q="

ONE_CALL_URL = "https://api.openweathermap.org/data/2.5/onecall"

AQI_ENDPOINT = "http://api.openweathermap.org/data/2.5/air_pollution?appid=" + API_KEY


#--------------------------- UV INDEX STRING -----------------------------------#
def uvi_to_string(uvi):
    if uvi >= 11:
        uvi_string = "Extreme"
    elif uvi >= 8:
        uvi_string = "Very High"
    elif uvi >= 6:
        uvi_string = "High"
    elif uvi >= 3:
        uvi_string = "Moderate"
    elif uvi >= 0:
        uvi_string = "Low"

    return uvi_string


#--------------------------- CONVERT TIME -----------------------------------#
def convert_day_time(time):
    """
        Convert GMT Unix time to local day time
    """
    # Convert Unix timestamp to Python datetime
    time = datetime.datetime.fromtimestamp(time)

    # Format the date to hours, AM PM
    time = time.strftime("%m/%d/%Y")

    # Strip out the leading 0's
    time = time.lstrip("0")
    return time


#--------------------------- CONVERT TIME -----------------------------------#
def convert_hourly_time(time):
    """
        Convert GMT Unix time to local hourly time
    """
    # Convert Unix timestamp to Python datetime
    time = datetime.datetime.fromtimestamp(time)

    # Format the date to hours, AM PM
    time = time.strftime("%I:%S %p")

    # Strip out the leading 0's
    time = time.lstrip("0")
    return time


#----------------------------- CONVERT TIME --------------------------------#
def convert_time(time):
    """
        Convert GMT Unix time to local time
    """
    # Convert Unix timestamp to local Python datetime
    time = datetime.datetime.fromtimestamp(time)
    # Format the date to hours, minutes, seconds, AM PM
    time = f"{time:%I:%M:%S %p}"
    # Strip out the leading 0's: 01 becomes 1
    time = time.lstrip("0")
    # Return GMT Unix as local Python time object
    return time


#---------------------------------------------------- CONVERT DEGREES TO CARDINAL #
def degrees_to_cardinal(degrees):
    """ Convert degrees to cardinal directions """

    # Tuple of cardinal directions clockwise for 360 degrees
    cardinal_directions = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")

    # Divide 360 degrees into 16 segments 0-15
    # 22.5 degrees per segment
    # Shift incoming degrees by 11.25 to match Cardinal to Degree
    # Round down to the nearest integer
    cardinal_index = math.floor((degrees+11.25) / 22.5)

    # Take care of 348 to 360 returning 16, set to 0
    cardinal_index = cardinal_index % 16

    # Return the cardinal direction based on the tuple index
    return cardinal_directions[cardinal_index]


#----------------------- PROGRAM BANNER -------------------------------------#
WEATHER_BANNER = """
 _    _            _   _                
| |  | |          | | | |               
| |  | | ___  __ _| |_| |__   ___ _ __  
| |/\| |/ _ \/ _` | __| '_ \ / _ \ '__| 
\  /\  /  __/ (_| | |_| | | |  __/ | 
 \/  \/ \___|\__,_|\__|_| |_|\___|_| """

#----------------------- ASCII DECORATED TITLE -----------------------------#


def title(statement):
    '''
        Takes in a string argument
        returns a string with ascii decorations
    '''
    # Get the length of the statement
    text_length = len(statement)

    # Create the title string
    # Initialize the result string variable
    result = ""
    result = result + "+--" + "-" * text_length + "--+\n"
    result = result + "|  " + statement + "  |\n"
    result = result + "+--" + "-" * text_length + "--+"

    # Return the contatenated title string
    return result


#-------------------------- GOODBYE ----------------------------#
def goodbye():
    """
        Print goodbye to user
    """
    print(title("Good bye from OWM Weather App!"))
