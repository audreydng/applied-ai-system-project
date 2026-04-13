# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeFinder 1.0

---

## 2. Goal / Task

This recommender suggests top songs from a small CSV catalog.
It predicts what songs are a good match for one user profile.
The profile includes preferred genre, mood, energy, and acoustic preference.
It outputs a ranked list with score reasons.

---

## 3. Data Used

The dataset currently has 18 songs.
Each song includes genre, mood, energy, tempo, valence, danceability, and acousticness.
I expanded the starter catalog to include more genres and moods.
The data is still very small and not representative of all music tastes.
It does not include listening history, skips, lyrics, language, or context.

---

## 4. Algorithm Summary

Each song starts at score 0.
If genre matches the user, it gets +2.0.
If mood matches, it gets +1.0.
Energy adds up to +2.0 based on closeness to the user target.
If the user likes acoustic songs and the track is acoustic enough, it gets +0.75.
Valence and danceability add small tie-break points.
Then songs are sorted by score and the top K are returned.

---

## 5. Observed Behavior / Biases

The model strongly rewards direct genre matches.
This can create a filter bubble where similar genres keep repeating.
High-energy songs can rank highly even when mood is a weak match.
Users with uncommon or conflicting preferences may get less satisfying results.
Because the dataset is small, one or two songs can appear often across profiles.

---

## 6. Evaluation Process

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial High-Energy Sad profile.
I inspected the top 5 songs and their reason strings for each profile.
I compared outputs to musical intuition.
I also ran a sensitivity experiment: half genre weight and double energy weight.
That experiment pushed energy-matching songs higher, even without genre match.

---

## 7. Intended Use and Non-Intended Use

Intended use:
Classroom learning and quick demos of transparent recommendation logic.
It is useful for showing how weights and features change rankings.

Non-intended use:
It should not be used for real production recommendations.
It should not be used for high-stakes decisions about people.
It should not be treated as personalized advice without user behavior data.

---

## 8. Ideas for Improvement

- Add diversity constraints so the top 5 are not all from similar genres.
- Learn weights from feedback instead of fixed hand-tuned values.
- Add context features like time of day, activity, and recent listening history.

---

## 9. Personal Reflection

My biggest learning moment was seeing how a simple weighted score can feel surprisingly realistic.
AI tools helped me move faster when drafting code and brainstorming edge cases.
I still had to double-check logic, because small AI-generated weight choices can create hidden ranking bias.
What surprised me most is that even basic rules can produce recommendations that look convincing.
If I extend this project, I want to add user feedback loops and measure diversity across recommendations.

