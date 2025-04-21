import requests

def generate_response(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",  # Make sure this says "phi"
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        data = response.json()
        return data['response'].strip()
    else:
        return "(Error communicating with LLM.)"