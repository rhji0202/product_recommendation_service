from google.adk.agents import Agent,LlmAgent, ParallelAgent, SequentialAgent
from .sub_agents.keyword_extraction_agent import keyword_extraction_agent
from .sub_agents.category_search_agent import category_search_agent
from .sub_agents.product_search_agent import product_search_agent
from .sub_agents.filter_agent import filter_agent

search_info_agent = ParallelAgent(
    name="product_info",
    sub_agents=[category_search_agent, product_search_agent],
    description="The product info agent is the agent that can extract product info from the user input.",
)

recommend_agent = LlmAgent(
    name="search_info_agent",
    description="The search info agent is the agent that can search for product info from the user input.",
    model="gemini-2.0-flash",
    instruction="""
    당신은 검색결과를 바탕으로 상품추천 해주는 에이전트야


    검색 결과와 필터링된 결과를 바탕으로 상품을 추천해 주세요.
    필터링된 결과가 있는 경우 필터링된 결과를 우선적으로 추천해 주세요.
    """,
)

pipeline_agent = SequentialAgent(
    name="pipeline_agent",
    sub_agents=[keyword_extraction_agent, search_info_agent],
    description="The root agent is the agent that can extract product info from the user input.",
)

root_agent = Agent(
    name="root_agent",
    sub_agents=[pipeline_agent, filter_agent, recommend_agent],
    description="The root agent is the agent that can extract product info from the user input.",
    model="gemini-2.0-flash",
    instruction="""
    당신은 사용자의 입력을 바탕으로 상품을 추천해 주는 에이전트야
    """,
)