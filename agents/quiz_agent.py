import os
import json
import re
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def generate_quiz(source: str, count: int = 5, output_file: str = "quiz.json") -> list:
    """
    Generate an English quiz based on a YouTube URL or transcript, save to JSON file, and return quiz data.

    Args:
        source: YouTube URL or transcript string
        count: Number of questions to generate
        output_file: JSON file path to save quiz

    Returns:
        List of quiz questions (dicts)
    """

    # Get transcript
    if source.startswith("http"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    # Prompt Gemini to generate quiz ONLY in English, JSON format
    prompt = (
        f"Create a quiz of {count} questions based on the transcript below.\n"
        "Please write ALL questions, options, and answers in ENGLISH only.\n\n"
        "Use ONLY JSON format as a list of questions, like this:\n"
        "[\n"
        "  {\n"
        "    \"type\": \"open|multiple|yesno\",\n"
        "    \"question\": \"...\",\n"
        "    \"options\": [\"opt1\", \"opt2\"],   # only for multiple choice\n"
        "    \"answer\": \"...\"\n"
        "  },\n"
        "  ...\n"
        "]\n\n"
        f"Transcript:\n{transcript}"
    )

    # Generate content
    response = model.generate_content(prompt)

    # Debug output
    print("Gemini raw response:")
    print(response.text)

    # Extract JSON safely
    def extract_json(text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\[\s*{.*}\s*\]", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        return []

    quiz_data = extract_json(response.text)

    # Save quiz to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"quiz": quiz_data}, f, ensure_ascii=False, indent=2)

    return quiz_data
