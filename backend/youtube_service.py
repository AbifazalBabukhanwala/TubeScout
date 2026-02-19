import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"

def search_videos(query, max_results=5):
    url = f"{BASE_URL}/search"
    params = {
        'q': query,
        'part': 'snippet',
        'type': 'video',
        'maxResults': max_results,
        'relevanceLanguage': 'en',
        'order': 'relevance',
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    videos = []
    for item in data['items']:
        video = {
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url']
        }
        videos.append(video)
    return videos

def get_video_stats(video_id):
    url = f"{BASE_URL}/videos"
    params = {
        'part': 'statistics,contentDetails',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['items']:
        item = data['items'][0]
        return {
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'comments_count': int(item['statistics'].get('commentCount', 0)),
            'duration': item['contentDetails']['duration']
        }
    return {}

def get_comments(video_id, max_comments=100):
    url = f"{BASE_URL}/commentThreads"
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'maxResults': max_comments,
        'order': 'relevance',
        'key': YOUTUBE_API_KEY
    }
    comments = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            likes = item['snippet']['topLevelComment']['snippet']['likeCount']
            comments.append({'text': comment, 'likes': likes})
    except Exception as e:
        print(f"Comments error: {e}")
    return comments