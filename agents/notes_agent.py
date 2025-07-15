import os
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key="AIzaSyB7jhfPmylkTapJ77nYiNlEP8VAYCJd7Es")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_notes(source: str) -> str:
    """
    Generating notes from source video
    """
    if source.startswith("https"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    prompt = (
        "Extract Key bullet points from the following transcript."
        "Each bullet should reflect the main topics, important ideas and events."
        "Group similar ideas together and make it concise and easy to understand:\n\n"
        f"{transcript}"
    )

    response = model.generate_content(prompt)
    return response.text.strip()
