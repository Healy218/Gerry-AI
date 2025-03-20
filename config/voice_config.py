# Voice IDs for different bots
VOICE_IDS = {
    "WSB": "1fwHxg7vyqil11CYGuag",  # WSB voice
    "BG3": "viyyLJOwpZc4bofwHde1",  # Baldur's Gate 3 voice
    "CLAUDE": "your_claude_voice_id_here",  # Claude voice
    "DEEPSEEK": "your_deepseek_voice_id_here",  # DeepSeek voice
    "GERRY": "UZAh1WD3AhxDclPcWvsX",  # Gerry AI voice
    "DEFAULT": "FGY2WhTYpPnrIDTdsKH5"  # Default to ElevenLabs Laura voice 
}

# Voice settings for different personalities
VOICE_SETTINGS = {
    "WSB": {
        "speed": 1.2,
        "stability": 0.4,
        "similarity_boost": 0.5,
        "style": 0.58,
        "use_speaker_boost": True
    },
    "BG3": {
        "speed": .91,
        "stability": 0.13,
        "similarity_boost": 0.85,
        "style": 0.99,
        "use_speaker_boost": True
    },
    "CLAUDE": {
        "stability": 0.6,
        "similarity_boost": 0.6,
        "style": 0.4,
        "use_speaker_boost": True
    },
    "DEEPSEEK": {
        "stability": 0.5,
        "similarity_boost": 0.5,
        "style": 0.5,
        "use_speaker_boost": True
    },
    "GERRY": {
        "speed": 1,
        "stability": 0.5,
        "similarity_boost": 0.5,
        "style": 0.5,
        "use_speaker_boost": True
    },
    "DEFAULT": {
        "speed": .85,
        "stability": 0.3,
        "similarity_boost": 0.7,
        "style": 0.91,
        "use_speaker_boost": True
    }
} 