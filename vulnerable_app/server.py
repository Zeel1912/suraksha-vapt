#!/usr/bin/env python3
"""
Vulnerable Web Application Server
Educational test environment for SURAKSHA VAPT platform
"""

import http.server
import socketserver
import os
import sys
import subprocess
import time

class VulnerableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set PHP files to be handled by PHP CGI
        if self.path.endswith('.php'):
            self.run_php_script()
        else:
            super().do_GET()

    def run_php_script(self):
        """Execute PHP scripts using php-cgi"""
        try:
            # Get the full path to the PHP file
            php_file = os.path.join(os.getcwd(), self.path[1:])  # Remove leading /

            if not os.path.exists(php_file):
                self.send_error(404, "File not found")
                return

            # Run PHP script
            result = subprocess.run(
                ['php', php_file],
                capture_output=True,
                text=True,
                env=dict(os.environ, **{
                    'REQUEST_METHOD': 'GET',
                    'QUERY_STRING': self.path.split('?', 1)[1] if '?' in self.path else '',
                    'SCRIPT_NAME': self.path.split('?')[0],
                    'REQUEST_URI': self.path,
                    'DOCUMENT_ROOT': os.getcwd(),
                    'REMOTE_ADDR': self.client_address[0],
                    'REMOTE_PORT': str(self.client_address[1])
                })
            )

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result.stdout.encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def do_POST(self):
        """Handle POST requests for PHP scripts"""
        if self.path.endswith('.php'):
            self.run_php_script_post()
        else:
            self.send_error(405, "Method not allowed")

    def run_php_script_post(self):
        """Execute PHP scripts with POST data"""
        try:
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Get the full path to the PHP file
            php_file = os.path.join(os.getcwd(), self.path[1:])

            if not os.path.exists(php_file):
                self.send_error(404, "File not found")
                return

            # Run PHP script with POST data
            result = subprocess.run(
                ['php', php_file],
                input=post_data,
                capture_output=True,
                text=True,
                env=dict(os.environ, **{
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                    'CONTENT_LENGTH': self.headers.get('Content-Length', '0'),
                    'SCRIPT_NAME': self.path,
                    'REQUEST_URI': self.path,
                    'DOCUMENT_ROOT': os.getcwd(),
                    'REMOTE_ADDR': self.client_address[0],
                    'REMOTE_PORT': str(self.client_address[1])
                })
            )

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result.stdout.encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

def setup_database():
    """Initialize the vulnerable database"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS vulnerable_db")
        print("✓ Database 'vulnerable_db' created")

        conn.close()
        print("✓ Database setup complete")
    except ImportError:
        print("⚠️ MySQL connector not available. Please install with: pip install mysql-connector-python")
    except Exception as e:
        print(f"⚠️ Database setup failed: {e}")

def main():
    # Change to vulnerable_app directory
    os.chdir(os.path.dirname(__file__) or '.')

    print("🎯 SURAKSHA Vulnerable Test Environment")
    print("=" * 50)
    print("⚠️  WARNING: This is for educational purposes only!")
    print("🚫 Never expose this to the internet!")
    print("=" * 50)

    # Setup database
    setup_database()

    # Start server
    port = 8080
    handler = VulnerableHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Server started at http://localhost:{port}")
            print("📁 Serving files from:", os.getcwd())
            print("🔗 Access the vulnerable app at: http://localhost:8080")
            print("🛑 Press Ctrl+C to stop the server")
            print()

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()