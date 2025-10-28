"""
Test two workflow runs to see the prepared statement issue
"""

from backend.services.multi_agent_service import MultiAgentService
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


print("Testing two workflow runs...")
print("=" * 60)

service = MultiAgentService()

print("\n### RUN 1 ###")
result1 = service.process_checkin(
    user_id="user1",
    user_input="stressed"
)
print(f"Depth: {result1.get('depth')}")
print(f"Response: {result1.get('response')[:80]}...")

print("\n### RUN 2 ###")
result2 = service.process_checkin(
    user_id="user2",
    user_input="chest tight"
)
print(f"Depth: {result2.get('depth')}")
print(
    f"Response: {result2.get('response')[:80] if result2.get('response') else 'ERROR'}")

if 'error' in result2:
    print(f"\n⚠️  Error on run 2: {result2['error'][:100]}")
else:
    print(f"\n✓ Both runs completed successfully!")

print("=" * 60)

service.close()
