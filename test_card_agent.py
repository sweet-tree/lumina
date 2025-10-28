"""
Unit tests for Card Agent
"""

from backend.services.card_agent import CardAgent
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


class TestCardAgent(unittest.TestCase):
    """Unit tests for CardAgent"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = CardAgent()

    def test_award_deep_reflection(self):
        """Test card award for deep reflection"""
        user_model = {
            "patterns": {"loops": []},
            "trajectory": {},
            "in_loop": False
        }
        extraction = {
            "body_signals": ["chest: tight"],
            "triggers": []
        }

        result = self.agent.decide_award(user_model, "deep", extraction)

        self.assertTrue(result["award_card"])
        self.assertEqual(result["rarity"], "common")
        self.assertIn("Deep reflection", result["reason"])
        self.assertIsNotNone(result["card_id"])

    def test_no_award_shallow_first_attempt(self):
        """Test no card for shallow first attempt"""
        user_model = {
            "patterns": {"loops": []},
            "trajectory": {},
            "in_loop": False
        }
        extraction = {
            "body_signals": [],
            "triggers": []
        }

        result = self.agent.decide_award(user_model, "shallow", extraction)

        self.assertFalse(result["award_card"])
        self.assertIsNone(result["card_id"])
        self.assertIn("first attempt", result["reason"])

    def test_award_new_pattern_rare(self):
        """Test rare card for new pattern detection"""
        user_model = {
            "patterns": {
                "loops": [
                    {
                        "name": "Monday Morning Spiral",
                        "sequence": ["tension", "depleted", "foggy"],
                        "frequency": 3  # Exactly 3 = first detection
                    }
                ]
            },
            "trajectory": {},
            "in_loop": False
        }
        extraction = {
            "body_signals": ["chest: tight"],
            "triggers": []
        }

        result = self.agent.decide_award(user_model, "medium", extraction)

        self.assertTrue(result["award_card"])
        self.assertEqual(result["rarity"], "rare")
        self.assertIn("pattern detected", result["reason"])
        self.assertEqual(result["card_id"], "monday_morning_spiral")

    def test_no_award_medium_depth(self):
        """Test no card for medium depth without other criteria"""
        user_model = {
            "patterns": {"loops": []},
            "trajectory": {},
            "in_loop": False
        }
        extraction = {
            "body_signals": ["chest: tight"],
            "triggers": []
        }

        result = self.agent.decide_award(user_model, "medium", extraction)

        self.assertFalse(result["award_card"])
        self.assertIsNone(result["card_id"])

    def test_card_selection_chest(self):
        """Test card selection for chest signals"""
        extraction = {
            "body_signals": ["chest: tight", "chest: heavy"],
            "triggers": []
        }

        card_id = self.agent._select_card_from_signals(extraction)

        self.assertEqual(card_id, "heart_opening")

    def test_card_selection_shoulders(self):
        """Test card selection for shoulder signals"""
        extraction = {
            "body_signals": ["shoulders: tense"],
            "triggers": []
        }

        card_id = self.agent._select_card_from_signals(extraction)

        self.assertEqual(card_id, "burden_release")

    def test_card_selection_breath(self):
        """Test card selection for breath signals"""
        extraction = {
            "body_signals": ["breath: shallow"],
            "triggers": []
        }

        card_id = self.agent._select_card_from_signals(extraction)

        self.assertEqual(card_id, "breath_awareness")

    def test_card_selection_default(self):
        """Test default card when no recognized signals"""
        extraction = {
            "body_signals": ["unknown_location: sensation"],
            "triggers": []
        }

        card_id = self.agent._select_card_from_signals(extraction)

        self.assertEqual(card_id, "presence")

    def test_card_selection_no_signals(self):
        """Test card selection with no body signals"""
        extraction = {
            "body_signals": [],
            "triggers": []
        }

        card_id = self.agent._select_card_from_signals(extraction)

        self.assertEqual(card_id, "awareness")

    def test_pattern_to_card_id(self):
        """Test pattern name to card ID conversion"""
        loop = {
            "name": "Monday Morning Spiral",
            "frequency": 5
        }

        card_id = self.agent._pattern_to_card_id(loop)

        self.assertEqual(card_id, "monday_morning_spiral")

    def test_new_pattern_detection_frequency_3(self):
        """Test new pattern detection with frequency 3"""
        patterns = {
            "loops": [
                {"name": "Test Loop", "frequency": 3}
            ]
        }

        result = self.agent._check_new_pattern_detected(patterns)

        self.assertTrue(result)

    def test_new_pattern_detection_frequency_not_3(self):
        """Test no new pattern with frequency != 3"""
        patterns = {
            "loops": [
                {"name": "Test Loop", "frequency": 5}
            ]
        }

        result = self.agent._check_new_pattern_detected(patterns)

        self.assertFalse(result)

    def test_new_pattern_detection_no_loops(self):
        """Test no new pattern when no loops"""
        patterns = {"loops": []}

        result = self.agent._check_new_pattern_detected(patterns)

        self.assertFalse(result)

    def test_output_structure(self):
        """Test that output has correct structure"""
        user_model = {
            "patterns": {"loops": []},
            "trajectory": {},
            "in_loop": False
        }
        extraction = {
            "body_signals": ["chest: tight"],
            "triggers": []
        }

        result = self.agent.decide_award(user_model, "deep", extraction)

        # Should have required fields
        self.assertIn("award_card", result)
        self.assertIn("card_id", result)
        self.assertIn("rarity", result)
        self.assertIn("reason", result)

        # Types should be correct
        self.assertIsInstance(result["award_card"], bool)
        self.assertIn(result["rarity"], [
                      "common", "rare", "epic", "legendary"])
        self.assertIsInstance(result["reason"], str)

    def test_rarity_levels(self):
        """Test different rarity levels"""
        # Common: deep reflection
        user_model_common = {
            "patterns": {"loops": []},
            "trajectory": {},
            "in_loop": False
        }
        result_common = self.agent.decide_award(
            user_model_common, "deep", {"body_signals": [], "triggers": []})
        self.assertEqual(result_common["rarity"], "common")

        # Rare: new pattern
        user_model_rare = {
            "patterns": {
                "loops": [{"name": "Test", "frequency": 3}]
            },
            "trajectory": {},
            "in_loop": False
        }
        result_rare = self.agent.decide_award(user_model_rare, "medium", {
                                              "body_signals": [], "triggers": []})
        self.assertEqual(result_rare["rarity"], "rare")


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Card Agent Unit Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCardAgent)

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
