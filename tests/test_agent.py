import unittest
from milestone2_agent import answer_question


class TestAgent(unittest.TestCase):

    def test_known_question(self):
        answer = answer_question("What is the refund policy?")
        self.assertIn("7 days", answer)

    def test_unknown_question(self):
        answer = answer_question(
            "What is the company's office address?"
        )
        self.assertIn("don't have enough information", answer)

    def test_repeated_question(self):
        question = "What is the refund policy?"
        first = answer_question(question)
        second = answer_question(question)
        self.assertEqual(first, second)

    def test_empty_question(self):
        self.assertEqual(
            answer_question(""),
            "Please enter a question."
        )


if __name__ == "__main__":
    unittest.main()
