from google.adk.agents import LlmAgent
from pydantic import BaseModel

class KeywordExtractionOutput(BaseModel):
    keywords: list[str]

keyword_extraction_agent = LlmAgent(
    name="keyword_extraction_agent",
    model="gemini-2.0-flash",
    description="A agent that can extract keywords from a text",
    instruction="""
u    당신은 사용자 입력을 분석하여 키워드를 추출하는 에디전트

    요청을 받으면, 다음 단계를 따르세요:
    1. 사용자 입력에서 중요한 키워드를 추출합니다.
    2. 추출된 키워드를 분석하여 키워드와 연관성 있는 키워드를 최대 5개까지 생성합니다.
    3. 키워드는 중복되지 않도록 합니다.


    결과는 다음을 포함하는 JSON 형식으로 반환합니다:
    - keywords: 추출된 키워드 리스트 (최대 5개)
    - 각 키워드는 소문자로 변환하고, 중복을 제거합니다.
    - 예시: {"keywords": ["전자제품", "스마트폰", "가전제품", "컴퓨터", "태블릿"]}

    중요
    - 키워드는 반드시 소문자로 변환하여 반환합니다.
    - 정보는 사용자의 입력과 관련된 주제나 제품을 나타내야 합니다.
    
    """,
    output_key="keywords",
    output_schema=KeywordExtractionOutput
)