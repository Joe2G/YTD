from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pytube import YouTube
from pydantic import BaseModel

app = FastAPI()

# CORS configuration to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    type: str

@app.post('/download')
async def download_video_or_audio(request: DownloadRequest):
    try:
        url = request.url
        type = request.type

        if type not in ['video', 'audio']:
            raise HTTPException(status_code=400, detail="Invalid 'type'. Use 'video' or 'audio'.")

        if type == 'video':
            video_file_path = download_video(url)
            return {'message': 'Video download complete!', 'file_path': video_file_path}
        elif type == 'audio':
            video_file_path, audio_file_path = download_audio(url)
            return {'message': 'Video and audio download complete!', 'video_file_path': video_file_path, 'audio_file_path': audio_file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_video(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    video_file_path = f"videos/{yt.title}.mp4"
    video_stream.download(output_path="videos", filename=yt.title + ".mp4")
    return video_file_path

def download_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = f"audios/{yt.title}.mp3"
    audio_stream.download(output_path="audios", filename=yt.title + ".mp3")
    return f"videos/{yt.title}.mp4", audio_file_path
