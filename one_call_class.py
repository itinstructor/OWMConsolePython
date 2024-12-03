"""
    Name: one_call_class.py
    Author: William A Loring
    Created: 07/04/21
    Purpose: OOP console app
    Get lat and lon from Openweather map current weather
    Use lat and lon for One Call Weather
    Use geopy to reverse lookup to confirm location
"""

import datetime
import requests
import weather_utils
# import geocode_owm for reverse geocode
import geocode_geopy


class OneCall:
    def __init__(self):
        """ Initialize object """
        # Field width constants for printing in columns
        self.__WIDTH = 13
        self.__AQI_WIDTH = 26
        # Create empty dictionary for weather data
        self.__weather_data = {}
        print(weather_utils.WEATHER_BANNER)
        print(weather_utils.title("Welcome to OpenWeatherMap Weather App!"))

#--------------------------------- GET LOCATION -------------------------------------#
    def get_location(self):
        """
            Get weather location and weather information
        """
        try:
            # Get location input from user
            city = input("Enter city or zip: ")
            if city.isdecimal():
                state = ""
            else:
                state = input("Enter state: ")
                state += ","

            city += ","
            country = input("Enter country: ")

            # Build the weather query
            self.__location = f"{city}{state}{country}"

            # Build the openweathermap api url
            url = weather_utils.URL + self.__location

            # Get the weather information out as a weather object
            response = requests.get(url)
            # print(response.text)

            # If the status_code is 200, successful connection and data
            if(response.status_code == 200):
                # Load json response into __weather dictionary
                weather_data = response.json()
                # For testing
                # print(self.__weather)
                # Let user know the connection was successful
                print("\n[+] The connection to OpenWeatherMap was successful.")
                # Get latitude and longitude from owm
                self.__latitude = weather_data.get("coord").get("lat")
                self.__longitude = weather_data.get("coord").get("lon")

                # Reverse gecode the address with geopy Nominatim to confirm address
                self.__address = geocode_geopy.reverse_geocode(
                    self.__latitude,
                    self.__longitude
                )

                # Get weather information for the location
                self.get_one_call_weather()
            else:
                # Recursive call if the user types in invalid information
                print(f"The response status code was: {response.status_code}")
                print("You may have typed an invalid location.")
                print("Please try again.")
                self.get_location()
        except:
            print("[-] Sorry, there was a problem connecting.")

#-------------------------- GET ONE CALL WEATHER DATA -------------------------------#
    def get_one_call_weather(self):
        """ Get one call weather data """
        try:
            # Parameters for building the URL
            weather_params = {
                "lat": self.__latitude,
                "lon": self.__longitude,
                "appid": weather_utils.API_KEY,
                "units": "imperial",
                "exclude": "minutely"
            }

            # Make request to API with parameters
            self.response = requests.get(
                weather_utils.ONE_CALL_URL,
                params=weather_params
            )

            # Testing
            # print(response.content)
            # Raise exception if anything other than status code 200
            self.response.raise_for_status

        # Recursive call for error to try a new location
        except Exception as e:
            print(e)
            print("Oops, try again.")
            self.get_location()

        # Get weather data as python dictionary
        self.__weather_data = self.response.json()
        print("="*70)

        # Print reverse geocode address to confirm location
        print(f"{self.__address}")

#----------------------------- GET CURRENT WEATHER ----------------------------------#
    def get_current_weather(self):
        """
            Get current weather from One Call weather data
        """
        # Create dictionary of current weather data
        weather_dict = self.__weather_data.get("current")
        # Get time of data calculation
        self.__data_time = weather_utils.convert_time(weather_dict.get("dt"))
        # Weather description, Clear, Partly Cloudy
        self.__description = weather_dict.get(
            "weather")[0].get("description").title()
        self.__temperature = weather_dict.get("temp")
        self.__feels_like = weather_dict.get("feels_like")
        self.__humidity = weather_dict.get("humidity")
        self.__wind_speed = weather_dict.get("wind_speed")
        self.__wind_direction = weather_dict.get("wind_deg")
        # Get pascals and convert to inches of mercury
        self.__pressure = round(weather_dict.get('pressure') / 33.86, 2)
        self.__clouds = weather_dict.get("clouds")

        # Get visibility in meters, convert to miles
        self.__visibility = round(
            weather_dict.get("visibility") * 0.00062137, 1)
        # Get sunrise and sunset time
        self.__sunrise_time = weather_utils.convert_time(
            weather_dict.get("sunrise"))
        self.__sunset_time = weather_utils.convert_time(
            weather_dict.get("sunset"))
        self.__uvi = weather_dict.get("uvi")

