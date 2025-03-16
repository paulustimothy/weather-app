import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                            QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from dotenv import load_dotenv
import os

class WeatherApp(QWidget):
    load_dotenv()

    # Constants
    API_KEY = os.getenv('API_KEY')
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    WEATHER_EMOJIS = {
        (200, 232): "⛈",  # Thunderstorm
        (300, 321): "🌦",  # Drizzle
        (500, 531): "🌧",  # Rain
        (600, 622): "❄",   # Snow
        (700, 741): "🌫",  # Mist/Fog
        (762, 762): "🌋",  # Volcanic ash
        (771, 771): "💨",  # Squall
        (781, 781): "🌪",  # Tornado
        (800, 800): "☀",   # Clear sky
        (801, 804): "☁"    # Clouds
    }

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        self.setup_styles()
        self.setup_connections()

    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("weather.png"))

    def create_widgets(self):
        """Create all widgets"""
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Set object names for styling
        for widget, name in [
            (self.city_label, "city_label"),
            (self.city_input, "city_input"),
            (self.get_weather_button, "get_weather_button"),
            (self.temperature_label, "temperature_label"),
            (self.emoji_label, "emoji_label"),
            (self.description_label, "description_label")
        ]:
            widget.setObjectName(name)
            if isinstance(widget, QLabel):
                widget.setAlignment(Qt.AlignCenter)
            self.city_input.setAlignment(Qt.AlignCenter)

    def setup_layout(self):
        """Setup the layout"""
        layout = QVBoxLayout()
        
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        
        self.setLayout(layout)

    def setup_styles(self):
        """Setup the stylesheet"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;  
                color: #2c3e50;            
            }
            
            QLabel, QPushButton {
                font-family: 'Segoe UI', calibri;
                padding: 5px;
                margin: 2px;
            }
            
            QLineEdit#city_input {
                font-size: 40px;
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: white;
            }
            
            QLineEdit#city_input:focus {
                border-color: #2980b9;
                background-color: #ecf0f1;
            }
            
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
            }
            
            QPushButton#get_weather_button:hover {
                background-color: #2980b9;
            }
            
            QPushButton#get_weather_button:pressed {
                background-color: #2472a4;
            }
            
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            QLabel#temperature_label {
                font-size: 40px;
                font-weight: bold;
                color: #e74c3c; 
            }
            
            QLabel#emoji_label {
                font-size: 100px;
                font-family: 'Segoe UI Emoji';
            }
            
            QLabel#description_label {
                font-size: 50px;
                color: #27ae60;
            }
        """)

    def setup_connections(self):
        """Setup signal connections"""
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        """Fetch weather data from API"""
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name.")
            return
        
        url = f"{self.BASE_URL}?q={city}&appid={self.API_KEY}"

        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            self.handle_http_error(status_code)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nPlease check your internet connection")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error: {req_error}")

    def handle_http_error(self, status_code: int):
        """Handle different HTTP error codes"""
        error_messages = {
            400: "Bad Request\nPlease check your city name",
            401: "Unauthorized\nPlease check your API key",
            403: "Forbidden\nPlease check your API key",
            404: "Not Found\nPlease check your city name",
            500: "Internal Server Error\nPlease try again later",
            502: "Bad Gateway\nInvalid Response from Server",
            503: "Service Unavailable\nServer is down",
            504: "Gateway Timeout\nNo response from server"
        }
        message = error_messages.get(status_code, f"An error occurred: {status_code}")
        self.display_error(message)

    def display_error(self, message):
        """Display error message in the UI."""
        self.temperature_label.setStyleSheet("font-size: 20px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data: dict):
        """Display weather information"""
        self.temperature_label.setStyleSheet("font-size: 50px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        temp_f = (temp_k * 9/5) - 459.67
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temp_c:.0f}°C\n{temp_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_desc.capitalize())

        # Add country to city name if not present
        current_text = self.city_input.text()
        if "," not in current_text:
            self.city_input.setText(current_text + ", " + data["sys"]["country"])

    def get_weather_emoji(self, weather_id: int) -> str:
        """Get weather emoji based on weather ID"""
        for (start, end), emoji in self.WEATHER_EMOJIS.items():
            if start <= weather_id <= end:
                return emoji
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

