import requests
import google.generativeai as genai

# ⚠️ 주의: API 키는 반드시 재발급 받아서 아래에 넣으세요!
NEWS_API_KEY = '재발급_받은_NEWS_API_키'
GEMINI_API_KEY = '재발급_받은_GEMINI_API_키'

genai.configure(api_key=GEMINI_API_KEY)
# 모델 선언을 더 간결하게 변경
model = genai.GenerativeModel('gemini-1.5-flash')

def get_stock_news(symbol):
    print(f"🔍 {symbol} 관련 뉴스를 가져오는 중...")
    
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={NEWS_API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()

        # API 호출 제한(Rate Limit)이나 오류 메시지 확인
        if "Information" in data:
            print(f"⚠️ API 알림: {data['Information']}")
            return
        
        if "feed" not in data or not data['feed']:
            print("❌ 분석할 뉴스 데이터가 없습니다.")
            return

        # 첫 번째 뉴스 데이터 추출
        top_news = data['feed'][0]
        title = top_news.get('title', '제목 없음')
        summary_text = top_news.get('summary', '')

        print(f"\n📰 원본 뉴스 제목: {title}")
        print("-" * 50)
        
        if not summary_text:
            print("❌ 요약할 본문 내용이 부족합니다.")
            return

        print("🤖 AI가 뉴스를 분석 중입니다...")
        
        prompt = f"주식 종목 '{symbol}'에 대한 뉴스 요약이야. 내용을 한국어로 3줄 요약하고, 마지막에 '투자 관점(호재/악재)'을 명확히 써줘:\n\n{summary_text}"
        
        result = model.generate_content(prompt)
        print("\n✨ AI 요약 결과:")
        print(result.text)

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

# 실행
get_stock_news('NVDA')
