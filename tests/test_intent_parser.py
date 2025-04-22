import unittest
from src.SoulSpeak.nlu.intent_parser import get_intent

class TestIntentParser(unittest.TestCase):
    def test_new_entry_intent(self):
        self.assertEqual(get_intent("I'd like to write something down"), "new_entry")
        self.assertEqual(get_intent("Can I journal today?"), "new_entry")

    def test_view_memories_intent(self):
        self.assertEqual(get_intent("Show me my past memories"), "view_memories")
        self.assertEqual(get_intent("Can I see recent entries?"), "view_memories")

    def test_check_trend_intent(self):
        self.assertEqual(get_intent("What emotional patterns are showing?"), "check_trend")
        self.assertEqual(get_intent("Give me a trend update"), "check_trend")

    def test_summarize_archive_intent(self):
        self.assertEqual(get_intent("Summarize my archive"), "summarize_archive")
        self.assertEqual(get_intent("Give me a full summary of past logs"), "summarize_archive")

    def test_archive_intent(self):
        self.assertEqual(get_intent("Please archive my older memories"), "archive")
        self.assertEqual(get_intent("Store everything older than last week"), "archive")

    def test_exit_intent(self):
        self.assertEqual(get_intent("Exit"), "exit")
        self.assertEqual(get_intent("Goodbye for now"), "exit")

    def test_unknown_intent(self):
        self.assertEqual(get_intent("Do you believe in dreams?"), "unknown")
        self.assertEqual(get_intent("What’s the meaning of life?"), "unknown")

if __name__ == '__main__':
    unittest.main()