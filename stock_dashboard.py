import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import time

st.set_page_config(page_title="실시간 주식 대시보드", layout="wide")
st.title("🚀 실시간 주식 대시보드")
st.markdown("### 1분마다 자동 업데이트")

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "현대차": "005380.KS",
    "삼성바이오로직스": "207940.KS",
    "카카오": "035720.KS",
    "애플": "AAPL",
    "테슬라": "TSLA",
    "엔비디아": "NVDA",
    "마이크로소프트": "MSFT",
    "구글": "GOOGL",
    "Recursion Pharma": "RXRX",
    "Rocket Lab": "RKLB",
    "마이크론": "MU",
    "Credo Technology": "CRDO",
    "LVMH (ADR)": "LVMUY",
    "Hermes (ADR)": "HESAY"
}

selected_stock = st.sidebar.selectbox("종목 크게 보기", list(stocks.keys()))

period_options = {"5일": "5d", "1개월": "1mo", "3개월": "3mo", "6개월": "6mo"}
selected_period_label = st.sidebar.selectbox("차트 기간 선택", list(period_options.keys()))
selected_period = period_options[selected_period_label]

placeholder = st.empty()

def get_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period=period)
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    prev = info.get('regularMarketPreviousClose')
    change = price - prev if price and prev else 0
    change_pct = (change / prev * 100) if prev else 0
    return info, hist, price, change, change_pct

try:
    while True:
        with placeholder.container():
            kst = datetime.now(timezone.utc) + timedelta(hours=9)
            st.subheader(f"🕒 {kst.strftime('%Y년 %m월 %d일 %H:%M:%S')} (한국 시간)")

            cols = st.columns(5)
            for i, (name, ticker) in enumerate(stocks.items()):
                _, _, price, change, change_pct = get_stock_data(ticker, "5d")
                with cols[i % 5]:
                    st.metric(
                        label=f"**{name}**",
                        value=f"{price:,.2f}" if price else "N/A",
                        delta=f"{change:+.2f} ({change_pct:+.2f}%)"
                    )

            st.divider()
            st.subheader(f"📊 {selected_stock} 상세 분석 ({selected_period_label})")
            
            info, hist, price, change, change_pct = get_stock_data(stocks[selected_stock], selected_period)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("현재가", f"{price:,.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
            
            with col2:
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close']
                )])
                fig.update_layout(height=500, title=f"{selected_stock} {selected_period_label} 차트")
                st.plotly_chart(fig, use_container_width=True)

            st.caption("※ 1분마다 자동 업데이트 됩니다.")

        time.sleep(60)

except Exception as e:
    st.error(f"오류: {e}")
