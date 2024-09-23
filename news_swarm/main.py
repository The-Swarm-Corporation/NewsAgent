import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Any
from news_swarm.prompts import NEWS_SYS_PROMPT
from pydantic import BaseModel, Field
from swarms import Agent, create_file_in_folder

from news_swarm.tool import fetch_stock_news


class InputLog(BaseModel):
    id: Optional[str] = Field(
        default=str(uuid.uuid4()),
        description="Unique identifier for the input log",
    )
    query: Optional[str]
    start_date: Optional[Any]
    end_date: Optional[Any]
    return_json: Optional[bool]
    max_articles: Optional[int] = 5
    time_stamp: Optional[str] = Field(
        default=time.strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of the input log",
    )


class OutputLogSummaries(BaseModel):
    id: Optional[str] = Field(
        default=str(uuid.uuid4()),
        description="Unique identifier for the output log summary",
    )
    articles: Optional[Any]  # Accept list of dictionaries
    summary: Optional[str]
    time_stamp: Optional[str] = Field(
        default=time.strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of the output log summary",
    )


class OutputLog(BaseModel):
    id: Optional[str] = Field(
        default=str(uuid.uuid4()),
        description="Unique identifier for the output log",
    )
    input_log: Optional[InputLog]
    output_logs: Optional[List[OutputLogSummaries]] = Field(
        ..., description=None
    )
    time_stamp: Optional[str] = Field(
        default=time.strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of the output log",
    )


def check_newsapi() -> str:
    try:
        key = os.getenv("NEWSAPI_API_KEY")
        return key
    except Exception:
        return None


class NewsAgent(Agent):
    """
    A specialized agent for fetching and processing news articles based on given tasks.
    It utilizes the News API to fetch articles and a language model to generate summaries.
    """

    def __init__(
        self,
        agent_name: str = "news_agent_v1",
        newsapi_api_key: str = None,
        system_prompt: str = None,
        agent: Agent = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        return_json: bool = False,
        max_articles: int = 5,
        autosave: bool = False,
    ):
        """
        Initializes the NewsAgent with the necessary parameters.

        Args:
            agent_name (str): The name of the agent.
            newsapi_api_key (str, optional): The API key for News API. Defaults to None.
            system_prompt (str, optional): The system prompt for the language model. Defaults to None.
            llm (BaseLLM, optional): The language model to use for summarization. Defaults to None.
            agent (Agent, optional): The base agent to inherit from. Defaults to None.
            start_date (Optional[str], optional): The start date for the news query in 'YYYY-MM-DD' format. Defaults to None.
            end_date (Optional[str], optional): The end date for the news query in 'YYYY-MM-DD' format. Defaults to None.
            return_json (bool, optional): If True, return the result as a JSON object, otherwise return a formatted string. Defaults to False.
            max_articles (int, optional): The maximum number of articles to fetch. Defaults to 5.
        """
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.newsapi_api_key = newsapi_api_key
        self.start_date = start_date
        self.end_date = end_date
        self.return_json = return_json
        self.max_articles = max_articles
        self.agent = agent
        self.autosave = autosave

        self.output_log = OutputLog(
            input_log=InputLog(
                query="",
                start_date=start_date,
                end_date=end_date,
                return_json=return_json,
                max_articles=max_articles,
            ),
            output_logs=[],
        )

        # Transition the sys prompt of the agent
        self.agent.system_prompt = NEWS_SYS_PROMPT

    def run(self, tasks: List[str], *args, **kwargs):
        """
        Runs the news fetching and summarization process sequentially for each task.

        Args:
            tasks (List[str]): A list of tasks or queries to process.

        Returns:
            Union[str, dict]: The output of the process, either a formatted string or a JSON object depending on the return_json parameter.
        """
        for task in tasks:
            self.output_log.input_log.query = task

            string_query, data_dict = fetch_stock_news(
                task,
                self.newsapi_api_key,
                self.start_date,
                self.end_date,
                max_articles=self.max_articles,
            )
            print(type(data_dict))

            summary = self.agent.run(string_query)

            output_log_indi = OutputLogSummaries(
                articles=data_dict,
                summary=summary,
            )

            self.output_log.output_logs.append(output_log_indi)

        # Save the log
        create_file_in_folder(
            "news_agent_runs",
            f"news_agent_run_id:{self.output_log.id}.json",
            self.output_log.model_dump_json(indent=4),
        )

        if self.return_json is True:
            return self.output_log.model_dump_json(indent=4)

        else:
            return summary

    def run_concurrently(self, tasks: List[str]) -> str:
        """
        Runs the news fetching and summarization process concurrently for each task.

        Args:
            tasks (List[str]): A list of tasks or queries to process.

        Returns:
            str: The output of the process as a JSON object.
        """
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.run, [task]): task
                for task in tasks
            }
            for future in futures:
                future.result()  # Wait for all tasks to complete

        return self.output_log.model_dump_json(indent=4)