#-------------------------- DISPLAY CURRENT WEATHER ---------------------------------#
    def display_current_weather(self):
        """
            Display current weather
        """
        # Print weather information to console
        print()
        print("="*70)
        print(f'Current weather at {self.__data_time} ☀')
        print(f"{self.__address}")
        print("="*70)
        print(self.__description)
        print(f'{"Temperature:":{self.__WIDTH}} {self.__temperature}°F 🌡')
        print(f'{"Feels Like:":{self.__WIDTH}} {self.__feels_like}°F')
        print(f'{"Humidity:":{self.__WIDTH}} {self.__humidity}%')
        print(f'{"Wind:":{self.__WIDTH}} {self.__wind_speed} mph {weather_utils.degrees_to_cardinal(self.__wind_direction)}')
        print(f'{"Pressure:":{self.__WIDTH}} {self.__pressure} inHg')
        print(f'{"Cloud Cover:":{self.__WIDTH}} {self.__clouds}% ☁️')
        print(f'{"Visibility:":{self.__WIDTH}} {self.__visibility} miles')
        print(f'{"Sunrise:":{self.__WIDTH}} {self.__sunrise_time}')
        print(f'{"Sunset:":{self.__WIDTH}} {self.__sunset_time}')
        print(f'{"Latitude:":{self.__WIDTH}} {self.__latitude}')
        print(f'{"Longitude:":{self.__WIDTH}} {self.__longitude}')
        print(
            f'{"UV Index:":{self.__WIDTH}} {self.__uvi} {weather_utils.uvi_to_string(self.__uvi)}')
        print("-"*70)
        # Display Air Quality Index and major pollutants
        print(
            f"{'Air Quality Index:':{self.__AQI_WIDTH}} {self.__aqi} {self.__aqi_string}")
        print(f"{'Ground Level Ozone (O₃):':{self.__AQI_WIDTH}} {self.__o3}")
        print(f"{'Fine Particulates (PM25):':{self.__AQI_WIDTH}} {self.__pm25}")
        print(f"{'Carbon Monoxide (CO):':{self.__AQI_WIDTH}} {self.__co}")
        print(f"{'Sulphur Dioxide (SO₂):':{self.__AQI_WIDTH}} {self.__so2}")
        print(f"{'Nitrogen Dioxide (NO₂):':{self.__AQI_WIDTH}} {self.__no2}")


#----------------------------- 12-HOUR FORECAST -------------------------------------#

    def get_twelve_hour(self):
        """
            Get 12-hour forecast from One Call Weather data
        """
        # Slice 12 hours out of weather_data
        weather_slice = self.__weather_data["hourly"][:12]

        print()
        print("="*70)
        print(
            f"12 Hour Weather Forecast for {datetime.datetime.now():%m/%d/%Y}")
        print(f"{self.__address}")
        print("="*70)
        print(f"  Time      Temp    Humidity  Wind Spd")

        # Iterate through the temps
        for hourly_data in weather_slice:
            temp = hourly_data["temp"]
            description = hourly_data["weather"][0]["main"]
            humidity = hourly_data["humidity"]
            wind_speed = hourly_data["wind_speed"]
            time = weather_utils.convert_hourly_time(hourly_data["dt"])
            print(
                f"{time:>8}: {temp:>5.1f} °F | {humidity:4.1f} % | {wind_speed:4.1f} mph | {description}")
        print()

#----------------------------- 48-HOUR FORECAST -------------------------------------#
    def get_forty_eight_hour(self):
        """
            Get 48-hour forecast from One Call Weather data
        """
        # Slice 48 hours out of weather_data
        weather_slice = self.__weather_data["hourly"][:]

        print()
        print("="*70)
        print(
            f"48 Hour Weather Forecast for {datetime.datetime.now():%m/%d/%Y}")
        print(f"{self.__address}")
        print("="*70)

        counter = 0
        # Iterate through the hourly weather data
        for hourly_data in weather_slice:
            counter += 1
            # Only display every even data slice
            if counter % 2:
                temp = hourly_data["temp"]
                description = hourly_data["weather"][0]["main"]
                time = weather_utils.convert_hourly_time(hourly_data["dt"])
                print(f"{time:>8}: {temp:>5.1f} °F  {description}")
        print()

#------------------------------- 7-DAY FORECAST -------------------------------------#
    def get_seven_day(self):
        """
            Get 7 day forecast from One Call Weather data
        """
        # Slice the daily list out of weather_data
        weather_slice = self.__weather_data["daily"][:]

        print("="*70)
        print(f"                 7 Day Forecast")
        print(f"{self.__address}")
        print("="*70)
        # print(f"Weather Forecast for {datetime.datetime.now():%m/%d/%Y}")
        print(f"Date           Max       Min     Wind Spd  ")
        # Iterate through the temps
        for daily_data in weather_slice:
            temp_max = daily_data["temp"]["max"]
            temp_min = daily_data["temp"]["min"]
            wind_speed = daily_data["wind_speed"]
            description = daily_data["weather"][0]["description"].title()
            time = weather_utils.convert_day_time(daily_data["dt"])
            print(
                f"{time:>9} {temp_max:7.1f} °F | {temp_min:4.1f} °F | {wind_speed:4.1f} mph | {description}")

#------------------------------- AIR QUALITY INDEX -------------------------------------#
    def get_air_quality(self):
        """ 
            Get Air Quality Index from OpenWeatherMap with API call
        """
        params = {
            "lat": self.__latitude,
            "lon": self.__longitude
        }
        # Build request with url and parameters
        url = weather_utils.AQI_ENDPOINT
        response = requests.get(url, params)
        # print(response.text)

        # If the status_code is 200, successful connection and data
        if(response.status_code == 200):
            # Load json response into dictionary
            data = response.json()
            # Air Quality Index (SQI)
            self.__aqi = data.get("list")[0].get("main").get("aqi")
            # Ground level ozone
            self.__o3 = data.get("list")[0].get("components").get("o3")
            # Carbon Monoxide
            self.__co = data.get("list")[0].get("components").get("co")
            # Sulphur Dioxide
            self.__so2 = data.get("list")[0].get("components").get("so2")
            # Nitrogen Dioxide
            self.__no2 = data.get("list")[0].get("components").get("no2")
            # Fine particulates
            self.__pm25 = data.get("list")[0].get("components").get("pm2_5")

            # Convert AQI to text
            if self.__aqi == 1:
                self.__aqi_string = "Good"
            elif self.__aqi == 2:
                self.__aqi_string = "Fair"
            elif self.__aqi == 3:
                self.__aqi_string = "Moderate"
            elif self.__aqi == 4:
                self.__aqi_string = "Poor"
            elif self.__aqi == 5:
                self.__aqi_string = "Very Poor"
