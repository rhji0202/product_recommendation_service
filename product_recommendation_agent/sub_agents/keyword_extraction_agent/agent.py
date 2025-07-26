from google.adk.agents import LlmAgent
from pydantic import BaseModel

class KeywordExtractionOutput(BaseModel):
    keywords: list[str]

keyword_extraction_agent = LlmAgent(
    name="keyword_extraction_agent",
    model="gemini-2.0-flash",
    description="A agent that can extract keywords from a text",
    instruction="""
    당신은 사용자 입력을 분석하여 상품 카테고리와 관련 키워드를 추출하는 전문가입니다.

    사용자 입력으로부터 다음 정보를 추출하세요:
    1. 상품 카테고리: 사용자가 찾고 있는 상품의 카테고리를 정확하게 파악하세요.
    2. 관련 키워드: 사용자 입력에서 중요한 키워드를 추출하세요.

    예시:
    - 사용자 입력: "여름에 입을 트랜디한 티셔츠를 추천해줘"
      결과: ["여름", "트랜디", "티셔츠", "상의","남성","여성"]

    가이드라인:
    - 텍스트에서 중요한 키워드를 추출합니다.
    - 키워드는 최대 5개까지 추출합니다.
    - 키워드는 중복되지 않도록 추출합니다.
    - 항상 아래의 JSON 형식으로 출력합니다.
    - 추가 설명이나 다른 텍스트는 포함하지 마세요. 

    중요:
    ["여름", "트랜디", "티셔츠", "상의","남성","여성"]
    """,
    output_key="keywords",
    output_schema=KeywordExtractionOutput
)