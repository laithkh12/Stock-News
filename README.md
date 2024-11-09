# 📈 Stock Price Notification System 📲

A Python application that monitors stock price fluctuations for Tesla (TSLA) and sends news updates via SMS when a significant price change occurs.

---

## 📜 Overview

This project uses **Alphavantage API** to get the latest stock price data, **News API** to retrieve recent news articles about Tesla, and **Twilio** to send SMS alerts. If Tesla's stock price changes by more than 5% from the previous day, the application sends an SMS with the latest news headlines related to Tesla.

---

## 📦 Features

- **Fetch Stock Data**: Retrieves the latest stock closing prices for TSLA.
- **Calculate Percentage Change**: Checks if the stock price has moved by a significant percentage.
- **Get News Articles**: Uses the News API to find relevant articles about Tesla.
- **Send SMS Alerts**: Sends each news headline and brief to the specified phone number via Twilio.

---

## 🛠️ Setup and Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/username/stock-price-notification.git
    ```
2. Install Dependencies: Make sure you have requests, python-dotenv, and twilio installed:
```bash
pip install requests python-dotenv twilio
```
3. Environment Variables: Create a .env file in the project root and add the following:
```plaintext
STOCK_API_KEY=your_alphavantage_api_key
NEWS_API_KEY=your_news_api_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
FROM_PHONE=your_twilio_phone_number
TO_PHONE=your_phone_number
```
---
## 📄 How It Works
### Step 1: Fetch Stock Price Data
The program retrieves the closing stock prices for TSLA over the last two days.
```python
stockParams = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stockParams)
data = response.json()["Time Series (Daily)"]
```
### Step 2: Calculate Percentage Change
It then calculates the percentage difference between the two most recent closing prices.
```python
difference = float(yesterdayClosingPrice) - float(dayBeforeYesterdayClosingPrice)
diffPercent = round((difference / float(yesterdayClosingPrice)) * 100)
```
### Step 3: Fetch News Articles
If the percentage change exceeds the threshold, the program fetches the top three news articles about Tesla.
```python
newsParams = {
    'apikey': NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}
newsResponse = requests.get(NEWS_ENDPOINT, params=newsParams)
```
### Step 4: Send SMS Alerts
Each news article is formatted and sent as an SMS message to the specified phone number.
```python
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in formattedArticles:
    message = client.messages.create(body=article, from_=FROM_PHONE, to=TO_PHONE)
```
---
## 🔍 Example Output
SMS Format:
```plaintext
TSLA: 🔺5%
Headline: Tesla Hits New Milestone
Brief: Tesla reached a new milestone today by ...
```
---
## 🔐 Security
Make sure to exclude your .env file from version control to keep your API keys and credentials secure.
---
## 📌 Notes
- You need to sign up for API keys from Alphavantage, News API, and Twilio.
- Ensure your Twilio account has SMS capabilities for the region you are targeting.
---
## 📧 Contact
For any questions or issues, feel free to reach out!
