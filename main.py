import importlib.util
import os
import sys
from pathlib import Path

def load_bot_module(bot_name):
    """Dynamically load a bot module from the bots directory."""
    bot_path = Path("bots") / f"{bot_name}.py"
    if not bot_path.exists():
        raise FileNotFoundError(f"Bot {bot_name} not found in bots directory")
    
    spec = importlib.util.spec_from_file_location(bot_name, bot_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def list_available_bots():
    """List all available bots in the bots directory."""
    bots_dir = Path("bots")
    return [f.stem for f in bots_dir.glob("*.py")]

def main():
    print("Welcome to the Twitch Bot Launcher!")
    print("\nAvailable bots:")
    
    # List available bots
    bots = list_available_bots()
    for i, bot in enumerate(bots, 1):
        print(f"{i}. {bot}")
    
    # Get user selection
    while True:
        try:
            selection = int(input("\nEnter the number of the bot you want to run (or 0 to exit): "))
            if selection == 0:
                print("Goodbye!")
                sys.exit(0)
            if 1 <= selection <= len(bots):
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Load and run the selected bot
    selected_bot = bots[selection - 1]
    print(f"\nLoading {selected_bot}...")
    try:
        bot_module = load_bot_module(selected_bot)
        print(f"Starting {selected_bot}...")
        bot_module.bot.run()
    except Exception as e:
        print(f"Error running {selected_bot}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 