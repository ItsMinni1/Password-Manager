import sys
import webview
from app import app

if __name__ == '__main__':
    # Initialize the desktop window, pointing to the Flask app
    window = webview.create_window('Minni Password Manager', app, width=1024, height=768)
    webview.start()
