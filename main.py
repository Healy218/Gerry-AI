import importlib.util
import os
import sys
import argparse
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

def interactive_mode():
    """Run in interactive mode with user input."""
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
                return bots[selection - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    parser = argparse.ArgumentParser(description="Twitch Bot Launcher")
    parser.add_argument("--bot", type=str, help="Name of the bot to run (e.g., GerryAI, DeepSeekBot)")
    parser.add_argument("--list", action="store_true", help="List available bots")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    print("Welcome to the Twitch Bot Launcher!")
    
    # List available bots
    bots = list_available_bots()
    
    # Handle interactive mode
    if args.interactive or (not args.bot and not args.list and sys.stdin.isatty()):
        selected_bot = interactive_mode()
    # Handle list mode
    elif args.list or not args.bot:
        print("\nAvailable bots:")
        for bot in bots:
            print(f"- {bot}")
        if not args.bot:
            sys.exit(0)
        selected_bot = args.bot
    else:
        selected_bot = args.bot
    
    # Check if the specified bot exists
    if selected_bot not in bots:
        print(f"Error: Bot '{selected_bot}' not found. Available bots are: {', '.join(bots)}")
        sys.exit(1)
    
    # Load and run the selected bot
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