from phi.agent import Agent
from phi.model.openai import OpenAIChat
import os
from phi.agent import Agent, RunResponse
from phi.tools.github import GithubTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.firecrawl import FirecrawlTools
import requests
import pygame
from io import BytesIO
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_=load_dotenv(find_dotenv())

github_agent = Agent(
    name="Github Repository Agent",
    role="Proivde all the Repositories of Jiten-Bhalavat",
    model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
    instructions=[
        "Use your tools to answer questions about the profile: Jiten-Bhalavat",
        "This profile has multiple repos which are both forked as well as Own, You have to provide only which are not forked",
        "First you have to provide few information from the Overview section and then You have to visit the profile and provide me the First Five repos of Jiten-Bhalavat"
    ],
    tools=[GithubTools(access_token=os.getenv("GITHUB_API_TOKEN") , list_repositories=True, get_repository=True)],
    show_tool_calls=True,
)

medium_agent = Agent(
    name="Medium AI Agent",
    role="Provide all the Blog Post of Jiten-Bhalavat profile named: infinityai.medium.com",
    instructions=["Your task is to scrape the posts from my Medium account.",
                  "Please gather the names of all the posts I have uploaded on my account and present them in a clear list format.",
                  "Ensure that you capture every post title, without including any other details like publication dates or descriptions.",
                  "The focus is solely on the titles of the posts I’ve shared"],
    model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[
        FirecrawlTools(scrape=False, crawl=True, api_key=os.getenv('FIRECRAWL_API_KEY'), limit=5),
        ],
    show_tool_calls=True, markdown=True)

general_agent = Agent(
    name="General AI Agent",
    role="Provides Necessary and Important Information of Jiten-Bhalavat",
    instructions=[
        "Explore everything about Jiten-Bhalavat and provide all his important information in brief",
      ],
      model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
      tools=[DuckDuckGo()], show_tool_calls=True)

headers = {'Authorization': 'Bearer ' + os.getenv("Linkedin_Crawl_API_KEY")}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': 'https://www.linkedin.com/in/jiten-bhalavat/',
    'extra': 'include',
    'include_experiences': 'include',
    'include_education': 'include',
    'include_recommendations': 'include',
    'personal_contact_number': 'include',
    'personal_email': 'include',
    'inferred_salary': 'include',
    'skills': 'include',
    'use_cache': 'if-present',
    'fallback_to_cache': 'on-error',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)
linkedin_agent = Agent(
    name="Linkedin Scrapper AI Agent",
    role="Provides the Necessary Information from Resposne",
    # model=Groq(id="llama-3.3-70b-versatile", api_key=userdata.get('GROQ_API_KEY')),
    instructions=[f"Your task is to provide me the necessary and important details from {response.json()}."],
    model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
    markdown=True
)
personal_agent=Agent(
    team=[ general_agent, linkedin_agent , github_agent , medium_agent ],
    instructions=["""You are part of a team with specific tasks:
general_agent="Provide me all the necessary and Important information about Jiten-Bhalavat in 6-7 Sentences"
github_agent="Your task is to analyze the information and generate a clear and concise 5-6 line summary.
The summary should:
Highlight the main focus or purpose of the repositories.
Mention key technologies or frameworks used (if available).
Emphasize any unique or standout features.
Avoid overly technical jargon while still being informative."

medium_agent="Provide the Blogs Post Names for this https://infinityai.medium.com/"
linkedin_agent="Provide me Education, Experience and Top 3 Posts of Jiten-Bhalavat"

."""],
    # show_tool_calls=True,
    markdown=True,
)
run: RunResponse = personal_agent.run("Proivde in brief description about and engaging profile about Jiten Bhalavat. Start with a generic title, mention his Bachelor's and Master's Education. Highlight his skills in Python, Machine Learning, and AI. Discuss his role at Plutomen Technologies, his projects from Github, and then provide his Medium Blog posts. Conclude with his volunteer work and achievements. Keep it simple, professional, and engaging.")

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate speech with OpenAI's TTS API
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=run.content,
)
# Access the audio data from the response
audio_data = response.content  # Correct way to access binary audio data

# Play the audio using Pygame
pygame.mixer.init()
audio_stream = BytesIO(audio_data)  # Use in-memory file-like object
pygame.mixer.music.load(audio_stream)
pygame.mixer.music.play()

# Wait until playback is finished
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
