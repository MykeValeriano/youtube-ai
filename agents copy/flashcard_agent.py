import os
import json
import google.generativeai as genai
from utils.youtube_agent import get_transcript_from_youtube

genai.configure(api_key="AIzaSyBcRtLFcwuHt2cMN_1Qf9G0xn48w1usn4Y")
model = genai.GenerativeModel("gemini-2.5-pro")

def generate_flashcards(source: str, count: int = 10, output_file: str = "public/flashcards.json") -> list:
    """
    Generate flashcards using definitions as questions and concepts as answers.
    Saves the flashcards in JSON format.

    Args:
        source: YouTube URL or plain transcript text
        count: Number of flashcards to generate
        output_file: Path to save flashcards JSON

    Returns:
        A list of flashcard dictionaries: [{"question": ..., "answer": ...}, ...]
    """
    # Get transcript from URL or direct text
    if source.startswith("http"):
        transcript = get_transcript_from_youtube(source)
    else:
        transcript = source

    # Prompt Gemini with definition-as-question structure
    prompt = (
        f"Generate {count} flashcards from the transcript below.\n\n"
        "Each flashcard should follow this structure:\n"
        "Flashcard 1:\n"
        "Q: [A definition or description of a concept from the transcript]\n"
        "A: [The name of the concept being described]\n\n"
        "Examples:\n"
        "Q: A high-level, interpreted programming language known for readability and ease of use.\n"
        "A: Python\n\n"
        "Q: The process of finding and fixing errors in code.\n"
        "A: Debugging\n\n"
        "Only include key topics, definitions, or facts. Avoid trivia.\n\n"
        f"{transcript}"
    )

    # Generate response
    response = model.generate_content(prompt)
    raw_output = response.text.strip()

    # Parse the response into flashcards
    flashcards = []
    for block in raw_output.split("Flashcard ")[1:]:
        try:
            _, content = block.split(":", 1)
            q_line = next(line for line in content.splitlines() if line.startswith("Q:"))
            a_line = next(line for line in content.splitlines() if line.startswith("A:"))
            question = q_line[2:].strip()
            answer = a_line[2:].strip()
            flashcards.append({"question": question, "answer": answer})
        except Exception:
            continue  # Skip any malformed blocks
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"flashcards": flashcards}, f, ensure_ascii=False, indent=2)
    return flashcards