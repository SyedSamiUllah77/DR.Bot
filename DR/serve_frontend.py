import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def start_server():
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ Frontend server running at http://localhost:{PORT}")
        print(f"✅ Backend API running at http://localhost:8000")
        print(f"\n🏥 Opening Medical Chatbot in browser...")
        print(f"\nPress Ctrl+C to stop the server\n")
        httpd.serve_forever()

if __name__ == "__main__":
    # Open browser after a short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f'http://localhost:{PORT}/chatbot.html')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
