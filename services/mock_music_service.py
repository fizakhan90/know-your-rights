from typing import List, Dict
import random

class MockMusicService:
    def __init__(self):
        self.music_database = {
            "Anxious": [
                {"title": "Weightless", "artist": "Marconi Union", "therapeutic_score": 0.95},
                {"title": "Breathe", "artist": "Pink Floyd", "therapeutic_score": 0.89},
                {"title": "Claire de Lune", "artist": "Claude Debussy", "therapeutic_score": 0.92}
            ],
            "Stressed": [
                {"title": "River Flows in You", "artist": "Yiruma", "therapeutic_score": 0.91},
                {"title": "Gymnopédie No.1", "artist": "Erik Satie", "therapeutic_score": 0.88},
                {"title": "Meditation", "artist": "Jules Massenet", "therapeutic_score": 0.90}
            ],
            "Sad": [
                {"title": "Here Comes the Sun", "artist": "The Beatles", "therapeutic_score": 0.93},
                {"title": "Three Little Birds", "artist": "Bob Marley", "therapeutic_score": 0.87},
                {"title": "What a Wonderful World", "artist": "Louis Armstrong", "therapeutic_score": 0.89}
            ],
            "Calm": [
                {"title": "Moon River", "artist": "Henry Mancini", "therapeutic_score": 0.86},
                {"title": "The Girl from Ipanema", "artist": "Stan Getz", "therapeutic_score": 0.85},
                {"title": "Fly Me to the Moon", "artist": "Frank Sinatra", "therapeutic_score": 0.88}
            ],
            "Happy": [
                {"title": "Walking on Sunshine", "artist": "Katrina & The Waves", "therapeutic_score": 0.92},
                {"title": "Good Vibrations", "artist": "The Beach Boys", "therapeutic_score": 0.90},
                {"title": "Dancing Queen", "artist": "ABBA", "therapeutic_score": 0.89}
            ],
            "Energetic": [
                {"title": "Eye of the Tiger", "artist": "Survivor", "therapeutic_score": 0.94},
                {"title": "Don't Stop Believin'", "artist": "Journey", "therapeutic_score": 0.91},
                {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "therapeutic_score": 0.93}
            ]
        }

    def get_therapeutic_music(self, mood: str, activity: str, goals: List[str]) -> List[Dict]:
        """Get music recommendations based on mood"""
        if mood in self.music_database:
            
            recommendations = self.music_database[mood].copy()
            
            
            for song in recommendations:
                activity_bonus = random.uniform(0.01, 0.05)
                goals_bonus = random.uniform(0.01, 0.05) * len(goals)
                song['therapeutic_score'] = min(0.99, song['therapeutic_score'] + activity_bonus + goals_bonus)
            
        
            recommendations.sort(key=lambda x: x['therapeutic_score'], reverse=True)
            return recommendations[:5]
        return []