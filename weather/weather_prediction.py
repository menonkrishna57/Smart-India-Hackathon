# Import the necessary libraries
import requests
from dotenv import load_dotenv
import os
# --- Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual WeatherAPI.com API key
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# Coordinates for Mumbai, Maharashtra, India
MUMBAI_COORDS = "19.0760,72.8777"

# --- The "Weather Watchdog" (for WeatherAPI.com) ---
def get_weather_data(api_key, location):
    """Fetches weather data from the WeatherAPI.com forecast API."""
    
    # We ask for a 3-day forecast and specify that we want alerts
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

# --- The "Decision Maker" (UPGRADED) ---
def analyze_weather(weather_data):
    """Analyzes weather data from WeatherAPI.com and returns a list of warnings."""
    
    warnings = []
    
    # --- Define our thresholds for warnings ---
    RAIN_CHANCE_THRESHOLD = 70 # percent
    HEAVY_RAIN_MM_THRESHOLD = 10 # millimeters
    HIGH_WIND_KPH_THRESHOLD = 50 # kilometers per hour
    EXTREME_HEAT_C_THRESHOLD = 38 # Celsius
    
    # 1. Check for Official Weather Alerts
    if weather_data.get("alerts") and weather_data["alerts"]["alert"]:
        for alert in weather_data["alerts"]["alert"]:
            event = alert.get("event", "Weather Alert")
            headline = alert.get("headline", "No headline available.")
            warnings.append(f"[URGENT ALERT] {event}: {headline}")

    # The forecast data is in a list called 'forecastday'
    if "forecast" in weather_data and "forecastday" in weather_data["forecast"]:
        # We check for today (index 0) and tomorrow (index 1)
        for i in range(min(2, len(weather_data["forecast"]["forecastday"]))):
            day_forecast = weather_data["forecast"]["forecastday"][i]
            day_info = day_forecast.get("day", {})
            
            day_name = "Today" if i == 0 else "Tomorrow"
            
            # 2. Check for high chance of rain
            if day_info.get("daily_chance_of_rain", 0) > RAIN_CHANCE_THRESHOLD:
                warnings.append(f"[RAIN WARNING] High chance of rain ({day_info['daily_chance_of_rain']}%) forecast for {day_name}.")
                
            # 3. Check for heavy rain volume
            if day_info.get("totalprecip_mm", 0) > HEAVY_RAIN_MM_THRESHOLD:
                warnings.append(f"[HEAVY RAIN] Potential for heavy rain ({day_info['totalprecip_mm']}mm) forecast for {day_name}.")
            
            # 4. NEW: Check for high winds
            if day_info.get("maxwind_kph", 0) > HIGH_WIND_KPH_THRESHOLD:
                warnings.append(f"[HIGH WIND] Strong winds up to {day_info['maxwind_kph']} km/h expected for {day_name}.")
                
            # 5. NEW: Check for extreme heat (heatwave)
            if day_info.get("maxtemp_c", 0) > EXTREME_HEAT_C_THRESHOLD:
                warnings.append(f"[EXTREME HEAT] High temperatures of {day_info['maxtemp_c']}°C expected for {day_name}.")

            # 6. NEW: Check for thunderstorms
            if day_info.get("daily_will_it_thunder", 0) == 1:
                warnings.append(f"[THUNDERSTORM] Thunderstorms are possible on {day_name}.")


    return warnings


# --- Main script execution ---
if __name__ == "__main__":
    print("--- Farmer's Weather Shield (using WeatherAPI.com) ---")
    
    weather_data = get_weather_data(WEATHER_API_KEY, MUMBAI_COORDS)
    
    if weather_data:
        active_warnings = analyze_weather(weather_data)
        
        print("\n--- Analysis Complete ---")
        if active_warnings:
            print("Adverse weather conditions detected! Sending notifications:")
            # Use a set to only print unique warnings
            for warning in sorted(list(set(active_warnings))):
                print(f"- {warning}")
        else:
            print("Weather conditions look clear. No warnings to send.")