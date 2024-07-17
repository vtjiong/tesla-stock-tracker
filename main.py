import requests
import math
from twilio.rest import Client

account_sid = 'GET FROM TWILIO'
auth_token = 'GET FROM TWILIO'
client = Client(account_sid, auth_token)
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "APIKEY",
    "datatype": "json",
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_metadata = stock_response.json()["Meta Data"]
stock_data= stock_response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in stock_data.items()]
most_recent_price = data_list[0]["4. close"]
previous_day_closing_price = data_list[1]["4. close"]
five_percent = float(previous_day_closing_price) * 5 / 100
difference = abs(float(most_recent_price) - float(previous_day_closing_price))
difference_percentage = (difference / float(previous_day_closing_price)) * 100
difference_percentage = math.floor(difference_percentage)

if difference > five_percent:
    news_params=params = {
    "apiKey": "apiKey",
    "q": COMPANY_NAME,
    "language": "en",
    "pageSize": 3,
    "sortBy": "publishedAt",
    "to": stock_metadata["3. Last Refreshed"],
    "searchIn": "title"
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data=news_response.json()["articles"]
    client = Client(account_sid, auth_token)
    for x in range (len(news_data)):
        if difference_percentage > 0:
            direction = "⬆️"
        else:
            direction= "⬇️"
        message = client.messages.create(
            body=f"TSLA:️ {direction}️ {difference_percentage}%\n\nHeadline: {news_data[x]['title']}\nBrief: {news_data[x]['description']}\nLink for more detail=: {news_data[x]['url']}",
            from_='+VIRTUAL PHONE NUMBER',
            to='YOUR PHONE NUMBER'
            )
