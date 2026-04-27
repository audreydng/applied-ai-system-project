"""Automated reliability checks for the music recommender.

Run this script from the repository root or the project folder:

    python scripts/reliability_check.py

It exits with a non-zero status if any check fails.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import Recommender, Song, UserProfile, load_songs, recommend_songs  # noqa: E402


def run_checks() -> int:
    """Run a small suite of deterministic checks against the recommender."""
    failures: list[str] = []

    songs = load_songs(str(PROJECT_ROOT / "data" / "songs.csv"))
    if len(songs) != 18:
        failures.append(f"expected 18 songs, got {len(songs)}")

    cases = [
        (
            "High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.88,
                "likes_acoustic": False,
            },
            "Sunrise City",
        ),
        (
            "Chill Lofi",
            {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "likes_acoustic": True,
            },
            "Library Rain",
        ),
        (
            "Deep Intense Rock",
            {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.92,
                "likes_acoustic": False,
            },
            "Storm Runner",
        ),
    ]

    for profile_name, prefs, expected_title in cases:
        recommendations = recommend_songs(prefs, songs, k=1)
        if not recommendations:
            failures.append(f"{profile_name}: no recommendations returned")
            continue
        actual_title = recommendations[0][0]["title"]
        if actual_title != expected_title:
            failures.append(
                f"{profile_name}: expected top song {expected_title}, got {actual_title}"
            )

    sample_recommender = Recommender(
        [
            Song(1, "Test Pop Track", "Test Artist", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
            Song(2, "Chill Lofi Loop", "Test Artist", "lofi", "chill", 0.4, 80, 0.6, 0.5, 0.9),
        ]
    )
    user = UserProfile("pop", "happy", 0.8, False)
    explanation = sample_recommender.explain_recommendation(user, sample_recommender.songs[0])
    if not isinstance(explanation, str) or not explanation.strip():
        failures.append("explanation should be a non-empty string")

    if failures:
        print("Reliability check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Reliability check passed: 5 out of 5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_checks())