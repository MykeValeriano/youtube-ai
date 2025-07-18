from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
import re

def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL.
    """
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def get_transcript_from_youtube(url: str) -> str:
    """
    Retrieves the transcript of a YouTube video in English if available,
    or falls back to the first available language.
    """
    video_id = extract_video_id(url)
    formatter = TextFormatter()

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except (NoTranscriptFound, TranscriptsDisabled):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_obj = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )
            transcript = transcript_obj.fetch()
        except Exception as e:
            raise RuntimeError(f"Transcript not available in any language: {e}")
    return "\n".join(item["text"] if isinstance(item, dict) else item.text for item in transcript)
