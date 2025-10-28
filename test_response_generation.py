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
            return_value="Test response")

        # Mock vector store
        self.generator.vector_store = Mock()
        self.generator.vector_store.search = Mock(return_value=[
            {"text": "Teaching 1", "score": 0.9},
            {"text": "Teaching 2", "score": 0.8},
            {"text": "Teaching 3", "score": 0.7}
        ])

    def test_generate_question_strategy(self):
        """Test response generation with question strategy"""
        state = {
            "user_input": "stressed",
            "teaching_strategy": {
                "strategy": "question",
                "guidance": "Ask about body location"
            },
            "extraction": {"body_signals": []},
            "user_model": {}
        }

        result = self.generator.generate(state)

        # Should have response and RAG contexts
        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)

        # Chat service should be called
        self.generator.chat_service.generate.assert_called()

        # Response should not be empty
        self.assertIsInstance(result["final_response"], str)
        self.assertGreater(len(result["final_response"]), 0)

    def test_generate_reflect_strategy(self):
        """Test response generation with reflect strategy"""
        state = {
            "user_input": "chest tight, breath shallow",
            "teaching_strategy": {
                "strategy": "reflect",
                "guidance": "Mirror their awareness"
            },
            "extraction": {"body_signals": ["chest: tight"]},
            "user_model": {}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)
        self.generator.chat_service.generate.assert_called()

    def test_generate_teach_strategy(self):
        """Test response generation with teach strategy"""
        state = {
            "user_input": "feeling tense again",
            "teaching_strategy": {
                "strategy": "teach",
                "guidance": "Explain the pattern"
            },
            "extraction": {"body_signals": ["shoulders: tense"]},
            "user_model": {
                "patterns": {
                    "loops": [
                        {
                            "name": "Tension Loop",
                            "sequence": ["tension", "depleted"],
                            "frequency": 5
                        }
                    ]
                }
            }
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)
        self.generator.chat_service.generate.assert_called()

    def test_generate_challenge_strategy(self):
        """Test response generation with challenge strategy"""
        state = {
            "user_input": "stressed",
            "teaching_strategy": {
                "strategy": "challenge",
                "guidance": "Point out regression"
            },
            "extraction": {"body_signals": []},
            "user_model": {}
        }

        result = self.generator.generate(state)

        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)
        self.generator.chat_service.generate.assert_called()

    def test_rag_retrieval(self):
        """Test RAG wisdom retrieval"""
        contexts = self.generator._retrieve_wisdom("chest tight", "reflect")

        # Should call vector store search
        self.generator.vector_store.search.assert_called_once()

        # Should return contexts
        self.assertIsInstance(contexts, list)
        self.assertLessEqual(len(contexts), 3)

    def test_rag_retrieval_failure(self):
        """Test RAG retrieval handles failures gracefully"""
        # Mock search to raise exception
        self.generator.vector_store.search = Mock(
            side_effect=Exception("Search failed"))

        contexts = self.generator._retrieve_wisdom("test", "reflect")

        # Should return empty list on failure
        self.assertEqual(contexts, [])

    def test_format_rag_contexts(self):
        """Test RAG context formatting"""
        contexts = [
            {"text": "Teaching 1", "score": 0.9},
            {"text": "Teaching 2", "score": 0.8}
        ]

        formatted = self.generator._format_rag_contexts(contexts)

        self.assertIn("Teaching 1", formatted)
        self.assertIn("Teaching 2", formatted)
        self.assertIn("1.", formatted)
        self.assertIn("2.", formatted)

    def test_format_rag_contexts_empty(self):
        """Test RAG context formatting with empty list"""
        formatted = self.generator._format_rag_contexts([])

        self.assertIn("No specific teachings", formatted)

    def test_fallback_responses(self):
        """Test fallback responses when generation fails"""
        # Mock chat service to raise exception
        self.generator.chat_service.generate = Mock(
            side_effect=Exception("Generation failed"))

        state = {
            "user_input": "test",
            "teaching_strategy": {"strategy": "question", "guidance": "test"},
            "extraction": {},
            "user_model": {}
        }

        result = self.generator.generate(state)

        # Should still return a response (fallback)
        self.assertIn("final_response", result)
        self.assertIsInstance(result["final_response"], str)

    def test_output_structure(self):
        """Test that output has correct structure"""
        state = {
            "user_input": "test",
            "teaching_strategy": {"strategy": "reflect", "guidance": "test"},
            "extraction": {},
            "user_model": {}
        }

        result = self.generator.generate(state)

        # Should have required fields
        self.assertIn("final_response", result)
        self.assertIn("rag_contexts", result)

        # Types should be correct
        self.assertIsInstance(result["final_response"], str)
        self.assertIsInstance(result["rag_contexts"], list)


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
