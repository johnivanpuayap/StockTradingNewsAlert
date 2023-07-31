import os
from datetime import datetime, timedelta

import requests

# DATA
STOCK = "GOOGL"
COMPANY_NAME = "Alphabet Inc Class A"
ALPHA_VANTAGE_API_KEY = os.environ['ALPHA_VANTAGE_API_KEY']

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
    print(f"GOOGL: 🔺{percentage}%")
elif percentage == 0:
    print(f"GOOGLE: 0%")
else:
    print(f"GOOGL: 🔻{percentage}%")

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
if -5 > percentage > 5:
    print("Get News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
