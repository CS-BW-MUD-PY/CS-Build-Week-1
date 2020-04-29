# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.


import numpy as np

class Room():
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.n_to = None
        self.e_to = None
        self.s_to = None
        self.w_to = None
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
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


class World:
    def __init__(self, size = 100):
        self.size = size
        self.mid = int(size ** (1/2)) * 3 + 1
        diameter = self.mid * 2 - 1
        self.grid = [[' ' for col in range(diameter)] for row in range(diameter)]
    def generate_rooms(self):
        dirs = ['n_to', 'e_to', 's_to', 'w_to']
        entrance = Room('entrance', 'description')
#         entrance.save()
        self.grid[self.mid][self.mid] = 'O'        
        for i in range(self.size):
            flag = True
            room = entrance            
            row = self.mid
            col = self.mid
            while flag:
                r = np.random.randint(4)
                dx = dirs[r]
                row += 2 * (dx == 's_to') - 2 * (dx == 'n_to')
                col += 2 * (dx == 'e_to') - 2 * (dx == 'w_to')
                if self.grid[row][col] == ' ':
                    n_room = Room('title', 'description')
                    setattr(n_room, dirs[(r + 2) % 4], room)
#                     n_room.save()
                    setattr(room, dx, n_room)
                    self.grid[row][col] = 'X'
                    self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    flag = False

    def print_rooms(self):   
        map = []             
        for _ in self.grid:
            map.append(''.join(_)) 

        return map


    

w = World()
num_rooms = 44
width = 8
height = 7
w.generate_rooms()
w.print_rooms()


# print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
