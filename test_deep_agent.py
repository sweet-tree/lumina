"""
Unit tests for Deep Agent
"""

from backend.services.deep_agent import DeepAgent
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


class TestDeepAgent(unittest.TestCase):
    """Unit tests for DeepAgent"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock Store
        self.mock_store = MagicMock()
        self.agent = DeepAgent(self.mock_store)

        # Sample extraction
        self.sample_extraction = {
            'body_signals': ['chest: tight', 'shoulders: tense'],
            'triggers': ['meeting'],
            'temporal': 'future',
            'specificity_score': 8.0
        }

    def test_relative_depth_deep(self):
        """Test depth evaluation when specificity is above baseline"""
        # Baseline 5.0, current 8.0 → should be "deep"
        depth = self.agent._calculate_relative_depth(8.0, 5.0)
        self.assertEqual(depth, 'deep')

    def test_relative_depth_shallow(self):
        """Test depth evaluation when specificity is below baseline"""
        # Baseline 7.0, current 3.0 → should be "shallow"
        depth = self.agent._calculate_relative_depth(3.0, 7.0)
        self.assertEqual(depth, 'shallow')

    def test_relative_depth_medium(self):
        """Test depth evaluation when specificity is near baseline"""
        # Baseline 5.0, current 6.0 → should be "medium"
        depth = self.agent._calculate_relative_depth(6.0, 5.0)
        self.assertEqual(depth, 'medium')

    def test_relative_depth_boundary_deep(self):
        """Test boundary condition for deep classification"""
        # Baseline 5.0, current 7.1 (> baseline + 2) → "deep"
        depth = self.agent._calculate_relative_depth(7.1, 5.0)
        self.assertEqual(depth, 'deep')

    def test_relative_depth_boundary_shallow(self):
        """Test boundary condition for shallow classification"""
        # Baseline 5.0, current 2.9 (< baseline - 2) → "shallow"
        depth = self.agent._calculate_relative_depth(2.9, 5.0)
        self.assertEqual(depth, 'shallow')

    def test_trajectory_progressing(self):
        """Test trajectory when user is progressing"""
        trajectory = self.agent._calculate_trajectory('test_user', 9.0, 5.0)

        self.assertTrue(trajectory['progressing'])
        self.assertFalse(trajectory['regressing'])

    def test_trajectory_regressing(self):
        """Test trajectory when user is regressing"""
        trajectory = self.agent._calculate_trajectory('test_user', 1.0, 5.0)

        self.assertTrue(trajectory['regressing'])
        self.assertFalse(trajectory['progressing'])

    def test_trajectory_stuck_shallow(self):
        """Test trajectory when user is stuck shallow"""
        trajectory = self.agent._calculate_trajectory('test_user', 2.0, 5.0)

        self.assertGreater(trajectory['stuck_shallow_count'], 0)

    @patch('backend.services.deep_agent.update_triggers')
    @patch('backend.services.deep_agent.update_body_patterns')
    @patch('backend.services.deep_agent.update_user_baseline')
    @patch('backend.services.deep_agent.get_triggers')
    @patch('backend.services.deep_agent.get_body_patterns')
    @patch('backend.services.deep_agent.get_user_patterns')
    @patch('backend.services.deep_agent.get_user_baseline')
    def test_evaluate_output_structure(self, mock_baseline, mock_patterns, mock_body,
                                       mock_triggers, mock_update_baseline,
                                       mock_update_body, mock_update_triggers):
        """Test that evaluate returns correct structure"""
        # Setup mocks
        mock_baseline.return_value = 5.0
        mock_patterns.return_value = {'loops': [], 'doorways': []}
        mock_body.return_value = {}
        mock_triggers.return_value = {}

        result = self.agent.evaluate('test_user', self.sample_extraction)

        # Should have required fields
        self.assertIn('user_model', result)
        self.assertIn('relative_depth', result)

        # user_model should have required fields
        user_model = result['user_model']
        self.assertIn('baseline', user_model)
        self.assertIn('patterns', user_model)
        self.assertIn('trajectory', user_model)
        self.assertIn('in_loop', user_model)

        # relative_depth should be valid
        self.assertIn(result['relative_depth'], ['shallow', 'medium', 'deep'])

    @patch('backend.services.deep_agent.update_triggers')
    @patch('backend.services.deep_agent.update_body_patterns')
    @patch('backend.services.deep_agent.update_user_baseline')
    @patch('backend.services.deep_agent.get_triggers')
    @patch('backend.services.deep_agent.get_body_patterns')
    @patch('backend.services.deep_agent.get_user_patterns')
    @patch('backend.services.deep_agent.get_user_baseline')
    def test_evaluate_calls_memory_updates(self, mock_baseline, mock_patterns, mock_body,
                                           mock_triggers, mock_update_baseline,
                                           mock_update_body, mock_update_triggers):
        """Test that evaluate updates memory correctly"""
        # Setup mocks
        mock_baseline.return_value = 5.0
        mock_patterns.return_value = {'loops': [], 'doorways': []}
        mock_body.return_value = {}
        mock_triggers.return_value = {}

        self.agent.evaluate('test_user', self.sample_extraction)

        # Should call update functions
        mock_update_baseline.assert_called_once()
        mock_update_body.assert_called_once()
        mock_update_triggers.assert_called_once()


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Deep Agent Unit Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDeepAgent)

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
