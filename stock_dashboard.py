import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="실시간 주식 대시보드", layout="wide")
st.title("🚀 실시간 주식 대시보드")
st.markdown("### 1분마다 자동 업데이트")

# ================== 종목 리스트 (10개) ==================
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
    "구글(Alphabet)": "GOOGL"
}

# 사이드바 - 특정 종목 크게 보기
st.sidebar.header("🔍 종목 크게 보기")
selected_stock = st.sidebar.selectbox("종목 선택", list(stocks.keys()))

# 메인 대시보드
placeholder = st.empty()

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="5d")
    
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    prev_close = info.get('regularMarketPreviousClose')
    change = price - prev_close if price and prev_close else 0
    change_pct = (change / prev_close * 100) if prev_close else 0
    
    return info, hist, price, change, change_pct

try:
    while True:
        with placeholder.container():
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
            st.subheader(f"🕒 {current_time} 업데이트")

            # 전체 종목 카드
            cols = st.columns(5)
            for i, (name, ticker) in enumerate(stocks.items()):
                info, hist, price, change, change_pct = get_stock_data(ticker)
                color = "green" if change >= 0 else "red"
                
                with cols[i % 5]:
                    st.metric(
                        label=f"**{name}**",
                        value=f"{price:,.2f}" if price else "N/A",
                        delta=f"{change:+.2f} ({change_pct:+.2f}%)",
                        delta_color="normal"
                    )

            # 선택한 종목 크게 보기 + 차트
            st.divider()
            st.subheader(f"📊 {selected_stock} 상세 분석")
            
            info, hist, price, change, change_pct = get_stock_data(stocks[selected_stock])
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("현재가", f"{price:,.2f} USD" if "KS" not in stocks[selected_stock] else f"{price:,.0f} 원",
                         f"{change:+.2f} ({change_pct:+.2f}%)")
                st.write(f"**시가총액**: {info.get('marketCap', 0)/1000000000000:.2f}조 USD")
                
            with col2:
                # 차트
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name="가격"
                ))
                fig.update_layout(height=400, title=f"{selected_stock} 최근 5일 차트")
                st.plotly_chart(fig, use_container_width=True)

            st.caption("※ 1분마다 자동 업데이트 됩니다. (실시간이 아닌 1분 지연 데이터입니다)")

        time.sleep(60)  # 1분마다 업데이트

except KeyboardInterrupt:
    st.write("프로그램을 종료합니다.")
