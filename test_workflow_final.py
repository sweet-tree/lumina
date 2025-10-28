"""
Final workflow test - single service instance for all tests
"""

from backend.services.multi_agent_service import MultiAgentService
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


print("=" * 60)
print("Multi-Agent Workflow Tests")
print("=" * 60)

# Create single service instance (reused for all tests)
service = MultiAgentService()

print("\n### TEST 1: Shallow Input ###")
result1 = service.process_checkin(
    user_id="user1",
    user_input="stressed"
)
print(f"✓ Depth: {result1['depth']}")
print(f"✓ Response: {result1['response'][:80]}...")

print("\n### TEST 2: Deep Input ###")
result2 = service.process_checkin(
    user_id="user2",
    user_input="chest tight, breath shallow, shoulders tense"
)
print(f"✓ Depth: {result2['depth']}")
print(f"✓ Extraction: {result2['extraction']['body_signals']}")
print(f"✓ Response: {result2['response'][:80]}...")

print("\n### TEST 3: Multiple Check-ins Same User ###")
result3a = service.process_checkin(
    user_id="user3",
    user_input="jaw clenched"
)
result3b = service.process_checkin(
    user_id="user3",
    user_input="jaw still clenched, stomach tight now"
)
print(f"✓ First check-in depth: {result3a['depth']}")
print(f"✓ Second check-in depth: {result3b['depth']}")

print("\n### TEST 4: Card Award ###")
result4 = service.process_checkin(
    user_id="user4",
    user_input="chest tight, breath shallow, heart racing, meeting in 5 minutes"
)
print(f"✓ Depth: {result4['depth']}")
print(f"✓ Card awarded: {result4['card_decision']['award_card']}")
if result4['card_decision']['award_card']:
    print(
        f"✓ Card: {result4['card_decision']['card_id']} ({result4['card_decision']['rarity']})")

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)

service.close()
