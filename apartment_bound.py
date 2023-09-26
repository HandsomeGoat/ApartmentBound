import json
class Room:
    def __init__(self, name, description):
       self.name = name
       self.description = description
       self.exits = {}

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

#     Now you can load room data from the JSON file and create room instances using the load_rooms_from_json method:

room_data_file = "rooms.json"  # Replace with your JSON file path
rooms = Room.load_rooms_from_json(room_data_file)

current_room = rooms["Living Room"]

while True:
    # Display the current room's description and exits
    print(current_room.get_full_description())

    # Get user input
    user_input = input("Enter a direction (e.g., north, south, east, west): ").strip().lower()

    if user_input == "quit" or user_input == "exit":
        print("\nThanks for playing! Goodbye.")
        break  # Exit the game loop

    # Check if the input is a valid exit
    next_room = current_room.get_exit(user_input)

    if next_room:
        current_room = rooms[next_room]
    else:
        print("Invalid direction. Try again.")
