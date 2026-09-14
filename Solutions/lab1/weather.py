# weather_solution.py

# Task 1 — Import the tool that talks to the internet.
import requests

# Task 3 — Read all cities from the file into a list of dictionaries.
# Each line of cities.txt looks like: 1,Tokyo,35.6895,139.6917
cities = []
with open("cities.txt") as f:
    for line in f:
        number, name, lat, lon = line.strip().split(",")
        cities.append({"number": int(number), "name": name,
                       "lat": float(lat), "lon": float(lon)})

# Task 4 — Ask the user which city they want (input is text, so convert to int).
choice = int(input("Enter a city number (1-50): "))

# Task 5 — Find the matching city and stop searching once found.
city = None
for c in cities:
    if c["number"] == choice:
        city = c
        break

#if city == None:
#    raise SystemExit("City not found. Please check the number and try again.")

# ----- GIVEN CODE (do not change) -----
# Build the API URL using the chosen city's coordinates.
url = (f"https://api.open-meteo.com/v1/forecast"
       f"?latitude={city['lat']}&longitude={city['lon']}&current_weather=true")
data = requests.get(url).json()
# --------------------------------------

# Task 6 — Dig into the reply and show the result.
weather = data["current_weather"]
print(f"Weather in {city['name']}:")
print(f"Temperature: {weather['temperature']}°C")
print(f"Wind speed: {weather['windspeed']} km/h")