import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# DATA
STOCK = "GOOGL"
COMPANY_NAME = "Alphabet Inc Class A"
ALPHA_VANTAGE_API_KEY = os.environ['ALPHA_VANTAGE_API_KEY']
NEWS_API_KEY = os.environ['NEWS_API_KEY']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = '+14706135180'
MY_PHONE_NUMBER = '+639561886073'
articles = []

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': ALPHA_VANTAGE_API_KEY
}
response = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)

# Check the date today
date_today = datetime.now().date()

if date_today.weekday() == 0:
    yesterday = (date_today - timedelta(days=3)).strftime("%Y-%m-%d")
    day_before_yesterday = (date_today - timedelta(days=4)).strftime("%Y-%m-%d")
else:
    yesterday = (date_today - timedelta(days=1)).strftime("%Y-%m-%d")
    day_before_yesterday = (date_today - timedelta(days=2)).strftime("%Y-%m-%d")

yesterday_closing = float(response.json()['Time Series (Daily)'][yesterday]['4. close'])
day_before_yesterday_closing = float(response.json()['Time Series (Daily)'][day_before_yesterday]['4. close'])

# Calculate the change
difference = yesterday_closing - day_before_yesterday_closing
percentage = round(difference / day_before_yesterday_closing * 100, 3)

if percentage > 0:
    stock_change = f"GOOGL: 🔺{percentage}%"
elif percentage == 0:
    stock_change = f"GOOGL: 0%"
else:
    stock_change = f"GOOGL: 🔻{percentage}%"

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
if percentage >= 5 or percentage <= -5:
    news_parameters = {
        'q': "google",
        'apiKey': NEWS_API_KEY,
        'from': day_before_yesterday,
        'to': yesterday,
    }
    news_response = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)
    articles = news_response.json()['articles'][:3]

# Load Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

for article in articles:
    body = f"{stock_change}\n" \
           f"Headline: {article['title']}\n" \
           f"Brief: {article['description']}\n"

    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )
    print(message.sid)