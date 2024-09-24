
# News Agent

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@kyegomez3242) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kye-g-38759a207/) [![Follow on X.com](https://img.shields.io/badge/X.com-Follow-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/kyegomezb)


**NewsAgent** is an enterprise-grade news aggregation agent designed to fetch, query, and summarize news from multiple sources at scale. Built for modern businesses, NewsAgent enables you to automate the process of news monitoring, delivering summarized, relevant, and timely news from across the web. Whether you need real-time updates or comprehensive analysis, NewsAgent can seamlessly integrate into your workflows, ensuring that you always stay informed.

<!-- ## Key Features


- **Multi-Article Summarization**: Efficiently summarizes multiple articles at once, reducing the noise and delivering concise insights. -->

## Installation

To install **NewsAgent**, use the following command:

```bash
pip3 install -U news-swarm
```

Ensure that you have Python 3.10+ installed.

## Environment Variables

```txt
OPENAI_API_KEY="if you use openai"
WORKSPACE_DIR="agent_workspace"
NEWSAPI_API_KEY="api from the newsapi"
```

## Quick Start
```python
import os

from dotenv import load_dotenv
from swarm_models import OpenAIChat
from swarms import Agent

from news_swarm.main import NewsAgent

load_dotenv()

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAIChat class
model = OpenAIChat(
    openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.1
)

# Initialize the agent
base_agent = Agent(
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
    agent=base_agent,
    newsapi_api_key=os.getenv("NEWSAPI_API_KEY"),
    system_prompt=None,
    return_json=True,
    # start_date="2024-08-01",
    # end_date="2024-08-10"
)


# Run the agent
print(agent.run("multi-agent collaboration"))
print(agent.run_concurrently(["OpenAI", "Anthropic"]))


```


<!-- 
### 3. Customize Query Parameters

You can customize query parameters such as date ranges, languages, and source priorities:

```python
summary = agent.fetch_and_summarize(
    "Quantum Computing", 
    date_range="2023-01-01:2023-09-01", 
    language="en", 
    sources=["nytimes", "bbc"]
)

print(summary)
``` -->

<!-- 
## Advanced Usage

**NewsAgent** also supports advanced use cases such as bulk fetching and deep analysis of specific sectors:

### Bulk Fetching

For large-scale news aggregation across multiple industries:

```python
topics = ["Financial Markets", "Healthcare", "Technology"]
summaries = agent.bulk_fetch_and_summarize(topics, sources=["forbes", "reuters", "bloomberg"])

for topic, summary in summaries.items():
    print(f"Topic: {topic}\nSummary: {summary}\n")
```

### Integration with Enterprise Systems

Easily integrate **NewsAgent** with your company's internal systems via the provided API endpoints or through webhook support for real-time notifications.

```python
agent.start_monitoring(
    "Cybersecurity", 
    interval=1800,  # 30 minutes
    on_update_callback=your_enterprise_notification_system.notify
)
``` -->

<!-- ## Security

NewsAgent follows strict security protocols:
- **API Key Encryption**: All API keys are securely stored and transmitted using industry-standard encryption methods.
- **Data Privacy**: NewsAgent does not store any news data or summaries beyond what is necessary for real-time operations. -->

## Enterprise Support

For enterprise customers, we offer:
- **24/7 Priority Support**
- **Custom Feature Development**
- **Integration Assistance** for your existing platforms (CRM, ERP, etc.)

For more information on enterprise solutions, contact us at [kye@swarms.world](mailto:kye@swarms.world).

# Todo
- **Smart Query Crafting**: Automatically creates optimized queries using an llm to fetch the most relevant news from multiple sources.
- **Real-Time Updates**: Fetch news in real-time or set scheduled intervals for continuous monitoring.
- **Customizable Sources**: Add or remove specific news sources, tailored to your business needs.
<!-- - **Enterprise Integration**: Easily integrates into existing enterprise platforms for automated news monitoring and alert systems. -->
- **Bing API**: Implement Bing API for search
- **Google API**: Implement Google API for search
- **Free Seaarch**: Implement a free, fast, reliable search mechanism that runs completely locally and privately. 


## Contributing

We welcome contributions! If you'd like to contribute to **NewsAgent**, please open an issue or submit a pull request via our [GitHub repository](https://github.com/The-Swarm-Corporation/NewsAgent).

## License

**NewsAgent** is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

