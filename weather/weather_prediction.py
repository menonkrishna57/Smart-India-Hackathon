import requests
from dotenv import load_dotenv
import os
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
MUMBAI_COORDS = "19.0760,72.8777"
def get_weather_data(api_key, location):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3&aqi=no&alerts=yes"
    
    print("Fetching weather data from WeatherAPI.com...")
    try:
        response = requests.get(url)
        response.raise_for_status() 
        print("Data fetched successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
def analyze_weather(weather_data):
    
    warnings = []
    
    RAIN_CHANCE_THRESHOLD = 70
    HEAVY_RAIN_MM_THRESHOLD = 10
    HIGH_WIND_KPH_THRESHOLD = 50
    EXTREME_HEAT_C_THRESHOLD = 38
    
    if weather_data.get("alerts") and weather_data["alerts"]["alert"]:
        for alert in weather_data["alerts"]["alert"]:
            event = alert.get("event", "Weather Alert")
            headline = alert.get("headline", "No headline available.")
            warnings.append(f"[URGENT ALERT] {event}: {headline}")

    if "forecast" in weather_data and "forecastday" in weather_data["forecast"]:
        for i in range(min(2, len(weather_data["forecast"]["forecastday"]))):
            day_forecast = weather_data["forecast"]["forecastday"][i]
            day_info = day_forecast.get("day", {})
            
            day_name = "Today" if i == 0 else "Tomorrow"
            
            if day_info.get("daily_chance_of_rain", 0) > RAIN_CHANCE_THRESHOLD:
                warnings.append(f"[RAIN WARNING] High chance of rain ({day_info['daily_chance_of_rain']}%) forecast for {day_name}.")
                
            if day_info.get("totalprecip_mm", 0) > HEAVY_RAIN_MM_THRESHOLD:
                warnings.append(f"[HEAVY RAIN] Potential for heavy rain ({day_info['totalprecip_mm']}mm) forecast for {day_name}.")
            
            if day_info.get("maxwind_kph", 0) > HIGH_WIND_KPH_THRESHOLD:
                warnings.append(f"[HIGH WIND] Strong winds up to {day_info['maxwind_kph']} km/h expected for {day_name}.")
                
            if day_info.get("maxtemp_c", 0) > EXTREME_HEAT_C_THRESHOLD:
                warnings.append(f"[EXTREME HEAT] High temperatures of {day_info['maxtemp_c']}°C expected for {day_name}.")

            if day_info.get("daily_will_it_thunder", 0) == 1:
                warnings.append(f"[THUNDERSTORM] Thunderstorms are possible on {day_name}.")


    return warnings


if __name__ == "__main__":
    print("--- Farmer's Weather Shield (using WeatherAPI.com) ---")
    
    weather_data = get_weather_data(WEATHER_API_KEY, MUMBAI_COORDS)
    
    if weather_data:
        active_warnings = analyze_weather(weather_data)
        
        print("\n--- Analysis Complete ---")
        if active_warnings:
            print("Adverse weather conditions detected! Sending notifications:")
            for warning in sorted(list(set(active_warnings))):
                print(f"- {warning}")
        else:
            print("Weather conditions look clear. No warnings to send.")