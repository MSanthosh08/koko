"""
recommender_engine.py
Simple emotion -> action mapping + lightweight personalization (profile JSON).
Stores learned scores in profiles.json and exposes recommend_for_child()
"""

import json
from pathlib import Path

PROFILE_PATH = Path("profiles.json")

DEFAULT_PROFILES = {
    "child_001": {
        "name": "Arya",
        "age": 9,
        "prefs": {"music": True, "videos": True, "movement": True},
        "fav_music": ["soft_piano.mp3"],
        "fav_videos": ["cartoon_clip_1.mp4"],
        "movement_pref": "gentle_spin",
        "rec_scores": {}
    }
}

BASE_MAPPING = {
    "happy": ["dance_move", "reward_learning", "celebrate"],
    "sad": ["play_cheer_music", "gentle_forward", "comfort_video"],
    "angry": ["calm_breathing", "slow_back", "blink_alert"],
    "neutral": ["idle_patrol", "interactive_prompt", "music_snippet"],
    "surprise": ["quick_spin", "show_surprised_eyes"],
    "fear": ["retreat_slow", "soothing_audio", "parent_notify"]
}

ASSETS = {
    # mapping to asset names or animation/action keys
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

def load_profiles():
    if PROFILE_PATH.exists():
        try:
            return json.loads(PROFILE_PATH.read_text())
        except Exception:
            print("[Recommender] Could not load profiles.json; creating default.")
    PROFILE_PATH.write_text(json.dumps(DEFAULT_PROFILES, indent=2))
    return DEFAULT_PROFILES.copy()

def save_profiles(profiles):
    PROFILE_PATH.write_text(json.dumps(profiles, indent=2))

def recommend_for_child(profile, emotion, top_k=1):
    """
    profile: profile dict for the child
    emotion: detected emotion string
    returns: list of recommendation keys (top_k)
    """
    candidates = BASE_MAPPING.get(emotion, BASE_MAPPING["neutral"])[:]
    # score by preference + learned rec_scores
    scored = []
    for c in candidates:
        base = 1.0
        pref_bonus = 0.0
        # heuristic: if action involves music/video/movement and child likes it
        if "music" in c or "cheer" in c or "soothing" in c:
            if profile["prefs"].get("music"):
                pref_bonus += 0.7
        if "video" in c or "comfort" in c:
            if profile["prefs"].get("videos"):
                pref_bonus += 0.7
        if "forward" in c or "spin" in c or "move" in c or "retreat" in c:
            if profile["prefs"].get("movement"):
                pref_bonus += 0.7
        learned = profile.get("rec_scores", {}).get(c, 0.0)
        score = base + pref_bonus + learned
        scored.append((c, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    picks = [c for c, _ in scored[:top_k]]
    # return picks and their asset choices as convenience
    return picks

def apply_feedback(profile, recommendation, before_emotion, after_emotion):
    """
    Simple reward shaping: if after_emotion valence improved -> +1; else -0.5
    """
    valence = {"happy": 2, "surprise": 1, "neutral": 0, "sad": -1, "fear": -2, "angry": -2}
    delta = valence.get(after_emotion, 0) - valence.get(before_emotion, 0)
    if delta > 0:
        change = 1.0
    elif delta == 0:
        change = 0.1
    else:
        change = -0.5
    rec_scores = profile.setdefault("rec_scores", {})
    rec_scores[recommendation] = max(-3.0, min(5.0, rec_scores.get(recommendation, 0.0) + change))
    return change
