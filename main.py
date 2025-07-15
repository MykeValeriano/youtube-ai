from agents.summary_agent import generate_summary
from agents.notes_agent import generate_notes

youtube = "https://www.youtube.com/watch?v=xauVFOBEX7Y"

summary = generate_summary(youtube)
notes = generate_notes(youtube)

print("summary:\n", summary)
print("notes:\n", notes)