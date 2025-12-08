"""
Local development server
Serves the website from project root to allow access to data/news.json
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000

# Change to docs directory for serving
os.chdir(Path(__file__).parent / 'docs')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def translate_path(self, path):
        """
        Translate path to handle ../data/ requests
        """
        # Get the original path
        path = super().translate_path(path)

        # If requesting data/news.json from parent directory
        if 'data' in path and 'news.json' in path:
            # Point to actual data directory
            project_root = Path(__file__).parent
            return str(project_root / 'data' / 'news.json')

        return path

Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 서버 시작: http://localhost:{PORT}")
    print(f"📂 제공 디렉토리: {os.getcwd()}")
    print(f"💡 Ctrl+C를 눌러 서버를 중지하세요")
    print()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ 서버가 중지되었습니다.")
