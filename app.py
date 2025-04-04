from flask import Flask, request, render_template, jsonify
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

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
    ticker = request.form['ticker'].strip()

    stock = yf.Ticker(ticker)
    info = stock.info
    
    if not info:
        return jsonify({"error": f"Unable to fetch data for {ticker}. Please check the ticker code."})
    
    current_price = info.get('currentPrice', 'N/A')
    open_price = info.get('regularMarketOpen', 'N/A')
    previous_close = info.get('regularMarketPreviousClose', 'N/A')
    pe_ratio = info.get('trailingPE', 'N/A')
    pb_ratio = info.get('priceToBook', 'N/A')
    div_yield = info.get('dividendYield', 'N/A')

    stock_chart = get_stock_chart(ticker)

    return jsonify({
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
