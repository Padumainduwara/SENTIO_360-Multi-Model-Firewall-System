# test_autoencoder.py

# Function to detect zero-day network anomalies using MSE
def check_network_anomaly(mse_error, threshold=0.05):
    # If Mean Squared Error is higher than threshold, flag as anomaly
    return mse_error > threshold

def test_autoencoder_block():
    # Test Case 1: Unnatural packet length variance simulating a DDoS attack
    # Expected Result: True (Anomaly detected)
    high_mse = 0.085
    assert check_network_anomaly(high_mse) == True

def test_autoencoder_safe():
    # Test Case 2: Normal web browsing traffic with low reconstruction error
    # Expected Result: False (Normal traffic)
    low_mse = 0.012
    assert check_network_anomaly(low_mse) == False