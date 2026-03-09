# test_db_log.py

# Function to structure the threat log before pushing to MongoDB
def format_threat_log(ip, score, shap_reason):
    # Return a JSON/Dictionary format required by NoSQL database
    return {
        "ip_address": ip, 
        "final_risk_score": score, 
        "shap_explanation": shap_reason
    }

def test_database_log_structure():
    # Test Case 1: Verify the dictionary keys and values
    mock_log = format_threat_log("192.168.1.100", 0.88, "High Packet Length Std")
    
    # Expected Result: The dictionary must contain exactly these keys
    assert "ip_address" in mock_log
    assert "shap_explanation" in mock_log
    
    # Expected Result: Values must match exactly
    assert mock_log["final_risk_score"] == 0.88
    assert mock_log["ip_address"] == "192.168.1.100"