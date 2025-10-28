"""
Unit tests for Extraction Agent
"""

from backend.services.extraction_agent import ExtractionAgent
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


class TestExtractionAgent(unittest.TestCase):
    """Unit tests for ExtractionAgent"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.agent = ExtractionAgent()

    def test_shallow_input_vague_label(self):
        """Test extraction with shallow input - vague emotional label"""
        result = self.agent.extract("stressed")

        # Should have no body signals
        self.assertEqual(result['body_signals'], [])

        # Should have no triggers
        self.assertEqual(result['triggers'], [])

        # Should be present tense
        self.assertEqual(result['temporal'], 'present')

        # Should have low specificity (0-3)
        self.assertLessEqual(result['specificity_score'], 3)
        self.assertGreaterEqual(result['specificity_score'], 0)

    def test_medium_input_body_awareness(self):
        """Test extraction with medium input - some body awareness"""
        result = self.agent.extract("shoulders tight")

        # Should have body signals
        self.assertGreater(len(result['body_signals']), 0)
        self.assertIn('shoulders', result['body_signals'][0].lower())

        # Should be present tense
        self.assertEqual(result['temporal'], 'present')

        # Should have medium specificity (4-6)
        self.assertGreaterEqual(result['specificity_score'], 4)
        self.assertLessEqual(result['specificity_score'], 6)

    def test_deep_input_specific_with_context(self):
        """Test extraction with deep input - specific sensations + context"""
        result = self.agent.extract(
            "chest tight, breath shallow, meeting in 10 min")

        # Should have multiple body signals
        self.assertGreaterEqual(len(result['body_signals']), 2)

        # Should have triggers
        self.assertGreater(len(result['triggers']), 0)

        # Should be future tense
        self.assertEqual(result['temporal'], 'future')

        # Should have high specificity (7-10)
        self.assertGreaterEqual(result['specificity_score'], 7)
        self.assertLessEqual(result['specificity_score'], 10)

    def test_deep_input_very_specific(self):
        """Test extraction with very specific body awareness"""
        result = self.agent.extract(
            "jaw clenched, shoulders up to ears, about to call mom")

        # Should have multiple body signals
        self.assertGreaterEqual(len(result['body_signals']), 2)

        # Should have triggers
        self.assertGreater(len(result['triggers']), 0)

        # Should be future tense
        self.assertEqual(result['temporal'], 'future')

        # Should have very high specificity (8-10)
        self.assertGreaterEqual(result['specificity_score'], 8)

    def test_past_tense_detection(self):
        """Test temporal detection for past tense"""
        result = self.agent.extract("was anxious yesterday")

        # Should detect past tense
        self.assertEqual(result['temporal'], 'past')

        # Should have low specificity
        self.assertLessEqual(result['specificity_score'], 4)

    def test_output_structure(self):
        """Test that output has correct structure"""
        result = self.agent.extract("test input")

        # Should have all required fields
        self.assertIn('body_signals', result)
        self.assertIn('triggers', result)
        self.assertIn('temporal', result)
        self.assertIn('specificity_score', result)

        # Should have correct types
        self.assertIsInstance(result['body_signals'], list)
        self.assertIsInstance(result['triggers'], list)
        self.assertIsInstance(result['temporal'], str)
        self.assertIsInstance(result['specificity_score'], (int, float))

        # Temporal should be valid
        self.assertIn(result['temporal'], ['past', 'present', 'future'])

        # Specificity should be in range
        self.assertGreaterEqual(result['specificity_score'], 0)
        self.assertLessEqual(result['specificity_score'], 10)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Extraction Agent Unit Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExtractionAgent)

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
