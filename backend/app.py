import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from youtube_service import search_videos, get_video_stats, get_comments
from ai_service import analyze_comments
from scoring import rank_videos

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Step 1: Search YouTube
        videos = search_videos(query, max_results=5)
        
        results = []
        for video in videos:
            video_id = video['video_id']
            
            # Step 2: Get stats
            stats = get_video_stats(video_id)
            
            # Step 3: Get comments
            comments = get_comments(video_id, max_comments=50)
            
            # Step 4: AI analysis
            ai_analysis = analyze_comments(comments, video['title'])
            
            results.append({
                'video_id': video_id,
                'title': video['title'],
                'channel': video['channel'],
                'thumbnail': video['thumbnail'],
                'description': video['description'],
                'stats': stats,
                'ai_analysis': ai_analysis,
                'url': f'https://www.youtube.com/watch?v={video_id}'
            })
        
        # Step 5: Rank videos
        ranked = rank_videos(results)
        
        return jsonify({'results': ranked})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)