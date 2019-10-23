from django.contrib.auth.models import User
from adventure.models import Player, Room
from collections import deque
import random

# delete all existing rooms
Room.objects.all().delete()

# create a World class, creates an interesting set of rooms
class World:
  def __init__(self, room_prob):
    self.grid = None
    self.width = 0
    self.height = 0
    self.room_prob = room_prob
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
    curr_room = Room(id=1, title="Treasure Chamber", description="""You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.""", x=x, y=y)
    self.grid[y][x] = curr_room
    curr_room.save()
    q = deque([(x, y)])
    # Create rooms until num_rooms created
    room_count = 1
    while room_count < num_rooms:
      curr_loc = q.popleft()
      # print("HERHERHER")
      # print(curr_loc)
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
            print("n connection")
            print(f"current: {self.grid[y][x].id}")
            print(f"curr n_to: {self.grid[y][x].n_to}")
            print(f"n_to: {self.grid[y+1][x].id}")
            print(f"n_to s_to: {self.grid[y+1][x].s_to}")
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
      new_room = Room(title="Room", description="room desc.")
      self.grid[y][x] = new_room
      new_room.save()
      return True
    return False
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
w = World(0.65)
num_rooms = 4
width = 5
height = 5
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

# move all players to a starting room
players = Player.objects.all()
for p in players:
    p.currentRoom = 0
    p.save()
