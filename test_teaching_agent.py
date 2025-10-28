"""
Unit tests for Teaching Agent
"""

from backend.services.teaching_agent import TeachingAgent
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


class TestTeachingAgent(unittest.TestCase):
    """Unit tests for TeachingAgent"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = TeachingAgent()

    def test_question_strategy_stuck_shallow(self):
        """Test question strategy when stuck shallow 5+ times"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 5,
                "regressing": False,
                "progressing": False
            },
            "in_loop": False,
            "patterns": {"loops": []}
        }

        result = self.agent.decide_strategy(user_model, "shallow", {})

        self.assertEqual(result["strategy"], "question")
        self.assertIn("body location", result["guidance"])
        self.assertIn("5", result["reason"])

    def test_challenge_strategy_regressing(self):
        """Test challenge strategy when user is regressing"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 0,
                "regressing": True,
                "progressing": False
            },
            "in_loop": False,
            "patterns": {"loops": []}
        }

        result = self.agent.decide_strategy(user_model, "shallow", {})

        self.assertEqual(result["strategy"], "challenge")
        self.assertIn("deeper before", result["guidance"])
        self.assertIn("regressing", result["reason"])

    def test_teach_strategy_in_loop(self):
        """Test teach strategy when user is in a loop"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 0,
                "regressing": False,
                "progressing": False
            },
            "in_loop": True,
            "patterns": {
                "loops": [
                    {
                        "name": "Monday Morning Spiral",
                        "sequence": ["tension", "depleted", "foggy"],
                        "frequency": 5
                    }
                ]
            }
        }

        result = self.agent.decide_strategy(user_model, "medium", {})

        self.assertEqual(result["strategy"], "teach")
        self.assertIn("pattern", result["guidance"])
        self.assertIn("Monday Morning Spiral", result["reason"])

    def test_teach_strategy_new_pattern(self):
        """Test teach strategy when pattern first detected"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 0,
                "regressing": False,
                "progressing": False
            },
            "in_loop": False,
            "patterns": {
                "loops": [
                    {
                        "name": "Work Tension Loop",
                        "sequence": ["tension", "depleted"],
                        "frequency": 3  # Exactly 3 = first detection
                    }
                ]
            }
        }

        result = self.agent.decide_strategy(user_model, "medium", {})

        self.assertEqual(result["strategy"], "teach")
        self.assertIn("pattern", result["guidance"])

    def test_reflect_strategy_default(self):
        """Test reflect strategy as default"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 0,
                "regressing": False,
                "progressing": False
            },
            "in_loop": False,
            "patterns": {"loops": []}
        }

        result = self.agent.decide_strategy(user_model, "deep", {})

        self.assertEqual(result["strategy"], "reflect")
        self.assertIn("Mirror", result["guidance"])
        self.assertIn("progressing", result["reason"])

    def test_strategy_priority_stuck_over_regressing(self):
        """Test that stuck shallow takes priority over regressing"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 6,
                "regressing": True,  # Both conditions true
                "progressing": False
            },
            "in_loop": False,
            "patterns": {"loops": []}
        }

        result = self.agent.decide_strategy(user_model, "shallow", {})

        # Stuck shallow should take priority
        self.assertEqual(result["strategy"], "question")

    def test_strategy_priority_regressing_over_loop(self):
        """Test that regressing takes priority over loop"""
        user_model = {
            "trajectory": {
                "stuck_shallow_count": 0,
                "regressing": True,
                "progressing": False
            },
            "in_loop": True,  # Both conditions true
            "patterns": {
                "loops": [{"name": "Test Loop", "frequency": 5}]
            }
        }

        result = self.agent.decide_strategy(user_model, "shallow", {})

        # Regressing should take priority
        self.assertEqual(result["strategy"], "challenge")

    def test_output_structure(self):
        """Test that output has correct structure"""
        user_model = {
            "trajectory": {"stuck_shallow_count": 0, "regressing": False, "progressing": False},
            "in_loop": False,
            "patterns": {"loops": []}
        }

        result = self.agent.decide_strategy(user_model, "medium", {})

        # Should have required fields
        self.assertIn("strategy", result)
        self.assertIn("guidance", result)
        self.assertIn("reason", result)

        # Strategy should be valid
        self.assertIn(result["strategy"], ["question",
                      "reflect", "teach", "challenge"])

        # All fields should be strings
        self.assertIsInstance(result["strategy"], str)
        self.assertIsInstance(result["guidance"], str)
        self.assertIsInstance(result["reason"], str)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Teaching Agent Unit Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTeachingAgent)

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
