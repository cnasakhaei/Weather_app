from django.shortcuts import render
from django.shortcuts import render
import requests
from datetime import datetime

def get_weather_info(city_name):
    api_key = "7a275e09915223beec68641b735bfdb9"
    get_geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city_name,
        "appid": api_key
    }

    

    response = requests.get(url=get_geo_url, params=params)
    response_json = response.json()
    
    if response_json:
        lat = response_json[0]["lat"]
        lon = response_json[0]["lon"]
        
        air_pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        weather_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key
        }
        
        air_pollution_response = requests.get(air_pollution_url, params=params)
        air_pollution = air_pollution_response.json()

        response = requests.get(weather_url, params=params)
        weather_info = response.json()

        if weather_info['cod'] == 200:
            temp = int(weather_info['main']['temp'] - 273)
            feels_like_temp = int(weather_info['main']['feels_like'] - 273)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']
            icon_num = weather_info["weather"][0]["icon"]
            icon = "https://openweathermap.org/img/wn/" + icon_num +"@2x.png"
            sunrise_time = time_format_for_location(sunrise + timezone)
            sunset_time = time_format_for_location(sunset + timezone)
            quality = air_pollution["list"][0]["main"]["aqi"]
            def switch_case(quality):
                if quality == 1:
                    return("Good")
                elif quality == 2:
                    return("Fair")
                elif quality == 3:
                    return("Moderate")
                elif quality == 4:
                    return("Poor")
                elif quality == 5:
                    return("Very Poor")
                else:
                    return("Air pollution not found!")
            return {
                "status" : True,
                "temp" : temp,
                "feels" : feels_like_temp,
                "pressure" : pressure,
                "humidity" : humidity,
                "wind_speed" : wind_speed,
                "sunrise" : sunrise,
                "sunset" : sunset,
                "timezone" : timezone,
                "cloudy" : cloudy,
                "description" : description,
                "sunrise_time" : sunrise_time,
                "sunset_time" : sunset_time,
                "icon" : icon,
                "air" : switch_case(quality)
            }
        
        else:
            return {"status" : False, "message" : f"Weather for '{city_name}' not found! Kindly enter a valid City Name!"}
    else:
        return{"status" : False, "message" : f"City '{city_name}' not found! Kindly enter a valid City Name!"}

def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

def show_weather(request):
    city_name = request.GET.get('city_name', False)
    if city_name == False:
        return render(request, 'weather/weather.html')
    weather_info = get_weather_info(city_name)
    return render(request, 'weather/weather.html', {'weather_info': weather_info, 'city_name':city_name})


