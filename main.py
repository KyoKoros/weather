import json
import time

import requests
from json.decoder import JSONDecodeError
from plyer import notification


def get_weather(url, city, auth):
    try:
        headers = {"key": auth}
        response = requests.get(url=url + f"?q={city}", headers=headers)

        if response.status_code == 200:
            response_dict = response.json()
            weather_info = response_dict["current"]
            return weather_info
        else:
            return f"Error: {response.text} with code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Requestion exception: {e}"
    except Exception as e:
        return f"Exception has occurred: {e}"


def send_alerts(config, weather: dict):
    for city, v in weather.items():
        notification_alert = []
        if v["temp_c"] > config["max_temp"]:
            notification_alert.append(f"Temperatura este foarte mare: {v['temp_c']}")
        if v["wind_kph"] > config["max_wind_velocity"]:
            notification_alert.append(f"Viteza vantului este foarte mare: {v['wind_kph']}")
        if v["pressure_mb"] > config["max_pressure"]:
            notification_alert.append(f"Presiunea atmosferica este foarte mare: {v['pressure_mb']}")

        print(f"City: {city}\n" + "\n".join(notification_alert))

        if notification_alert:
            notification.notify(
                title=city,
                message=" ".join(notification_alert),
                app_icon=None,
                timeout=10,
            )
        time.sleep(5)


def init_config():
    try:
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        return config
    except JSONDecodeError as e:
        print(f"Exception raised because the JSON file is not valid: {e}")
        exit()
    except FileNotFoundError as e:
        print(f"Config file not found: {e}")
        exit()
    except PermissionError as e:
        print(f"Permission denied to read the config file: {e}")
        exit()
    except Exception as e:
        print(f"Unknown Exception: {e}")
        exit()


def read_cities():
    try:
        with open("cities.txt", "r") as f:
            cities = [line.strip() for line in f if line.strip()]
        return cities
    except FileNotFoundError:
        print("Cities file not found. Create a 'cities.txt' file with one city per line.")
        exit()


if __name__ == "__main__":
    print("Started script here")
    config = init_config()
    weather = {}
    cities = read_cities()
    for city in cities:
        weather[city] = get_weather(config["base_url"], city, auth=config["api_key"])

    send_alerts(config, weather)