import requests
import math
from twilio.rest import Client

# Twilio account credentials
account_sid = 'GET FROM TWILIO'
auth_token = 'GET FROM TWILIO'
client = Client(account_sid, auth_token)

# Stock and company information
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Parameters for the stock API request
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "APIKEY",
    "datatype": "json",
}

# Fetch stock data
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_metadata = stock_response.json()["Meta Data"]
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

# Get most recent and previous day's closing prices
most_recent_price = data_list[0]["4. close"]
previous_day_closing_price = data_list[1]["4. close"]

# Calculate price difference and percentage change
five_percent = float(previous_day_closing_price) * 5 / 100
difference = abs(float(most_recent_price) - float(previous_day_closing_price))
difference_percentage = (difference / float(previous_day_closing_price)) * 100
difference_percentage = math.floor(difference_percentage)

# If the price change exceeds 5%, fetch news articles and send SMS alerts
if difference > five_percent:
    # Parameters for the news API request
    news_params = {
        "apiKey": "API KEY",
        "q": COMPANY_NAME,
        "language": "en",
        "pageSize": 3,
        "sortBy": "publishedAt",
        "to": stock_metadata["3. Last Refreshed"],
        "searchIn": "title"
    }
    
    # Fetch news data
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()["articles"]
    
    client = Client(account_sid, auth_token)
    for x in range(len(news_data)):
        if difference_percentage > 0:
            direction = "⬆️"
        else:
            direction = "⬇️"
        
        # Send SMS alert with the news details
        message = client.messages.create(
            body=f"TSLA:️ {direction}️ {difference_percentage}%\n\nHeadline: {news_data[x]['title']}\n"
                 f"Brief: {news_data[x]['description']}\nLink for more detail: {news_data[x]['url']}",
            from_='+VIRTUAL PHONE NUMBER',
            to='YOUR PHONE NUMBER'
        )
