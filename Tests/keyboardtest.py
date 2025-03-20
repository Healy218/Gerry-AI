import keyboard

def on_key_event(e):
    print("Key event:", e.name, e.scan_code)

keyboard.hook(on_key_event)
keyboard.wait()
