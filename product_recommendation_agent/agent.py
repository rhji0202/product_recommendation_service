from google.adk.agents import Agent,LlmAgent, ParallelAgent, SequentialAgent
from .sub_agents.keyword_extraction_agent import keyword_extraction_agent
from .sub_agents.category_search_agent import category_search_agent

product_info = ParallelAgent(
    name="product_info",
    sub_agents=[category_search_agent],
    description="The product info agent is the agent that can extract product info from the user input.",
)

root_agent = SequentialAgent(
    name="pipe_line",
    sub_agents=[keyword_extraction_agent, product_info],
    description="The pipe line agent is the agent that can extract product info from the user input.",
)

