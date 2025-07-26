from google.adk.agents import Agent,LlmAgent
from pydantic import BaseModel
from typing import List
from .tools import search_category_by_keyword

class CategorySearchOutput(BaseModel):
    category_search_result: List[str]

category_search_agent = Agent(
    name="category_search_agent",
    description="A agent that can search for categories",
    model="gemini-2.0-flash",
    instruction="""
    당신은 키워드를 바탕으로 도구를 사용하여 상품 카테고리를 추출하는 전문가입니다.

    키워드로 카테고리를 추출하세요:
    - 사용자가 제공한 키워드나 문장에서 관련 카테고리를 찾습니다.
    - 키워드와 가장 관련성이 높은 카테고리를 선택합니다.
    - 키워드에 여러 카테고리가 관련될 수 있는 경우, 가장 구체적인 카테고리를 선택합니다.
    - 키워드에 해당하는 카테고리가 없는 경우, 가장 유사한 카테고리를 추천합니다.

    도구:
    - search_category_by_keyword: 키워드를 기반으로 카테고리를 검색합니다.
    
    가이드라인:
    - 키워드를 바탕으로 도구를 사용하여 상품 카테고리를 추출합니다.

    """,
    tools=[search_category_by_keyword],
    output_key="category_search_output"
)