# weather_solution.py



# ----- GIVEN CODE (do not change) -----
# Build the API URL using the chosen city's coordinates.
url = (f"https://api.open-meteo.com/v1/forecast"
       f"?latitude={city['lat']}&longitude={city['lon']}&current_weather=true")
data = requests.get(url).json()
# --------------------------------------



