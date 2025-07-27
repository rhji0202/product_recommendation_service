from google.adk.agents import Agent,LlmAgent
from .tools import search_category_by_keyword

category_search_agent = Agent(
    name="category_search_agent",
    description="A agent that can search for categories",
    model="gemini-2.0-flash",
    instruction="""
    당신은 키워드를 바탕으로 도구를 사용하여 상품 카테고리를 테이블 조회하는 에이전트 입니다.

    카테고리 조회 요청을 받으면, 다음 단계를 따르세요:
    1. search_category_by_keyword 도구를 사용하여 카테고리를 추출합니다
    2. 검색된 딕셔너리를 그대로 반환합니다.
    
    도구는 다음을 포함하는 딕션너리를 리턴합니다
    - status: "success" 또는 "error"
    - total_count: 검색된 카테고리의 총 개수
    - categories: 검색된 카테고리 리스트

    중요:
    - search_category_by_keyword 도구를 무조건 사용하여 카테고리를 검색합니다.
    - 검색된 카테고리가 없을 경우, 아래의 예시대로 결과를 반환합니다:
    - 예시: {"status": "false", "total_count": 0, "categories": []}
    
    """,
    tools=[search_category_by_keyword],
    output_key="category_search_output"
)
