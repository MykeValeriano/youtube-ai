import os
import json
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def generate_summary(source: str, output_file: str = "public/summary.json") -> str:
    """
    Generate a summary from a YouTube URL or transcript and save it to a JSON file.

    Args:
        source: A YouTube URL or a plain transcript string
        output_file: The file path to save the summary JSON

    Returns:
        The generated summary as a string
    """
    # Get transcript from YouTube or use input string
    if source.startswith("http"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    prompt = (
        "Summarize the following transcript into a clear, concise, informative summary "
        "covering key points and ideas:\n\n"
        f"{transcript}"
    )
    response = model.generate_content(prompt)
    summary = response.text.strip()

    # Save summary to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"summary": summary}, f, ensure_ascii=False, indent=2)

    return summary
