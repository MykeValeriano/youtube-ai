import os
import json
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def generate_notes(source: str, output_file: str = "public/notes.json") -> str:
    """
    Generates detailed notes from a YouTube video or transcript using prompt engineering
    and saves them to a JSON file.

    Args:
        source: YouTube URL or transcript text
        output_file: Path to save notes JSON

    Returns:
        Notes string
    """
    if source.startswith("http"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source


    prompt = (
        """Extract Key bullet points from the following transcript."
        "Each bullet should reflect the main topics, important ideas and events."
        "Group similar ideas together and make it concise and easy to understand:\n\n"""
        f"{transcript}"
    )

    response = model.generate_content(prompt)
    notes = response.text.strip()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)

    return notes
