# Personal-AI-Agent

## 🚨📄 Problem Statement
This project aims to create a personal AI agent that provides a comprehensive overview of myself—skills, education, projects, experience, and more—by fetching data from various sources like GitHub, LinkedIn, Medium, and the internet. Instead of sharing my resume, the AI agent can instantly provide detailed information on demand.

## ✨ Key Features
1. GitHub Agent: Retrieves the latest repositories and projects from your GitHub profile.
2. LinkedIn Agent: Provides basic information such as education, projects, experience, and volunteer activities from your LinkedIn profile.
3. Medium Agent: Uses Firecrawl tools to fetch the top blog posts related to your Medium account.
4. General Information Agent: This agent searches the Internet using DuckDuckGo to gather additional details about you from various sources.
5. Personal Agent: Integrates all the information fetched from the above agents to provide a unified response about myself.
6. OpenAI TTS (Text-to-Speech): This method converts the fetched information into speech using OpenAI's Text-to-Speech model for an interactive experience.

## 🛠️ Technologies Used
1. OpenAI LLM Model: For text-based interactions and responses.
2. GitHub Token: To fetch repository data.
3. Scrapin.io API: To retrieve professional data such as experience, education, projects, and volunteer activities from LinkedIn.
4. Firecrawl Tools: For gathering blog posts from Medium.
5. DuckDuckGo API: For retrieving general information from the web.
6. OpenAI TTS Model: To convert text into speech for audio responses.

## Installation
1. **Clone the repository** :
   ```bash
    https://github.com/Jiten-Bhalavat/Personal-AI-Agent.git
    cd personal-ai-agent

2. **Install the required dependencies**:
   ```bash
    pip install -r requirements.txt

3. **Set up the necessary API keys for GitHub, LinkedIn (Scrapin), FireCrawl, and OpenAI**:              
Set up environment variables or configuration files with the keys.

4. **Run the agent**:
    ```bash
    python main.py
