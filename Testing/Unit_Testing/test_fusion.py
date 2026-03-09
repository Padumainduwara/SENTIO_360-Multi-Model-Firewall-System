# test_fusion.py

# Function to calculate the final Meta-Learning risk score
def calc_fusion_score(nlp_prob, behavior_prob, vision_prob):
    # Apply mathematical weights: NLP(35%), Behavior(45%), Vision(20%)
    return (nlp_prob * 0.35) + (behavior_prob * 0.45) + (vision_prob * 0.20)

def test_fusion_score_block():
    # Test Case 1: High threat detected across multiple modalities
    # Expected Result: Final score must be strictly greater than 0.60 (Block threshold)
    final_score = calc_fusion_score(0.80, 0.90, 0.50)
    assert final_score > 0.60 

def test_fusion_score_allow():
    # Test Case 2: Very low threat probabilities from AI engines
    # Expected Result: Final score must be below 0.60 (Allow traffic)
    final_score = calc_fusion_score(0.10, 0.05, 0.15)
    assert final_score < 0.60