from adventure.models import Room
from django.contrib.auth.models import User
import numpy as np

class World():
    def __init__(self, size = 100):
        self.size = size
        self.mid = int(size ** (1/2)) * 2 + 1
        self.length = self.mid * 2 - 1
        self.grid = [[' ' for col in range(self.length)] for row in range(self.length)]
        self.entrance = None
    def generate_rooms(self):
        # clearing users and rooms upon generating new world
        User.objects.all().delete()
        Room.objects.all().delete()
        # creating room grid 
        rooms = [[None for col in range(self.length)] for row in range(self.length)]        
        self.entrance = Room(title='Entrance', description='description')
        self.entrance.save()
        # Center Point
        self.grid[self.mid][self.mid] = 'O'
        rooms[self.mid][self.mid] = self.entrance
        dirs = ['n_to', 'e_to', 's_to', 'w_to']
        # Iterating for number of rooms
        for i in range(self.size):
            room = self.entrance            
            row = self.mid
            col = self.mid
            flag = True
            # Flag to indicate if a new room has been created this iteration
            while flag:
                r = np.random.randint(4)
                dx = dirs[r]
                rdx = dirs[(r + 2) % 4]
                row += 2 * (dx == 's_to') - 2 * (dx == 'n_to')
                col += 2 * (dx == 'e_to') - 2 * (dx == 'w_to')
                # Ensuring still within boundaries of grid
                if not 0 <= row < self.length or not 0 <= col < self.length:
                    row, col = self.mid, self.mid
                # Creating new room on empty spot as well as connection
                if self.grid[row][col] == ' ':
                    n_room = Room(title='unique room', description='description')
                    n_room.save()
                    setattr(n_room, rdx, room.id)
                    setattr(room, dx, n_room.id)
                    room.save()
                    n_room.save()
                    self.grid[row][col] = "X"
                    self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    rooms[row][col] = n_room
                    flag = False
                # Chance to connect existing rooms together in novel way
                else:
                    if np.random.randint(self.size) == 0:
                        o_room = rooms[row][col]
                        setattr(o_room, rdx, room.id)
                        setattr(room, dx, o_room.id)
                        o_room.save()
                        room.save()
                        self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    room = rooms[row][col]

        tadj = ['Abandoned', 'Derelict', 'Ruined', 'Enchanted']
        tnoun = ['Chamber', 'Garden', 'Hall', 'Shrine']
        lighting = ['In the dim light you see', 'Sconces on the wall illuminate', 'Through light fog you glimpse', 'Burning candles reveal']
        ceiling = ['water dripping from the', 'a beautifully painted', 'a partially collapsed']
        features = ['a broken statue in the corner', 'spiderwebs covering the walls', 'broken ceraminc urns in one corner', 'a jewel encrusted treasure chest']
        ground = ['uneven stone', 'smooth marble', 'damaged wooden planks', 'cooled molten rock', 'cobblestones', 'stone tiles']
        cover = ['slimy moss', 'puddles of water', 'soot and ash', 'rat droppings', 'gnawed bones', 'a large rug']
        doors = ['an open archway', 'the door is ajar', 'a sturdy hardwood door', 'a solid iron door', 'a rotting wooden door', 
                 'an ornately carved door', 'a metal door engraved with runes', 'a wall has crumbled leaving an opening']
        # Creating descriptions and titles, rendering certain path descriptions based on direction attributes        
        for line in rooms:
            for room in line:
                if room != None:
                    north = f'To the north: {np.random.choice(doors)}.' if room.n_to != 0 else ''
                    east = f'Looking east you see {np.random.choice(doors)}.' if room.e_to != 0 else ''
                    south = f'To the south {np.random.choice(doors)}.' if room.s_to != 0 else ''
                    west = f'On the west side {np.random.choice(doors)}.' if room.w_to != 0 else ''
                    if room.title != 'Entrance':
                        title = f'{np.random.choice(tadj)} {np.random.choice(tnoun)}'
                    desc = f'{np.random.choice(lighting)} a room with {np.random.choice(ceiling)} ceiling and {np.random.choice(features)}.  \
                    The floor is made of {np.random.choice(ground)} covered by {np.random.choice(cover)}.  {north} {south} {east} {west}'
                    room.title = title
                    room.description = desc
                    room.save()

        def print_rooms(self):
            map = []
            for chars in self.grid:
                map.append(''.join(chars))

            return map
            

w = World()
num_rooms = 44
width = 8
height = 7
w.generate_rooms()


# print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
