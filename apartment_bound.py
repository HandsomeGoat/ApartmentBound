import json
class Room:
    def __init__(self, name, description):
       self.name = name
       self.description = description
       self.exits = {}
       self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name:
                return item
            return None

    def add_exit(self, direction, neighbor):
        self.exits[direction] = neighbor

    def get_exit(self, direction):
        return self.exits.get(direction)

    def get_full_description(self):
        full_discription = "\n" + self.description + "\nExits: "
        exit_list = ", ".join(self.exits.keys())
        full_discription += exit_list
        return full_discription

    @classmethod
    def from_json(cls, json_data):
        room = cls(json_data["name"], json_data["description"])
        for direction, neighbor in json_data["exits"].items():
            room.add_exit(direction, neighbor)
        return room


    @staticmethod
    def load_rooms_from_json(file_path):
        with open(file_path, "r") as json_file:
            room_data = json.load(json_file)
            rooms = {}
        for room_name, data in room_data.items():
            room = Room.from_json(data)
            rooms[room_name] = room
        return rooms

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    @staticmethod
    def load_items_from_json(file_path):
        with open(file_path, "r") as json_file:
            item_data = json.load(json_file)
    
            items = {}
            for item_id, data in item_data.items():
                item = Item(data["name"], data["description"])
                items[item_id] = item
            return items



class Player:
    def __init__(self):
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def get_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item  # Return the item if found
        return None  # Return None if item is not found

    def remove_item(self, item_name):
        if isinstance(item_name, str):
            item_index_to_remove = None
            for index, item in enumerate(self.inventory):
                if item.name.lower() == item_name.lower():
                    item_index_to_remove = index
                    break

            if item_index_to_remove is not None:
                removed_item = self.inventory.pop(item_index_to_remove)
                return removed_item
        return None

# Initialize the Player object
player = Player()

# Load the rooms into memory
room_data_file = "rooms.json" 
rooms = Room.load_rooms_from_json(room_data_file)

# Load items into memory
item_data_file = "items.json"  
items = Item.load_items_from_json(item_data_file)

# Create instances of items
safe_key = items["Safe Key"]

# Add items to rooms or the player's inventory as needed
rooms["Bedroom"].add_item(safe_key)

# Set initial room / player state
current_room = rooms["Living Room"]

while True:
    # Display the current room's description and exits
    print(current_room.get_full_description())

    # Get user input
    user_input = input("Enter a command: ").strip().lower()

    if user_input == "quit" or user_input == "exit":
        print("\nThanks for playing! Goodbye.")
        break  # Exit the game loop

    # Check if the input is a valid exit
    next_room = current_room.get_exit(user_input)

    if next_room:
        current_room = rooms[next_room]
    # Take an item from the current room
    elif user_input.startswith("take"):
        item_name = user_input.split(" ", 1)[1]
        item = current_room.get_item(item_name)
        if item:
            player.add_item(item)
            current_room.remove_item(item)
            print(f"You have taken the {item.name}.")
        else:
            print("That item is not here.")
    # Drop an item from the player's inventory
    elif user_input.startswith("drop"):
        item_name = user_input.split(" ", 1)[1]
        item = player.get_item(item_name)
        if item:
            current_room.add_item(item)
            player.remove_item(item)
            print(f"You have dropped the {item.name}.")
        else:
            print("You don't have that item.")
    else:
        print("Invalid command. Try again.")
