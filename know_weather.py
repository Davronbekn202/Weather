import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout
)


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_name = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel("☀️")
        self.description_label = QLabel("", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Alignment
        self.city_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # css uchun id berilgan
        self.city_name.setObjectName("city_name")
        self.city_input.setObjectName("city_input")
        self.weather_button.setObjectName("weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # cssda korinishi
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }

            QLabel#city_name {
                font-size: 40px;
                font-style: italic;
            }

            QLineEdit#city_input {
                font-size: 40px;
            }

            QPushButton#weather_button {
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                font-size: 75px;
            }

            QLabel#emoji_label {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }

            QLabel#description_label {
                font-size: 50px;
            }
        """)
        # knopkani ishga tushurib get_weatherga ulangan
        self.weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # shaxarlardagi malumotni izlaydigan kalit (API)
        api_key = 'dd6d605b88a4af7c804b5cbc20fc8a15'
        city = self.city_input.text()
        # userdan malumot olish
        if not city:
            self.description_label.setText("Enter a city!")
            return
        # url manzili
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        # manzilni va malumotni json fileda olish
        response = requests.get(url)
        data = response.json()
        # hato yoki shaxar mavjud bolmasa
        if data.get("cod") != 200:
            self.description_label.setText("City not found")
            self.temperature_label.setText("")
            self.emoji_label.setText("❌")
            return
        # jsondan qidirish keylardan foydalnib
        temp = int(data["main"]["temp"])
        description = data["weather"][0]["description"]
        # emojilar va nomlar
        emojis = {
            "clear": "☀️",
            "cloud": "☁️",
            "rain": "🌧️",
            "storm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️"
        }

        emoji = "🌍"
        for key in emojis:
            if key in description.lower():
                emoji = emojis[key]

        # ekranga chiqarish
        self.temperature_label.setText(f"{temp}°C")  # temperaturani chiqaradi
        self.description_label.setText(description.capitalize())  # sovuq yoki isiq yoki boshqalarni chiqazad
        self.emoji_label.setText(emoji)  # prosta emoji


# barchasi ishlatadi
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
