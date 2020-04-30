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
        self.length = self.mid * 2 - 1
        self.grid = [[' ' for col in range(self.length)] for row in range(self.length)]
        self.entrance = None
    def generate_rooms(self):
        counter = 1
        Room.objects.all().delete()
        rooms = [[None for col in range(self.mid * 2 - 1)] for row in range(self.mid * 2 - 1)]        
        self.entrance = Room(title='Entrance', description='description')
        self.entrance.save()
        self.grid[self.mid][self.mid] = 'O'
        rooms[self.mid][self.mid] = self.entrance
        dirs = ['n_to', 'e_to', 's_to', 'w_to']
        for i in range(self.size):
            room = self.entrance            
            row = self.mid
            col = self.mid
            flag = True
            while flag:
                r = np.random.randint(4)
                dx = dirs[r]
                rdx = dirs[(r + 2) % 4]
                row += 2 * (dx == 's_to') - 2 * (dx == 'n_to')
                col += 2 * (dx == 'e_to') - 2 * (dx == 'w_to')
                if not 0 <= row < self.length or not 0 <= col < self.length:
                    row, col = self.mid, self.mid
                if self.grid[row][col] == ' ':
                    counter += 1
                    n_room = Room(title='unique room', description='description')
                    n_room.save()
                    # Room.objects.get(rooms[row][col])
                    setattr(n_room, rdx, room.id)
                    setattr(room, dx, n_room.id)
                    room.save()
                    n_room.save()
                    self.grid[row][col] = "X"
                    self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    rooms[row][col] = n_room
                    flag = False
                else:
                    if np.random.randint(self.size) == 0:
                        o_room = rooms[row][col]
                        setattr(o_room, rdx, room.id)
                        setattr(room, dx, o_room.id)
                        o_room.save()
                        room.save()
                        self.grid[row + (dx == 'n_to') - (dx == 's_to')][col + (dx == 'w_to') - (dx == 'e_to')] = '*'
                    room = rooms[row][col]
        for chars in self.grid:
            print(''.join(chars))

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
