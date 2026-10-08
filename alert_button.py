import os
import time
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise SystemExit("Please set BOT_TOKEN and CHAT_ID in .env.")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            button_pressed = True
            print("Someone pressed the alert button!")

            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": CHAT_ID,
                        "text": "Someone pressed the alert button!"
                    },
                    timeout=10
                )
                if response.status_code == 200 and response.json().get("ok"):
                    print("Telegram alert sent!")
                else:
                    print("Telegram rejected the alert. Check your settings.")
            except requests.exceptions.RequestException:
                print("Could not send alert. Check your internet connection.")

        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    GPIO.cleanup()
