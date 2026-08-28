import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_v2_flow():
    print("1. Preparing Interview...")
    prep_payload = {
      "candidate_id": "dca3fbc0-da27-4a98-b951-7354aaadbc73",
      "config": {
        "role": "AI Engineer",
        "level": "Junior",
        "duration_minutes": 30
      }
    }
    # User might have AUTH_ENABLED=true or false, we will try with anonymous user
    headers = {"X-User-ID": "95b19827-e2cf-4abd-aa30-53391a4987a4"}
    
    resp1 = requests.post(f"{BASE_URL}/api/v2/interview/prepare", json=prep_payload, headers=headers)
    if resp1.status_code != 200:
        print("Prepare Failed:", resp1.text)
        return
        
    data1 = resp1.json()
    session_id = data1["session_id"]
    print(f"-> Prepare Success! Session ID: {session_id}")
    print(f"-> Rounds: {len(data1['plan']['rounds'])}")
    
    print("\n2. Starting Interview (Generating First Question)...")
    start_time = time.time()
    start_payload = {
        "session_id": session_id
    }
    resp2 = requests.post(f"{BASE_URL}/api/v2/interview/start", json=start_payload, headers=headers)
    if resp2.status_code != 200:
        print("Start Failed:", resp2.text)
        return
        
    data2 = resp2.json()
    print(f"-> Start Success in {time.time() - start_time:.2f}s!")
    print("\n=== AI INTERVIEWER ASKS ===")
    print(data2["question"]["question_text"])
    print("\n=== EXPECTED KEY POINTS ===")
    for pt in data2["question"]["expected_key_points"]:
        print(f"- {pt}")
        
if __name__ == "__main__":
    test_v2_flow()
