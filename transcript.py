from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):

    if "v=" in url:
        return url.split("v=")[1].split("&")[0]

    if "youtu.be" in url:
        return url.split("/")[-1]

    return None


def fetch_transcript(url):

    video_id = get_video_id(url)

    if not video_id:
        return "Invalid YouTube URL"

    try:
        # fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])

        text = " ".join([item["text"] for item in transcript])

        return text

    except Exception as e:
        print("Transcript error:", e)
        return "Transcript not available for this video."
