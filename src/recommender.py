import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by profile match score."""
        user_prefs: Dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        ranked: List[Tuple[Song, float]] = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
                "valence": song.valence,
                "danceability": song.danceability,
            }
            score, _ = score_song(user_prefs, song_dict)
            ranked.append((song, score))

        ranked.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for a song score."""
        user_prefs: Dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
            "valence": song.valence,
            "danceability": song.danceability,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "No matching signals from current profile."


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    score = 0.0
    reasons: List[str] = []

    favorite_genre = str(user_prefs.get("genre", "")).strip().lower()
    favorite_mood = str(user_prefs.get("mood", "")).strip().lower()
    target_energy = float(user_prefs.get("energy", 0.5))

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = float(song.get("energy", 0.5))
    song_acousticness = float(song.get("acousticness", 0.0))
    song_valence = float(song.get("valence", 0.0))
    song_danceability = float(song.get("danceability", 0.0))

    weights = user_prefs.get("weights", {}) if isinstance(user_prefs.get("weights", {}), dict) else {}
    genre_weight = float(weights.get("genre", 2.0))
    mood_weight = float(weights.get("mood", 1.0))
    energy_weight = float(weights.get("energy", 2.0))
    valence_weight = float(weights.get("valence", 0.35))
    dance_weight = float(weights.get("danceability", 0.20))
    acoustic_bonus = float(weights.get("acoustic_bonus", 0.75))

    if favorite_genre and song_genre == favorite_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.2f})")

    if favorite_mood and song_mood == favorite_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.2f})")

    energy_similarity = max(0.0, 1.0 - abs(song_energy - target_energy))
    energy_points = energy_weight * energy_similarity
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is True and song_acousticness >= 0.60:
        score += acoustic_bonus
        reasons.append(f"acoustic preference match (+{acoustic_bonus:.2f})")

    valence_points = valence_weight * song_valence
    score += valence_points
    reasons.append(f"valence tie-break (+{valence_points:.2f})")

    dance_points = dance_weight * song_danceability
    score += dance_points
    reasons.append(f"danceability tie-break (+{dance_points:.2f})")

    return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV with numeric fields converted for scoring."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs using score_song and return top-k with explanations."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
