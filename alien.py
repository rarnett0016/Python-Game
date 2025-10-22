
# TextBasedGame.py
# Author: Ryan Arnett
# Course: IT-140
# Theme: Alien Artifact Retrieval (Text-Based Adventure)
#
# Project Two Requirements Covered:
# - Functions for instructions and status display
# - main() with a dictionary linking rooms and items
# - Gameplay loop with function calls, decision branching, and input validation
# - Win/Lose conditions based on items collected vs. entering villain room
# - Clear naming conventions and in-line comments (industry-standard best practices)

def show_instructions():
    """Print game title, objective, and available commands."""
    print("""
    =====================================
         ALIEN ARTIFACT: TEXT ADVENTURE
    =====================================
    Objective:
      Collect all 6 alien artifacts before you enter the Villain's room.

    Commands:
      go North | go South | go East | go West
      get <item name>
      status          (show current room, inventory, and visible item)
      help            (show these instructions again)
      quit            (exit the game)3
      
      
    """)


def show_status(current_room, inventory, rooms):
    """Show the player's current room, inventory, and any item present."""
    print("\n-----------------------------")
    print(f"You are in: {current_room}")
    print("Inventory:", inventory if inventory else "[empty]")
    # If this room has an item and it hasn't been picked up yet, display it
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print("-----------------------------")


def normalize_command(text):
    """Normalize whitespace and capitalization for consistent parsing."""
    return " ".join(text.strip().split())


def main():
    """Main gameplay function: sets up the map, runs the input loop, and handles win/lose logic."""
    # -----------------------------
    # Map: Rooms, exits, and items
    # Edit the names/items below if you need to align to your Project One map exactly.
    # Start Room: Bridge (no item)
    # Villain Room: Reactor Core (contains 'Alien Stalker' - cannot be collected)
    # Items to collect (6): Xenotech Circuit, Plasma Core, Holo Map, Stasis Key, Artifact Shard, Quantum Relic
    # -----------------------------
    rooms = {
        "Bridge": {
            "South": "Engineering Bay",
            "East": "Observation Deck",
            "West": "Crew Quarters"
            # Start room has no item
        },
        "Engineering Bay": {
            "North": "Bridge",
            "South": "Cargo Hold",
            "item": "Xenotech Circuit",
        },
        "Cargo Hold": {
            "North": "Engineering Bay",
            "East": "Airlock",
            "item": "Plasma Core",
        },
        "Airlock": {
            "West": "Cargo Hold",
            "North": "Med Lab",
            "item": "Holo Map",
        },
        "Med Lab": {
            "South": "Airlock",
            "West": "Observation Deck",
            "item": "Stasis Key",
        },
        "Observation Deck": {
            "West": "Bridge",
            "South": "Med Lab",
            "East": "Reactor Core",  # Leads to Villain room
            "item": "Artifact Shard",
        },
        "Crew Quarters": {
            "East": "Bridge",
            "South": "Reactor Access",
            "item": "Quantum Relic",
        },
        "Reactor Access": {
            "North": "Crew Quarters",
            # (Intentionally no direct path to Reactor Core in this layout. Keep or adjust as desired.)
        },
        "Reactor Core": {
            "West": "Observation Deck",
            "item": "Alien Stalker",  # Villain
        },
    }

    # Constants for clarity
    START_ROOM = "Bridge"
    VILLAIN_ROOM = "Reactor Core"
    VILLAIN_NAME = "Alien Stalker"

    # Compute how many unique collectible items exist based on the map (excludes the villain)
    required_items = [rooms[r]["item"] for r in rooms if "item" in rooms[r] and rooms[r]["item"] != VILLAIN_NAME]
    total_items_required = len(required_items)  # Should be 6 for this map

    # Game state
    current_room = START_ROOM
    inventory = []

    # Intro and first status display
    show_instructions()
    show_status(current_room, inventory, rooms)

    # -----------------------------
    # Gameplay loop
    # -----------------------------
    while True:
        user_input = input("Enter your move: ")
        command = normalize_command(user_input)

        if not command:
            print("Please enter a command. Type 'help' for options.")
            continue

        # Single-word utility commands
        if command.lower() == "quit":
            print("Exiting game. Thanks for playing!")
            break
        if command.lower() == "help":
            show_instructions()
            continue
        if command.lower() == "status":
            show_status(current_room, inventory, rooms)
            continue

        # Movement: must start with 'go '
        if command.lower().startswith("go "):
            # Get direction with Title case (North/South/East/West)
            direction = command[3:].strip().title()
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]

                # If player enters the villain room, check win/lose
                if current_room == VILLAIN_ROOM:
                    if len(inventory) >= total_items_required:
                        print("\n>>> You enter the Reactor Core, fully equipped with all artifacts.")
                        print(f"You confront the {VILLAIN_NAME} and prevail!\n")
                        print("Congratulations! You collected all artifacts and saved the ship!")
                        print("Thanks for playing the game. Hope you enjoyed it.")
                        break
                    else:
                        print("\n>>> ALERT: You have entered the Reactor Core without all artifacts!")
                        print(f"The {VILLAIN_NAME} emerges from the shadows...")
                        print("NOM NOM... GAME OVER!")
                        print("Thanks for playing the game. Hope you enjoyed it.")
                        break
                else:
                    # Normal room: show updated status
                    show_status(current_room, inventory, rooms)
            else:
                # Input validation: invalid direction for current room
                print("You can't go that way. Try a different direction.")
            continue

        # Item pickup: must start with 'get '
        if command.lower().startswith("get "):
            requested_item = command[4:].strip()
            room_item = rooms[current_room].get("item")  # None if no item in room

            # Validate item exists in room and matches requested name (case-insensitive)
            if room_item and room_item.lower() == requested_item.lower():
                if room_item == VILLAIN_NAME:
                    print("You can't collect the villain! Focus on survival.")
                elif room_item in inventory:
                    print(f"You already collected the {room_item}.")
                else:
                    inventory.append(room_item)
                    # Remove item from the room after collecting
                    del rooms[current_room]["item"]
                    print(f"{room_item} collected! Inventory now: {inventory}")
            else:
                # Input validation: no matching item to pick up here
                print("There is no such item here to get.")
            continue

        # If we reach this point, the command didn't match any valid pattern
        print("Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
