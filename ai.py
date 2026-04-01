import requests
import google.generativeai as genai

# 1. 키 설정 (그대로 유지)
NEWS_API_KEY = '89XN2QBUE10HAGJS'
GEMINI_API_KEY = 'AIzaSyBpnEGg4q-Mm1Wd_DW7El7C0uG0O6bxBjE'

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------------------
# [치트키 구문] 내 컴퓨터에서 사용 가능한 모델을 자동으로 찾아옵니다.
# ---------------------------------------------------------
try:
    # 내 계정에서 쓸 수 있는 모델 중 'flash'가 들어간 첫 번째 모델을 자동으로 선택
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = [m for m in available_models if 'flash' in m][0]
    print(f"✅ 자동으로 찾은 모델명: {target_model}")
    model = genai.GenerativeModel(target_model)
except Exception:
    # 자동 찾기가 실패할 경우를 대비한 수동 지정 (최종 방어선)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
# ---------------------------------------------------------

def get_stock_news(symbol):
    print(f"🔍 {symbol} 관련 뉴스를 가져오는 중...")
    
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if "feed" not in data:
        print("❌ 뉴스를 가져오지 못했습니다.")
        return

    # 첫 번째 뉴스 데이터
    top_news = data['feed'][0]
    title = top_news['title']
    summary_text = top_news['summary']

    print(f"\n📰 원본 뉴스 제목: {title}")
    print("-" * 50)
    print("🤖 AI가 뉴스를 분석하고 요약하는 중입니다...")
    
    prompt = f"다음 주식 뉴스 내용을 한국어로 3줄 요약하고 투자 관점(호재/악재)을 알려줘: {summary_text}"
    
    try:
        result = model.generate_content(prompt)
        print("\n✨ AI 요약 결과:")
        print(result.text)
    except Exception as e:
        print(f"❌ 요약 실패: {e}")

# 실행
get_stock_news('NVDA')