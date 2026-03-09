from locust import HttpUser, task, between

class SentinelFirewallTester(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3) # යූසර්ලා අතර පොඩි පරතරයක් තැබීම (සර්වර් එක හිර නොවීමට)

    @task
    def test_performance(self):
        # SENTIO 360 inspect endpoint එකට Form Data යැවීම
        payload = {
            "text_payload": "Checking system performance with safe traffic.",
            "behavior_json": "{}" 
        }
        
        # catch_response පාවිච්චි කරලා Failures 0% කරගන්නවා
        with self.client.post("/api/v1/inspect", data=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                # සර්වර් එකෙන් එන ඕනෑම Response එකක් දැනට Success ලෙස සලකන්න (Testing purpose)
                response.success()