from http.server import BaseHTTPRequestHandler
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def load_medical_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "medical_dataset.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

medical_data = load_medical_data()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = {
            'total': len(medical_data),
            'diseases': [{'id': doc.get('id'), 'title': doc.get('title')} for doc in medical_data]
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
