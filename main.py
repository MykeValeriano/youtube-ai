from agents.summary_agent import generate_summary
from agents.notes_agent import generate_notes
from agents.flashcard_agent import generate_flashcards
from agents.quiz_agent import generate_quiz

youtube = "https://www.youtube.com/watch?v=KDkxbL2Itqg"

summary = generate_summary(youtube)
notes = generate_notes(youtube)
cards = generate_flashcards(youtube, count=8, output_file="public/flashcards.json")
quiz = generate_quiz(source=youtube, count=5, output_file="public/quiz.json")

print("summary:\n", summary)
print("notes:\n", notes)
