from adventure.models import Room
import numpy as np

# class Room():
#     def __init__(self, title, description):
#         self.title = title
#         self.description = description
#         self.n_to = None
#         self.e_to = None
#         self.s_to = None
#         self.w_to = None

Room.objects.all().delete()

class World():
    def __init__(self, size = 100):
        self.size = size
        self.mid = int(size ** (1/2)) * 2 + 1
        diameter = self.mid * 2 - 1
        self.grid = [[' ' for col in range(diameter)] for row in range(diameter)]
    def generate_rooms(self):
        rooms = [[None for col in range(self.mid * 2 - 1)] for row in range(self.mid * 2 - 1)]
        dirs = ['n_to', 'e_to', 's_to', 'w_to']
        entrance = Room(title='entrance', description='description')
        self.grid[self.mid][self.mid] = 'O'
        rooms[self.mid][self.mid] = entrance
        bonus = 0
        for i in range(self.size):
            flag = True
            room = entrance            
            row = self.mid
            col = self.mid
            while flag:
                r = np.random.randint(4)
                dx = dirs[r]
                rdx = dirs[(r + 2) % 4]
                row += 2 * (dx == 's_to') - 2 * (dx == 'n_to')
                col += 2 * (dx == 'e_to') - 2 * (dx == 'w_to')
                if self.grid[row][col] == ' ':
                    n_room = Room(title='title', description='description')
                    n_room.save()
                    setattr(n_room, rdx, room)
                    setattr(room, dx, n_room)
                    self.grid[row][col] = 'X'
                    self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    rooms[row][col] = n_room
                    flag = False
                else:
                    if np.random.randint(self.size) == 0:
                        o_room = rooms[row][col]
                        setattr(room, dx, o_room)
                        setattr(o_room, rdx, room)
                        self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    room = rooms[row][col]
        for _ in self.grid:
            print(''.join(_))

        for line in rooms:
            for room in line:
                if room != None:
                    room.save()

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
