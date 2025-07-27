from google.adk.agents import Agent,LlmAgent
from .tools import search_product_by_keyword

product_search_agent = LlmAgent(
    name="product_search_agent",
    description="A agent that can search for products",
    model="gemini-2.0-flash",
    instruction="""
    당신은 키워드를 바탕으로 도구를 사용하여 상품을 조회하는 에이전트 입니다.

    상품 조회 요청을 받으면, 다음 단계를 따르세요:
    1. search_product_by_keyword 도구를 사용하여 상품을 추출합니다
    2. 검색된 딕셔너리를 그대로 반환합니다.
    
    도구는 다음을 포함하는 딕션너리를 리턴합니다
    - status: "success" 또는 "error"
    - total_count: 검색된 상품의 총 개수
    - products: 검색된 상품 리스트

    중요:
    - search_product_by_keyword 도구를 무조건 사용하여 상품을 검색합니다.
    - 검색된 상품이 없을 경우, 아래의 예시대로 결과를 반환합니다:
    - 예시: {"status": "false", "total_count": 0, "products": []}
    
    """,
    tools=[search_product_by_keyword],
    output_key="product_search_result"
)
