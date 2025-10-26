"""
recommender_engine.py
Fully functional KOKO recommender engine with learning feedback.
- Uses child profiles stored in profiles.json
- Maps detected emotions to actions
- Adjusts recommendation scores based on feedback (before vs after emotion)
"""

import json
from pathlib import Path
import random

PROFILE_PATH = Path("profiles.json")

# Default child profiles
DEFAULT_PROFILES = {
    "child_001": {
        "name": "Arya",
        "age": 9,
        "prefs": {"music": True, "videos": True, "movement": True},
        "fav_music": ["soft_piano.mp3"],
        "fav_videos": ["cartoon_clip_1.mp4"],
        "movement_pref": "gentle_spin",
        "rec_scores": {}  # dynamic learning scores
    }
}

# Base emotion -> candidate actions
BASE_MAPPING = {
    "happy": ["dance_move", "reward_learning", "celebrate"],
    "sad": ["play_cheer_music", "gentle_forward", "comfort_video"],
    "angry": ["calm_breathing", "slow_back", "blink_alert"],
    "neutral": ["idle_patrol", "interactive_prompt", "music_snippet"],
    "surprise": ["quick_spin", "show_surprised_eyes"],
    "fear": ["retreat_slow", "soothing_audio", "parent_notify"]
}

# Assets mapped to action keys
ASSETS = {
    "play_cheer_music": ["cheer1.mp3"],
    "gentle_forward": ["gentle_forward"],
    "comfort_video": ["comfort_clip.mp4"],
    "calm_breathing": ["breath_audio.mp3"],
    "slow_back": ["slow_back"],
    "idle_patrol": ["patrol_pattern"],
    "interactive_prompt": ["ask_question_audio.mp3"],
    "music_snippet": ["jingle1.mp3"],
    "dance_move": ["dance_pattern"],
    "reward_learning": ["reward_game"],
    "celebrate": ["celebrate_pattern"],
    "quick_spin": ["quick_spin"],
    "show_surprised_eyes": ["surprise_eyes"],
    "retreat_slow": ["retreat_motion"],
    "soothing_audio": ["sooth.mp3"],
    "parent_notify": ["notify_parent"]
}

# Emotion valence for feedback learning
VALENCE = {"happy": 2, "surprise": 1, "neutral": 0, "sad": -1, "fear": -2, "angry": -2}

# ---------------- Profile Management ----------------

def load_profiles():
    """Load child profiles; create default if not present or corrupted."""
    if PROFILE_PATH.exists():
        try:
            return json.loads(PROFILE_PATH.read_text())
        except Exception:
            print("[Recommender] Could not load profiles.json; creating default.")
    PROFILE_PATH.write_text(json.dumps(DEFAULT_PROFILES, indent=2))
    return DEFAULT_PROFILES.copy()

def save_profiles(profiles):
    """Persist profiles.json"""
    PROFILE_PATH.write_text(json.dumps(profiles, indent=2))

# ---------------- Recommendation Engine ----------------

def recommend_for_child(profile, emotion, top_k=1):
    """
    Returns the top_k recommended action keys for a child given the detected emotion.
    Scoring = base + preference bonus + learned feedback
    """
    candidates = BASE_MAPPING.get(emotion, BASE_MAPPING["neutral"])[:]
    scored = []

    for c in candidates:
        base = 1.0
        pref_bonus = 0.0
        # Preference bonus heuristics
        if "music" in c or "cheer" in c or "soothing" in c:
            if profile["prefs"].get("music"):
                pref_bonus += 0.7
        if "video" in c or "comfort" in c:
            if profile["prefs"].get("videos"):
                pref_bonus += 0.7
        if "forward" in c or "spin" in c or "move" in c or "retreat" in c:
            if profile["prefs"].get("movement"):
                pref_bonus += 0.7

        # Learned feedback score
        learned = profile.get("rec_scores", {}).get(c, 0.0)
        score = base + pref_bonus + learned
        scored.append((c, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    picks = [c for c, _ in scored[:top_k]]
    return picks

# ---------------- Feedback Learning ----------------

def apply_feedback(profile, recommendation, before_emotion, after_emotion):
    """
    Adjust recommendation scores based on emotion change.
    delta > 0: emotion improved -> +1
    delta = 0: neutral -> +0.1
    delta < 0: emotion worsened -> -0.5
    Scores are clamped between -3 and 5.
    """
    delta_val = VALENCE.get(after_emotion, 0) - VALENCE.get(before_emotion, 0)
    if delta_val > 0:
        change = 1.0
    elif delta_val == 0:
        change = 0.1
    else:
        change = -0.5

    rec_scores = profile.setdefault("rec_scores", {})
    rec_scores[recommendation] = max(-3.0, min(5.0, rec_scores.get(recommendation, 0.0) + change))
    return change

# ---------------- Convenience ----------------

def get_assets(action_key):
    """Return the list of asset names for an action key"""
    return ASSETS.get(action_key, [action_key])
