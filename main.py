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

# Request Data to the Alpha Vantage API
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': ALPHA_VANTAGE_API_KEY
}
response = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)

# Check the Date Today
date_today = datetime.now().date()

if date_today.weekday() == 0:
    diff = 3
else:
    diff = 1

yesterday = (date_today - timedelta(days=diff)).strftime("%Y-%m-%d")
day_before_yesterday = (date_today - timedelta(days=diff + 1)).strftime("%Y-%m-%d")

yesterday_closing_price = float(response.json()['Time Series (Daily)'][yesterday]['4. close'])
day_before_yesterday_closing_price = float(response.json()['Time Series (Daily)'][day_before_yesterday]['4. close'])

# Calculate the Change
difference = yesterday_closing_price - day_before_yesterday_closing_price
percentage = round(difference / day_before_yesterday_closing_price * 100, 3)

if percentage > 0:
    stock_change = f"GOOGL: 🔺{percentage}%"
elif percentage == 0:
    stock_change = f"GOOGL: 0%"
else:
    stock_change = f"GOOGL: 🔻{percentage}%"

# Get News when percentage is +-5%
if percentage >= 5 or percentage <= -5:
    news_parameters = {
        'q': "google",
        'apiKey': NEWS_API_KEY,
        'from': day_before_yesterday,
        'to': yesterday,
    }
    news_response = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)
    articles = news_response.json()['articles'][:3]

# Load Client to Send SMS
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Send SMS for every article
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
