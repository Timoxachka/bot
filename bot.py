import sqlite3
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "7853278815:AAEsRlNglIhdIY7gq9hJlGVz59rTJ-D5Vfk"
CHANNEL_ID = "-1002281157592"

def check_subscription(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_ID, "user_id": user_id}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("ok") and data["result"]["status"] in ["member", "administrator", "creator"]:
        return True
    return False

@app.route('/check-subscription', methods=['POST'])
def check_subscription_route():
    user_id = request.json.get('user_id')
    if check_subscription(user_id):
        return jsonify({"subscribed": True})
    return jsonify({"subscribed": False})

@app.route('/get-referral-link', methods=['POST'])
def get_referral_link():
    user_id = request.json.get('user_id')
    conn = sqlite3.connect('referral_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT referral_link FROM users WHERE telegram_id=?", (user_id,))
    link = cursor.fetchone()
    conn.close()
    if link:
        return jsonify({"link": link[0]})
    return jsonify({"link": None})

if __name__ == '__main__':
    app.run(port=5000)