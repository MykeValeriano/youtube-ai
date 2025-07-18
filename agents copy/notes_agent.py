import os
import json
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key="AIzaSyBcRtLFcwuHt2cMN_1Qf9G0xn48w1usn4Y")
model = genai.GenerativeModel("gemini-2.5-pro")

def generate_notes(source: str, output_file: str = "public/notes.json") -> str:
    """
    Generating notes from source video
    """
    if source.startswith("http"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    prompt = (
        "Extract the key points and main ideas from the following transcript. "
        "Present the notes as a clear, well-structured, and easy-to-read bullet list. "
        "Group related ideas together, use concise language, and highlight important facts or events. "
        "Use Markdown formatting for the bullet points.\n\n"
        f"{transcript}"
    )

    response = model.generate_content(prompt)
    notes = response.text.strip()
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)
    return notes
