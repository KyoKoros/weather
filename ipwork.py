import json
import requests
from datetime import datetime

def get_location(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            location_data = response.json()
            return location_data
        else:
            return f"Error: {response.text} with code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Requestion exception: {e}"
    except Exception as e:
        return f"Exception has occurred: {e}"

def get_weather(api_key, lat, lon):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            return f"Error: {response.text} with code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Requestion exception: {e}"
    except Exception as e:
        return f"Exception has occurred: {e}"

def print_ip_weather(ip):
    location_data = get_location(ip)
    if isinstance(location_data, dict) and 'city' in location_data:
        city = location_data['city']
        print(f"IP: {ip}")
        print(f"Location: {city}")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Current Time: {current_time}")

        if 'latitude' in location_data and 'longitude' in location_data:
            lat = location_data['latitude']
            lon = location_data['longitude']
            weather_data = get_weather(api_key, lat, lon)
            if isinstance(weather_data, dict) and 'current' in weather_data:
                temp_c = weather_data['current']['temp_c']
                condition = weather_data['current']['condition']['text']
                print(f"Weather: {condition}")
                print(f"Temperature: {temp_c}°C")
                print()
            else:
                print(f"Error retrieving weather data: {weather_data}")
        else:
            print("Latitude or longitude data missing.")
    else:
        print(f"Error retrieving location data: {location_data}")


if __name__ == "__main__":
    api_key = "0a299760cdec49369d0154300232206"


    ip_file = "ip_list.txt"
    with open(ip_file, "r") as f:
        ip_list = [line.strip() for line in f if line.strip()]


    for ip in ip_list:
        print_ip_weather(ip)