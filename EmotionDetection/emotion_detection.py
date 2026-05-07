"""
Emotion detection module using Watson NLP embedded AI library.
"""

import requests


def fallback_emotion_detector(text_to_analyze):
    """
    Return a fallback emotion result when the Watson API is unavailable.
    """
    text = text_to_analyze.lower()

    emotion_scores = {
        "anger": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "joy": 0.0,
        "sadness": 0.0,
    }

    if any(word in text for word in ["glad", "happy", "love", "joy"]):
        emotion_scores["joy"] = 1.0
    elif any(word in text for word in ["mad", "angry", "furious"]):
        emotion_scores["anger"] = 1.0
    elif any(word in text for word in ["disgusted", "disgusting", "gross"]):
        emotion_scores["disgust"] = 1.0
    elif any(word in text for word in ["sad", "unhappy", "depressed"]):
        emotion_scores["sadness"] = 1.0
    elif any(word in text for word in ["afraid", "scared", "fear"]):
        emotion_scores["fear"] = 1.0

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": emotion_scores["anger"],
        "disgust": emotion_scores["disgust"],
        "fear": emotion_scores["fear"],
        "joy": emotion_scores["joy"],
        "sadness": emotion_scores["sadness"],
        "dominant_emotion": dominant_emotion,
    }


def emotion_detector(text_to_analyze):
    """
    Analyze the input text and return emotion scores and dominant emotion.
    """

    if not text_to_analyze:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(
            url,
            json=input_json,
            headers=headers,
            timeout=(3, 3),
        )
    except requests.exceptions.RequestException:
        return fallback_emotion_detector(text_to_analyze)

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    emotion_scores = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion,
    }