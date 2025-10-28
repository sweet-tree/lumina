"""
Single workflow test - just run once to see if it works
"""

from backend.services.multi_agent_service import MultiAgentService
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


print("Testing single workflow run...")
print("=" * 60)

service = MultiAgentService()

result = service.process_checkin(
    user_id="test_user",
    user_input="chest tight, breath shallow, meeting soon"
)

print(f"\nInput: 'chest tight, breath shallow, meeting soon'")
print(f"Depth: {result.get('depth')}")
print(f"Strategy: {result.get('teaching_strategy', {}).get('strategy')}")
print(f"Card Awarded: {result.get('card_decision', {}).get('award_card')}")
print(f"Response: {result.get('response')}")

if 'extraction' in result:
    print(f"\nExtraction:")
    print(f"  Body signals: {result['extraction'].get('body_signals')}")
    print(f"  Specificity: {result['extraction'].get('specificity_score')}")

if 'error' in result:
    print(f"\n⚠️  Error occurred: {result['error']}")
else:
    print(f"\n✓ Workflow completed successfully!")

print("=" * 60)
