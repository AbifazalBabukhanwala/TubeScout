import math

def calculate_score(video_stats, ai_analysis):
    score = 0
    
    # View score (max 25 points)
    views = video_stats.get('views', 0)
    if views > 0:
        view_score = min(25, math.log10(views) * 5)
        score += view_score
    
    # Like ratio score (max 25 points)
    views = video_stats.get('views', 0)
    likes = video_stats.get('likes', 0)
    if views > 0:
        like_ratio = likes / views
        score += min(25, like_ratio * 1000)
    
    # Sentiment score (max 20 points)
    sentiment = ai_analysis.get('sentiment', 'unknown')
    if sentiment == 'positive':
        score += 20
    elif sentiment == 'mixed':
        score += 10
    
    # Exam ready bonus (15 points)
    if ai_analysis.get('exam_ready', False):
        score += 15
    
    # Comment engagement score (max 15 points)
    comments_count = video_stats.get('comments_count', 0)
    if comments_count > 0:
        comment_score = min(15, math.log10(comments_count) * 5)
        score += comment_score
    
    return round(score, 1)

def rank_videos(videos_data):
    for video in videos_data:
        video['score'] = calculate_score(
            video.get('stats', {}),
            video.get('ai_analysis', {})
        )
    
    return sorted(videos_data, key=lambda x: x['score'], reverse=True)