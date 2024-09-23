import os

from dotenv import load_dotenv
from swarm_models import OpenAIChat
from swarms import Agent

from news_agent.main import NewsAgent

load_dotenv()

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAIChat class
model = OpenAIChat(
    openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.1
)

# Initialize the agent
agent = Agent(
    agent_name="News-Agent-V1",
    # system_prompt=FINANCIAL_AGENT_SYS_PROMPT,
    llm=model,
    max_loops=1,
    autosave=True,
    dashboard=False,
    verbose=True,
    dynamic_temperature_enabled=True,
    saved_state_path="news_agent.json",
    user_name="swarms_corp",
    retry_attempts=1,
    context_length=200000,
    return_step_meta=False,
    # output_type="json",
)

# Agent
agent = NewsAgent(
    agent_name="news-agent-v1",
    agent=agent,
    newsapi_api_key=os.getenv("NEWSAPI_API_KEY"),
    system_prompt=None,
    return_json=True,
    # start_date="2024-08-01",
    # end_date="2024-08-10"
)


# Run the agent
# agent.run(["multi-agent collaboration"])
agent.run_concurrently(["Swarm Multi-Agent", "AGI"])
