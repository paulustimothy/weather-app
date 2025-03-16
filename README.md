# Weather App

A simple desktop weather application built with PyQt5 that displays current weather information using the OpenWeatherMap API.

## Features
- Real-time weather data
- Temperature in Celsius and Fahrenheit
- Weather description with emojis
- Clean and modern UI
- City search with country code display

## Requirements
- Python 3.x
- PyQt5
- requests
- python-dotenv

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

2. Install required packages:
```bash
pip install PyQt5 requests python-dotenv
```

3. Get an API key:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/)
   - Get your API key from your account dashboard

4. Set up environment:
   - Create a `.env` file in the project directory
   - Add your API key:
     ```
     API_KEY=your_api_key_here
     ```

## Usage
Run the application:
```bash
python weatherApp.py
```

- Enter a city name in the input field
- Click "Get Weather" or press Enter
- View the current weather information

## Credit
Special Thanks to BroCode
