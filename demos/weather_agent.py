"""Demo agent that fetches and processes weather data."""

import asyncio
import logging
import aiohttp
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

class WeatherAgent:
    """Agent that demonstrates API integration and data processing"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.weather_agent")
        self.name = "weather_agent"
        self.session = None
        
        # Demo API key - replace with your own
        self.api_key = "demo_key_123456789"
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def _init_session(self) -> None:
        """Initialize aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _kelvin_to_celsius(self, kelvin: float) -> float:
        """Convert Kelvin to Celsius"""
        return round(kelvin - 273.15, 1)

    def _kelvin_to_fahrenheit(self, kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit"""
        return round((kelvin - 273.15) * 9/5 + 32, 1)

    def _format_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw weather data"""
        temp_k = data["main"]["temp"]
        return {
            "location": {
                "city": data["name"],
                "country": data["sys"]["country"],
                "coordinates": {
                    "lat": data["coord"]["lat"],
                    "lon": data["coord"]["lon"]
                }
            },
            "temperature": {
                "celsius": self._kelvin_to_celsius(temp_k),
                "fahrenheit": self._kelvin_to_fahrenheit(temp_k)
            },
            "conditions": {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"]
            },
            "timestamp": datetime.fromtimestamp(data["dt"], timezone.utc).isoformat()
        }

    async def get_weather(
        self,
        city: str,
        country_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get current weather for a location"""
        try:
            await self._init_session()
            
            # Build query
            location = f"{city}"
            if country_code:
                location = f"{city},{country_code}"
            
            # Make API request
            self.log.info(f"Fetching weather data for {location}")
            params = {
                "q": location,
                "appid": self.api_key
            }
            
            async with self.session.get(
                f"{self.base_url}/weather",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    formatted_data = self._format_weather_data(data)
                    
                    return {
                        "status": "success",
                        "data": formatted_data,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"API error: {error_text}")
                    
        except Exception as e:
            self.log.error(f"Error fetching weather: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            await self._close_session()

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format weather data for display"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Weather Data Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  🌤️  Weather Report - {data['location']['city']}, {data['location']['country']}
╚══════════════════════════════════════════════════════════════════╝

📍 Location:
  • Coordinates: {data['location']['coordinates']['lat']}°N, {data['location']['coordinates']['lon']}°E

🌡️ Temperature:
  • Celsius: {data['temperature']['celsius']}°C
  • Fahrenheit: {data['temperature']['fahrenheit']}°F

🌥️ Conditions:
  • Weather: {data['conditions']['main']} ({data['conditions']['description']})
  • Humidity: {data['conditions']['humidity']}%
  • Pressure: {data['conditions']['pressure']} hPa
  • Wind Speed: {data['conditions']['wind_speed']} m/s

⏰ Last Updated: {data['timestamp']}
"""

async def main():
    """Demo the weather agent"""
    agent = WeatherAgent()
    
    # Demo cities
    locations = [
        ("London", "UK"),
        ("New York", "US"),
        ("Tokyo", "JP"),
        ("Sydney", "AU")
    ]
    
    for city, country in locations:
        result = await agent.get_weather(city, country)
        print(agent.format_output(result))
        await asyncio.sleep(1)  # Pause between demos

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())