"""
Unit tests for the EmotionDetection package.
"""

import unittest
from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """
    Test cases for emotion_detector.
    """

    def test_emotion_detector(self):
        """
        Test dominant emotions for sample statements.
        """
        self.assertEqual(
            emotion_detector("I am glad this happened")["dominant_emotion"],
            "joy",
        )
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"],
            "anger",
        )
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")[
                "dominant_emotion"
            ],
            "disgust",
        )
        self.assertEqual(
            emotion_detector("I am so sad about what happened")[
                "dominant_emotion"
            ],
            "sadness",
        )
        self.assertEqual(
            emotion_detector("I am afraid that something bad will happen")[
                "dominant_emotion"
            ],
            "fear",
        )


if __name__ == "__main__":
    unittest.main()