import http.server
import socketserver
import webbrowser
import os
import threading

def start_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Change to the directory containing tickertape.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving tickertape at http://localhost:{PORT}/tickertape.html")
        webbrowser.open(f'http://localhost:{PORT}/tickertape.html')
        httpd.serve_forever()

def launch_ticker():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # This ensures the thread will close when the main program exits
    server_thread.start() 