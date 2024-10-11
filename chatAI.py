#demo basic code for idea
import requests
from flask import Flask, request, jsonify

# تنظیمات پیام‌رسان
username = "your_username"
password = "your_password"
from_number = "your_line_number"

# تنظیمات Flask
app = Flask(__name__)

# تابع ارسال پیامک با پیام‌رسان
def send_sms(to_number, message):
    url = "https://api.payam-resan.com/v1/sms/send/bulk"
    payload = {
        "Username": username,
        "Password": password,
        "From": from_number,
        "To": [to_number],
        "Text": message,
    }
    response = requests.post(url, json=payload)
    return response.json()

# ارسال سوال به API چت جی پی تی مینی و دریافت پاسخ
def send_to_chatgpt_mini(question):
    api_url = "https://api.chatgpt-mini.com/ask"  # آدرس فرضی API چت جی پی تی مینی
    headers = {
        "Authorization": "Bearer your_api_key",
        "Content-Type": "application/json"
    }
    data = {
        "question": question,
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()["answer"]  # فرض می‌کنیم پاسخ در فیلد 'answer' باشد

# دریافت پیامک و ارسال به چت جی پی تی مینی
@app.route("/receive_sms", methods=['POST'])
def receive_sms():
    # دریافت متن پیامک و شماره فرستنده
    user_number = request.form.get('From')
    user_message = request.form.get('Body')

    # ارسال پیام به چت جی پی تی مینی و دریافت پاسخ
    chatgpt_reply = send_to_chatgpt_mini(user_message)

    # ارسال پاسخ به شماره کاربر
    send_sms(user_number, chatgpt_reply)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(debug=True)

