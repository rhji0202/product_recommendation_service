from google.adk.agents import LlmAgent
from typing import List, Dict, Any
from .tools import filter_products

filter_agent = LlmAgent(
    name="filter_agent",
    description="An agent that can filter products based on criteria like price range, brand, and other attributes",
    model="gemini-2.0-flash",
    instruction="""
    당신은 사용자 요청에 따라 상품 목록을 필터링하는 에이전트입니다.

    필터링 요청을 받으면, 다음 단계를 따르세요:
    1. 사용자 입력에서 필터링 조건을 추출합니다 (가격 범위, 브랜드, 모델명, 키워드 등)
    2. filter_products 도구를 사용하여 조건에 맞는 상품만 필터링합니다
    3. 필터링된 상품 목록을 반환합니다

    필터링 조건:
    - min_price: 최소 가격 (이상)
    - max_price: 최대 가격 (이하)
    - brands: 브랜드 목록 (포함)
    - model_names: 모델명 목록 (포함)
    - keywords: 상품명이나 설명에 포함될 키워드 목록

    결과는 다음을 포함하는 JSON 형식으로 반환합니다:
    - filtered_products: 필터링된 상품 목록
    - total_count: 필터링된 상품 수
    - status: "success" 또는 "error"

    예시:
    입력: {
      "products": [상품목록],
      "filter_criteria": {
        "min_price": 10000,
        "max_price": 50000,
        "brands": ["삼성", "LG"]
      }
    }
    
    출력: {
      "filtered_products": [필터링된 상품목록],
      "total_count": 5,
      "status": "success"
    }

    중요:
    - filter_products 도구를 무조건 사용하여 상품을 필터링합니다
    - 필터링 조건이 없는 경우 모든 상품을 반환합니다
    - 필터링된 상품이 없을 경우, 빈 목록과 함께 total_count: 0을 반환합니다
    - 모든 필터링 조건은 AND 조건으로 적용됩니다 (모든 조건을 만족해야 함)
    """,
    tools=[filter_products],
    output_key="filtered_products"
)
