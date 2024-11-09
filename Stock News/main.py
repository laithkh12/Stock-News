import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Retrieve sensitive information from environment variables
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE")

## STEP 1: Fetch stock price data
stockParams = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stockParams)
data = response.json()["Time Series (Daily)"]
dataList = [value for (key, value) in data.items()]
yesterdayData = dataList[0]
yesterdayClosingPrice = yesterdayData["4. close"]

# Get the day before yesterday's closing stock price
dayBeforeYesterdayData = dataList[1]
dayBeforeYesterdayClosingPrice = dayBeforeYesterdayData["4. close"]

# Calculate difference and percentage
difference = float(yesterdayClosingPrice) - float(dayBeforeYesterdayClosingPrice)
upDown = "🔺" if difference > 0 else "🔻"
diffPercent = round((difference / float(yesterdayClosingPrice)) * 100)

## STEP 2: Fetch news articles if the price change is significant
if abs(diffPercent) > 1:
    newsParams = {
        'apikey': NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    newsResponse = requests.get(NEWS_ENDPOINT, params=newsParams)
    articles = newsResponse.json()["articles"]
    threeArticles = articles[:3]

    # Format articles for SMS
    formattedArticles = [
        f"{STOCK_NAME}: {upDown}{diffPercent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in threeArticles
    ]

    ## STEP 3: Send each article as an SMS via Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formattedArticles:
        message = client.messages.create(body=article, from_=FROM_PHONE, to=TO_PHONE)
        print(f"Message sent: {message.sid}")
