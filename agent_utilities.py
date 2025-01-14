import os
from dotenv import load_dotenv, find_dotenv
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.github import GithubTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.firecrawl import FirecrawlTools
import requests
from config_manager import ConfigManager


def initialize_env():
    """
    Load environment variables from .env file.
    """
    load_dotenv(find_dotenv())

class AgentManager:
    """
    Handles creation and configuration of agents with predefined roles and tools.
    """
    def __init__(self):
        self.config = ConfigManager()  ## Initialize ConfigManager

    @staticmethod
    def create_github_agent():
        """
        Create an agent for fetching repositories of a specified GitHub profile.
        """
        return Agent(
            name="Github Repository Agent",
            role="Provide all the repositories of Jiten-Bhalavat that are not forked.",
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
            instructions=[
                     "Use your tools to answer questions about the profile: Jiten-Bhalavat",
                     "This profile has multiple repos which are both forked as well as Own, You have to provide only which are not forked",
                     "First you have to provide few information from the Overview section and then You have to visit the profile and provide me the First Five repos of Jiten-Bhalavat"
                    ],
            tools=[GithubTools(access_token=os.getenv("GITHUB_API_TOKEN"), list_repositories=True, get_repository=True)],
            show_tool_calls=True,
        )

    @staticmethod
    def create_medium_agent():
        """
        Create an agent for scraping Medium blog posts.
        """
        return Agent(
            name="Medium AI Agent",
            role="Provide all the blog posts of Jiten-Bhalavat's Medium profile.",
            instructions=["Your task is to scrape the posts from my Medium account.",
                  "Please gather the names of all the posts I have uploaded on my account and present them in a clear list format.",
                  "Ensure that you capture every post title, without including any other details like publication dates or descriptions.",
                  "The focus is solely on the titles of the posts I have shared"],
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
            tools=[FirecrawlTools(scrape=False, crawl=True, api_key=os.getenv("FIRECRAWL_API_KEY"), limit=5)],
            show_tool_calls=True, markdown=True,
        )

    @staticmethod
    def create_general_agent():
        """
        Create an agent for providing general information about Jiten-Bhalavat.
        """
        return Agent(
            name="General AI Agent",
            role="Provide necessary and important information about Jiten-Bhalavat.",
            instructions=["Explore everything about Jiten-Bhalavat and provide all important information in brief."],
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
            tools=[DuckDuckGo()],
            show_tool_calls=True,
        )
    
    @staticmethod
    def create_linkedin_agent():
        """
        Create an agent for fetching LinkedIn profile data.
        """
        url = "https://api.scrapin.io/enrichment"
        querystring = {"apikey":os.getenv("Linkedin_Crawl_API_KEY"),"firstName":"Jiten","lastName":"Bhalavat","email":"jitenbhalavat@gmail.com"}
        response = requests.request("GET", url, params=querystring)

        return Agent(
            name="Linkedin Scrapper AI Agent",
            role="Provides the Necessary Information from Resposne",
            instructions=[f"Your task is to provide me the necessary and important details from {response.json()}."],
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
            markdown=True
        )

    @staticmethod
    def create_personal_agent():
        """
        Create a personal agent combining multiple agents into a team.
        """
        github_agent = AgentManager.create_github_agent()
        medium_agent = AgentManager.create_medium_agent()
        general_agent = AgentManager.create_general_agent()
        linkedin_agent = AgentManager.create_linkedin_agent()

        return Agent(
            team=[general_agent, linkedin_agent, github_agent, medium_agent],
            instructions=["""You are part of a team with specific tasks:
                            general_agent="Provide me all the necessary and Important information about Jiten-Bhalavat in 6-7 Sentences"
                            github_agent='''Your task is to analyze the information and generate a clear and concise 5-6 line summary.
                            The summary should:
                            Highlight the main focus or purpose of the repositories.
                            Mention key technologies or frameworks used (if available).
                            Emphasize any unique or standout features.
                            Avoid overly technical jargon while still being informative.'''
                            medium_agent="Provide the Blogs Post Names for this https://infinityai.medium.com/"
                            linkedin_agent="Provide me Education, Experience and Top 3 Posts of Jiten-Bhalavat." 
                          """],
            markdown=True,
        )
