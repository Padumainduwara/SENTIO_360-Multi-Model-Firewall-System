# test_heuristic.py

# Function to check if the payload is simple conversational text
def heuristic_bypass(payload):
    # If the text has less than 5 words, bypass the heavy AI
    return len(payload.split()) < 5

def test_bypass_safe():
    # Test Case 1: Safe user sending a normal short message
    # Expected Result: True (Bypass AI and allow traffic)
    payload = "Hello how are you"
    assert heuristic_bypass(payload) == True

def test_bypass_attack():
    # Test Case 2: Hacker sending a complex SQL injection payload
    # Expected Result: False (Do not bypass, send to Deep NLP model)
    payload = "SELECT * FROM admin_users WHERE '1'='1'"
    assert heuristic_bypass(payload) == False