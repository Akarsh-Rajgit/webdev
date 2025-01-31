from flask import Flask, request, render_template, jsonify
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

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
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data.index, data['Close'], label="Closing Price")
        ax.set_title(f"{ticker} - Stock Price Chart (Last Year)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (INR)")
        ax.legend()
        ax.grid()
        
        # Convert the plot to PNG and then to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_b64 = base64.b64encode(img.read()).decode('utf-8')
        plt.close(fig)
        return img_b64
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    company_name = request.form['company_name']
    ticker = get_ticker_by_name(company_name)
    if not ticker:
        return jsonify({"error": f"Unable to find a ticker for {company_name}. Please check the name."})
    
    stock = yf.Ticker(ticker)
    info = stock.info
    current_price = info.get('currentPrice', 'N/A')
    open_price = info.get('regularMarketOpen', 'N/A')
    previous_close = info.get('regularMarketPreviousClose', 'N/A')
    pe_ratio = info.get('trailingPE', 'N/A')
    pb_ratio = info.get('priceToBook', 'N/A')
    div_yield = info.get('dividendYield', 'N/A')

    stock_chart = get_stock_chart(ticker)

    return jsonify({
        "company_name": company_name,
        "ticker": ticker,
        "current_price": current_price,
        "open_price": open_price,
        "previous_close": previous_close,
        "pe_ratio": pe_ratio,
        "pb_ratio": pb_ratio,
        "div_yield": div_yield,
        "stock_chart": stock_chart
    })

if __name__ == "__main__":
    app.run(debug=True)
