from flask import Flask
import threading
import subprocess
import os
import time

app = Flask(__name__)

def run_bot():
    # Запускаем основного бота
    while True:
        try:
            subprocess.run(["python", "bot.py"])
        except Exception as e:
            print(f"Бот упал: {e}, перезапускаю через 5 секунд")
            time.sleep(5)

# Запускаем бота в фоне
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

@app.route('/')
def health():
    return "Бот работает", 200

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)