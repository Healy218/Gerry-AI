import threading
import time
import keyboard
from flask import Flask, jsonify

app = Flask(__name__)

# Global flag to signal a reset
reset_flag = False

print(keyboard._os_keyboard.from_name)

@app.route('/check', methods=['GET'])
def check_reset():
    global reset_flag
    if reset_flag:
        reset_flag = False  # Reset the flag so the command is only sent once
        return jsonify({'reset': True})
    return jsonify({'reset': False})

def run_flask():
    # Run the Flask server on port 5000
    app.run(port=5000)

def listen_for_keypress():
    global reset_flag

    def trigger_reset():
        global reset_flag
        reset_flag = True
        print("Numpad 9 pressed: Reset flag set.")

    # Listen for the numpad 9 key press
    keyboard.add_hotkey("9", trigger_reset)
    print("Listening for Numpad 9 press. Press Numpad 9 to trigger a reset command.")
    keyboard.wait()  # Keeps the listener running indefinitely

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("Flask server running on http://localhost:5000")

    # Start listening for key presses (this runs in the main thread)
    listen_for_keypress()
