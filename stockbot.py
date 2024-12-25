import requests
import yfinance as yf
import matplotlib.pyplot as plt

company_to_ticker = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Tata Consultancy Services": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Titan": "TITAN.NS",
    "JSW Energy": "JSWENERGY.NS",
}

def get_ticker_by_name(company_name):
    company_name = company_name.strip()
    if company_name in company_to_ticker:
        return company_to_ticker[company_name]
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('quotes', [])
        if results:
            symbol = results[0].get('symbol')
            if symbol and ".NS" not in symbol:
                symbol += ".NS"
            return symbol
    return None

def get_stock_chart(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    if not data.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label="Closing Price")
        plt.title(f"{ticker} - Stock Price Chart (Last Year)")
        plt.xlabel("Date")
        plt.ylabel("Price (INR)")
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print(f"No data available for {ticker}.")

def fundamental_analysis(company_name):
    ticker = get_ticker_by_name(company_name)
    if not ticker:
        print(f"Unable to find a ticker for {company_name}. Please check the name.")
        return
    stock = yf.Ticker(ticker)
    info = stock.info
    current_price = info.get('currentPrice', 'N/A')
    open_price = info.get('regularMarketOpen', 'N/A')
    previous_close = info.get('regularMarketPreviousClose', 'N/A')
    pe_ratio = info.get('trailingPE', 'N/A')
    pb_ratio = info.get('priceToBook', 'N/A')
    div_yield = info.get('dividendYield', 'N/A')

    print(f"Fundamental Analysis for {company_name} ({ticker})")
    print("=" * 50)
    print(f"Name: {info.get('longName', 'N/A')}")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"Market Cap: {info.get('marketCap', 'N/A')}")
    print(f"Current Price: {current_price}")
    print(f"Opening Price: {open_price}")
    print(f"Previous Close: {previous_close}")
    print(f"PE Ratio: {pe_ratio}")
    print(f"PB Ratio: {pb_ratio}")
    print(f"Dividend Yield: {div_yield}")
    print("=" * 50)
    get_stock_chart(ticker)

def main():
    while True:
        company_name = input("Enter the full name of the Indian company (or type 'exit' to quit): ").strip()
        if company_name.lower() == 'exit':
            print("Exiting the program.")
            break
        fundamental_analysis(company_name)

if __name__ == "__main__":
    main()
#c:\Users\AKARSH RAJ M H\OneDrive\Documents\PLC Files\codes\stockbot.py