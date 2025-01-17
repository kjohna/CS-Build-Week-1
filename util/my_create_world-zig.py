from django.contrib.auth.models import User
from adventure.models import Player, Room

# delete all existing rooms
Room.objects.all().delete()

# create a World class, creates an interesting set of rooms


class World:
  def __init__(self):
    self.grid = None
    self.width = 0
    self.height = 0
  def generate_rooms(self, size_x, size_y, num_rooms):
    '''
    Fill up the grid, bottom to top, in a zig-zag pattern
    '''
    # Initialize the grid
    self.grid = [None] * size_y
    self.width = size_x
    self.height = size_y
    for i in range(len(self.grid)):
      self.grid[i] = [None] * size_x
    # Start from lower-left corner (0,0)
    x = -1  # (this will become 0 on the first step)
    y = 0
    room_count = 0
    # Start generating rooms to the east
    direction = 1  # 1: east, -1: west
    # While there are rooms to be created...
    previous_room = None
    while room_count < num_rooms:
      # Calculate the direction of the room to be created
      if direction > 0 and x < size_x - 1:
        room_direction = "e"
        x += 1
      elif direction < 0 and x > 0:
        room_direction = "w"
        x -= 1
      else:
        # If we hit a wall, turn north and reverse direction
        room_direction = "n"
        y += 1
        direction *= -1
      # Create a room in the given direction
      room = Room(title="Treasure Chamber", description="""You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.""", x=x, y=y)
      # Save the room in the World grid
      print("last line???????")
      print(f"max y: {len(self.grid)}, max x: {len(self.grid[0])}")
      print(f"x: {x}, y: {y}")
      self.grid[y][x] = room
      # Save the room to the db
      room.save()
      print(room_count)
      # Connect the new room to the previous room
      if previous_room is not None:
        print(f"conn prev:{previous_room.id} curr:{room.id} dir:{room_direction}")
        previous_room.connectRooms(room, room_direction)
      # Update iteration variables
      previous_room = room
      room_count += 1
  def print_rooms(self):
    '''
    Print the rooms in room_grid in ascii characters.
    '''
    # Add top border
    str = "# " * ((3 + self.width * 5) // 2) + "\n"
    # The console prints top to bottom but our array is arranged
    # bottom to top.
    #
    # We reverse it so it draws in the right direction.
    reverse_grid = list(self.grid)  # make a copy of the list
    reverse_grid.reverse()
    for row in reverse_grid:
      # PRINT NORTH CONNECTION ROW
      str += "#"
      for room in row:
        if room is not None and room.n_to is not None:
          str += "  |  "
        else:
          str += "     "
      str += "#\n"
      # PRINT ROOM ROW
      str += "#"
      for room in row:
        if room is not None and room.w_to is not None:
          str += "-"
        else:
          str += " "
        if room is not None:
          str += f"{room.id}".zfill(3)
        else:
          str += "   "
        if room is not None and room.e_to is not None:
          str += "-"
        else:
          str += " "
      str += "#\n"
      # PRINT SOUTH CONNECTION ROW
      str += "#"
      for room in row:
        if room is not None and room.s_to is not None:
          str += "  |  "
        else:
          str += "     "
      str += "#\n"
    # Add bottom border
    str += "# " * ((3 + self.width * 5) // 2) + "\n"
    # Print string
    print(str)


# instantiate a World, generate some rooms
w = World()
num_rooms = 101
width = 10
height = 100
w.generate_rooms(width, height, num_rooms)
# w.print_rooms()

# move all players to a starting room
players = Player.objects.all()
for p in players:
    p.currentRoom = 0
    p.save()
