from agent_utilities import AgentManager
from openai import OpenAI
import pygame
from io import BytesIO

def main():
    """
    Main function to demonstrate the functionality of the personal agent and convert its output to speech.
    """
    # Initialize the Agent Manager
    agent_manager = AgentManager()

    # Create the personal agent
    personal_agent = agent_manager.create_personal_agent()

    # Run the personal agent
    print("\n--- Personal Agent Output ---")
    personal_output = personal_agent.run("Proivde in brief description about and engaging profile about Jiten Bhalavat. Start with a generic title, mention his Bachelor's and Master's Education. Highlight his skills in Python, Machine Learning, and AI. Discuss his role at Plutomen Technologies, his projects from Github, and then provide his Medium Blog posts. Conclude with his volunteer work and achievements. Keep it simple, professional, and engaging.")
    personal_content = personal_output.content

    # Initialize the OpenAI client
    client = OpenAI(api_key=agent_manager.config.get_api_key("OPENAI_API_KEY"))

    # Generate speech with OpenAI's TTS API
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=personal_content,
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

if __name__ == "__main__":
    main()
