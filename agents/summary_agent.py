import os
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_summary(source: str) -> str:
    """
    Generating summary from Youtube Video
    """
    if source.startswith("https"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    prompt = f"summarize the following transcript, make it concise and easy to understand:\n\n{transcript}"
    response = model.generate_content(prompt)
    return response.text.strip()
