"""
Unit tests for Response Generation
"""

from backend.services.response_generation import ResponseGenerator
import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


class TestResponseGeneration(unittest.TestCase):
    """Unit tests for ResponseGenerator"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock the services
        with patch('backend.services.response_generation.ChatService'), \
                patch('backend.services.response_generation.VectorStore'):
            self.generator = ResponseGenerator()

            # Mock chat service
            self.generator.chat_service = Mock()
            self.generator.chat_service.generate = Mock(
                return_value="The breath knows what the mind refuses to see.")

            # Mock vector store
            self.generator.vector_store = Mock()
            self.generator.vector_store.search = Mock(return_value=[
                {"text": "Be present with what is.", "score": 0.9},
                {"text": "The body speaks truth.", "score": 0.8}
            ])

    def test_generate_with_question_strategy(self):
        """Test response generation with question strategy"""
        state = {
            "user_input": "stressed",
            "teaching_strategy": {
                "strategy": "question",
                "guidance": "Ask about body location"
            },
            "user_model": {},
            "extraction": {}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)
        self.assertIsInstance(result["final_response"], str)
        self.assertGreater(len(result["final_response"]), 0)

    def test_generate_with_reflect_strategy(self):
        """Test response generation with reflect strategy"""
        state = {
            "user_input": "chest tight, breath shallow",
            "teaching_strategy": {
                "strategy": "reflect",
                "guidance": "Mirror their awareness"
            },
            "user_model": {},
            "extraction": {"body_signals": ["chest: tight"]}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)
        self.generator.chat_service.generate.assert_called_once()

    def test_generate_with_teach_strategy(self):
        """Test response generation with teach strategy"""
        state = {
            "user_input": "feeling depleted again",
            "teaching_strategy": {
                "strategy": "teach",
                "guidance": "Explain the pattern"
            },
            "user_model": {
                "patterns": {
                    "loops": [
                        {
                            "name": "Monday Morning Spiral",
                            "sequence": ["tension", "depleted", "foggy"],
                            "frequency": 5
                        }
                    ]
                }
            },
            "extraction": {}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)

    def test_generate_with_challenge_strategy(self):
        """Test response generation with challenge strategy"""
        state = {
            "user_input": "stressed",
            "teaching_strategy": {
                "strategy": "challenge",
                "guidance": "Point out regression"
            },
            "user_model": {},
            "extraction": {}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)

    def test_rag_retrieval(self):
        """Test RAG wisdom retrieval"""
        contexts = self.generator._retrieve_wisdom("stressed", "reflect")

        self.assertIsInstance(contexts, list)
        self.generator.vector_store.search.assert_called_once()

    def test_rag_retrieval_failure(self):
        """Test RAG retrieval handles failures gracefully"""
        self.generator.vector_store.search = Mock(
            side_effect=Exception("Connection error"))

        contexts = self.generator._retrieve_wisdom("stressed", "reflect")

        self.assertEqual(contexts, [])

    def test_format_rag_contexts(self):
        """Test RAG context formatting"""
        contexts = [
            {"text": "First wisdom", "score": 0.9},
            {"text": "Second wisdom", "score": 0.8},
            {"text": "Third wisdom", "score": 0.7}
        ]

        formatted = self.generator._format_rag_contexts(contexts)

        self.assertIn("First wisdom", formatted)
        self.assertIn("Second wisdom", formatted)
        self.assertIn("Third wisdom", formatted)

    def test_format_rag_contexts_empty(self):
        """Test RAG context formatting with empty list"""
        formatted = self.generator._format_rag_contexts([])

        self.assertIn("No spiritual wisdom", formatted)

    def test_fallback_response_question(self):
        """Test fallback response for question strategy"""
        fallback = self.generator._get_fallback_response("question")

        self.assertEqual(fallback, "What's here right now?")

    def test_fallback_response_reflect(self):
        """Test fallback response for reflect strategy"""
        fallback = self.generator._get_fallback_response("reflect")

        self.assertEqual(fallback, "Stay with what's present.")

    def test_fallback_response_teach(self):
        """Test fallback response for teach strategy"""
        fallback = self.generator._get_fallback_response("teach")

        self.assertEqual(fallback, "Notice the pattern.")

    def test_fallback_response_challenge(self):
        """Test fallback response for challenge strategy"""
        fallback = self.generator._get_fallback_response("challenge")

        self.assertEqual(fallback, "Return to the body.")

    def test_generation_failure_uses_fallback(self):
        """Test that generation failure uses fallback response"""
        self.generator.chat_service.generate = Mock(
            side_effect=Exception("API error"))

        state = {
            "user_input": "stressed",
            "teaching_strategy": {
                "strategy": "question",
                "guidance": "Ask about body"
            },
            "user_model": {},
            "extraction": {}
        }

        result = self.generator.generate(state)

        # Should return fallback
        self.assertEqual(result["final_response"], "What's here right now?")

    def test_build_prompt_includes_user_input(self):
        """Test that prompt includes user input"""
        prompt = self.generator._build_prompt(
            strategy="reflect",
            guidance="Mirror awareness",
            user_input="chest tight",
            rag_contexts=[],
            user_model={},
            extraction={}
        )

        self.assertIn("chest tight", prompt)

    def test_build_prompt_includes_wisdom(self):
        """Test that prompt includes spiritual wisdom"""
        contexts = [{"text": "Be present", "score": 0.9}]

        prompt = self.generator._build_prompt(
            strategy="reflect",
            guidance="Mirror awareness",
            user_input="stressed",
            rag_contexts=contexts,
            user_model={},
            extraction={}
        )

        self.assertIn("Be present", prompt)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Response Generation Unit Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestResponseGeneration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(f"✓ All {result.testsRun} tests passed!")
    else:
        print(f"✗ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
