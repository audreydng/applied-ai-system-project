"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_profile_results(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for one named user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n=== {profile_name} ===")
    print(
        f"genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']:.2f}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    if "weights" in user_prefs:
        print(f"weights={user_prefs['weights']}")
    print("-" * 72)
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{idx}. {song['title']} by {song['artist']}")
        print(f"   Score   : {score:.2f}")
        print(f"   Reasons : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.88,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "likes_acoustic": False,
        },
        "Adversarial: High-Energy Sad": {
            "genre": "ambient",
            "mood": "sad",
            "energy": 0.90,
            "likes_acoustic": True,
        },
    }

    print("\nBASELINE RECOMMENDATIONS")
    for profile_name, prefs in profiles.items():
        print_profile_results(profile_name, prefs, songs, k=5)

    print("\nSENSITIVITY EXPERIMENT")
    print("Change: half genre weight and double energy weight for High-Energy Pop")
    experimental = dict(profiles["High-Energy Pop"])
    experimental["weights"] = {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 4.0,
        "valence": 0.35,
        "danceability": 0.20,
        "acoustic_bonus": 0.75,
    }
    print_profile_results("High-Energy Pop (Experiment)", experimental, songs, k=5)


if __name__ == "__main__":
    main()
