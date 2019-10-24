# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
from collections import deque
import random


class Room:
  def __init__(self, id, title, description, x, y):
    self.id = id
    self.title = title
    self.description = description
    self.n_to = None
    self.s_to = None
    self.e_to = None
    self.w_to = None
    self.x = x
    self.y = y
  def __repr__(self):
    if self.e_to is not None:
      return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
    return f"({self.x}, {self.y})"
  def connectRooms(self, connecting_room, direction):
    '''
    Connect two rooms in the given n/s/e/w direction
    '''
    reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
    reverse_dir = reverse_dirs[direction]
    setattr(self, f"{direction}_to", connecting_room)
    setattr(connecting_room, f"{reverse_dir}_to", self)
  def get_room_in_direction(self, direction):
    '''
    Connect two rooms in the given n/s/e/w direction
    '''
    return getattr(self, f"{direction}_to")
  def save(self):
    print(f"save room {self.id}")

######
# ZIGZAG version
# class Room:
#   def __init__(self, id, name, description, x, y):
#     self.id = id
#     self.name = name
#     self.description = description
#     self.n_to = None
#     self.s_to = None
#     self.e_to = None
#     self.w_to = None
#     self.x = x
#     self.y = y
#   def __repr__(self):
#     if self.e_to is not None:
#       return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#     return f"({self.x}, {self.y})"
#   def connect_rooms(self, connecting_room, direction):
#     '''
#     Connect two rooms in the given n/s/e/w direction
#     '''
#     reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#     reverse_dir = reverse_dirs[direction]
#     setattr(self, f"{direction}_to", connecting_room)
#     setattr(connecting_room, f"{reverse_dir}_to", self)
#   def get_room_in_direction(self, direction):
#     '''
#     Connect two rooms in the given n/s/e/w direction
#     '''
#     return getattr(self, f"{direction}_to")


class World:
  def __init__(self):
    self.grid = None
    self.width = 0
    self.height = 0 
    self.room_prob = 0.65
  def generate_rooms(self, size_x, size_y, num_rooms):
    '''
    create a room at the center, for 4 possible neighbors (n,e,s,w) create neighbor. move to created neighbors, for 3 possible new neighbors create neighbor.
    room_prob - set chance that a neighbor is created
    '''
    # Initialize the grid
    self.grid = [None] * size_y
    self.width = size_x
    self.height = size_y
    for i in range(len(self.grid)):
      self.grid[i] = [None] * size_x
    # Create room at center of grid, push to queue
    x = size_x // 2
    y = size_y // 2
    curr_room = Room(id=0, title="Treasure Chamber", description="""You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.""", x=x, y=y)
    self.grid[y][x] = curr_room
    curr_room.save()
    q = deque([(x, y)])
    # Create rooms until num_rooms created
    room_count = 1
    while room_count < num_rooms:
      curr_loc = q.popleft()
      print("HERHERHER")
      print(curr_loc)
      x = curr_loc[0]
      y = curr_loc[1]
      curr_room = self.grid[y][x]
      # check each direction, if there is not a room put that location on the q, create a room there, connect it to current room
      # n_to
      if y < (size_y - 2):
        if not self.grid[y + 1][x]:
          if self.prob_add_room(x, y + 1, room_count):
            q.append((x, y + 1))
            curr_room.connectRooms(self.grid[y + 1][x], 'n')
            room_count += 1
      # s_to
      if y > 0:
        if not self.grid[y - 1][x]:
          if self.prob_add_room(x, y - 1, room_count):
            q.append((x, y - 1))
            curr_room.connectRooms(self.grid[y - 1][x], 's')
            room_count += 1
      # e_to
      if x < (size_x - 2):
        if not self.grid[y][x + 1]:
          if self.prob_add_room(x + 1, y, room_count):
            q.append((x + 1, y))
            curr_room.connectRooms(self.grid[y][x + 1], 'e')
            room_count += 1
      # w_to
      if x > 0:
        if not self.grid[y][x - 1]:
          if self.prob_add_room(x - 1, y, room_count):
            q.append((x - 1, y))
            curr_room.connectRooms(self.grid[y][x - 1], 'w')
            room_count += 1      
  def prob_add_room(self, x, y, room_count):
    if random.random() < self.room_prob:
      new_room = Room(id=room_count, title="Room", description="room desc.", x=x, y=y)
      self.grid[y][x] = new_room
      new_room.save()
      return True
    return False 
  #####
  # ZIG ZAG
  #  
  # def generate_rooms(self, size_x, size_y, num_rooms):
  #   '''
  #   Fill up the grid, bottom to top, in a zig-zag pattern
  #   '''
  #   # Initialize the grid
  #   self.grid = [None] * size_y
  #   self.width = size_x
  #   self.height = size_y
  #   for i in range( len(self.grid) ):
  #     self.grid[i] = [None] * size_x
  #   # Start from lower-left corner (0,0)
  #   x = -1 # (this will become 0 on the first step)
  #   y = 0
  #   room_count = 0
  #   # Start generating rooms to the east
  #   direction = 1  # 1: east, -1: west
  #   # While there are rooms to be created...
  #   previous_room = None
  #   while room_count < num_rooms:
  #     # Calculate the direction of the room to be created
  #     if direction > 0 and x < size_x - 1:
  #       room_direction = "e"
  #       x += 1
  #     elif direction < 0 and x > 0:
  #       room_direction = "w"
  #       x -= 1
  #     else:
  #       # If we hit a wall, turn north and reverse direction
  #       room_direction = "n"
  #       y += 1
  #       direction *= -1
  #     # Create a room in the given direction
  #     room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
  #     # Note that in Django, you'll need to save the room after you create it
  #     # Save the room in the World grid
  #     self.grid[y][x] = room
  #     # Connect the new room to the previous room
  #     if previous_room is not None:
  #       previous_room.connect_rooms(room, room_direction)
  #     # Update iteration variables
  #     previous_room = room
  #     room_count += 1
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
      reverse_grid = list(self.grid) # make a copy of the list
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


w = World()
num_rooms = 500
width = 25
height = 25
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
