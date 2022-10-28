import os
import copy

'''
hàng cột
map
x1 y1 x2 y2
các hàng tiếp theo thể hiện tọa độ các nút của cầu
'''
indir = "io_bloxorz/input"
outdir = "io_bloxorz/output"
# this class manage state of map
class bloxorz_state:
    def __init__(self, x1, y1, x2, y2, map, parent):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.map = copy.deepcopy(map)
        self.parent = parent
    
    def __str__(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        res = "==================================\n"
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if ((i == y1 and j == x1) or (i == y2 and j == x2)):
                    res += 'X '
                elif self.map[i][j] == 0:
                    res += '  '
                else:
                    res += str(self.map[i][j]) + ' '
            res += '\n'
        return res

class bloxorz_manage:
    def __init__(self, input):
        self.row, self.col, map, x1, y1, x2, y2, self.button = self.read_input(input)
        self.init_state = bloxorz_state(x1, y1, x2, y2, map, None)

    def read_input(self, filename):
        with open(os.path.join(indir,filename), "r") as f:
            #read number of column and number of row
            row, col = [int(x) for x in next(f).split()]
            #read map
            map = []
            countLine = 0
            for line in f:
                map.append([int(x) for x in line.split()])
                countLine += 1
                if countLine == row:
                    break
            #read x1, y1, x2, y2
            x1, y1, x2, y2 = [int(x) for x in next(f).split()]
            #read button management
            # <x> <y> <type(0(openonly), 1(closeonly), 2(both))> <numOfPoint> [<xi> <yi>]
            button = []
            for line in f:
                button.append([int(x) for x in next(f).split()])
            
            return row, col, map, x1, y1, x2, y2, button

    def goal_state(self, state) -> bool:
        if state.x1 == state.x2 and state.y1 == state.y2:
            if state.map[state.y1][state.x1] == 2:
                return True 
        return False

    def check_valid_state(self, state) -> bool:
        x1, x2, y1, y2, map = state.x1, state.x2, state.y1, state.y2, state.map
        if min(x1, x2) >= 0 and min(y1, y2) >= 0 and max(x1, x2) < len(map[0]) and max(y1, y2) < len(map):
            if state.map[y1][x1] == 0 or state.map[y2][x2] == 0: 
                return False
            elif x1 == x2 and y1 == y2 and state.map[y1][x1] == 3: #check for red point
                return False
            return True
        return False

    def move_up(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            y1 -= 1
            y2 -= 2
        elif y1 == y2: # horizontal
            y1 -= 1
            y2 -= 1
        else: #vertical
            y1 = y2 = min(y1-1, y2-1)
        state = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(state):
            return state
        return None

    def move_down(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            y1 += 1
            y2 += 2
        elif y1 == y2: # horizontal
            y1 += 1
            y2 += 1
        else: #vertical
            y1 = y2 = max(y1+1, y2+1)
        state = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(state):
            return state
        return None

    def move_left(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            x1 -= 1
            x2 -= 2
        elif y1 == y2: # horizontal
            x1 = x2 = min(x1-1, x2-1)
        else: #vertical
            x1 -= 1
            x2 -= 1
        state = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(state):
            return state
        return None

    def move_right(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            x1 += 1
            x2 += 2
        elif y1 == y2: # horizontal
            x1 = x2 = max(x1+1, x2+1)
        else: #vertical
            x1 += 1
            x2 += 1
        state = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(state):
            return state
        return None

class bloxorz_dfs(bloxorz_manage):
    def __init__(self, input):
        bloxorz_manage.__init__(self, input)
        self.isVisited = []
        self.input = input

    def check_for_visited(self, state):
        for i in self.isVisited:
            if state.x1 == i.x1 and state.y1 == i.y1 and state.x2 == i.x2 and \
                state.y2 == i.y2 and state.map == i.map:
                return False
        return True

    def get_all_next_state(self, state):
        up, down, left, right = self.move_up(state), self.move_down(state), self.move_left(state), self.move_right(state)
        res = []
        if (up != None and self.check_for_visited(up)):
            res.append(up)
            self.isVisited.append(up)
        if (down != None and self.check_for_visited(down)):
            res.append(down)
            self.isVisited.append(down)
        if (left != None and self.check_for_visited(left)):
            res.append(left)
            self.isVisited.append(left)
        if (right != None and self.check_for_visited(right)):
            res.append(right)
            self.isVisited.append(right)
        return res

    def DFS(self):
        stack = [self.init_state]
        self.isVisited.append(self.init_state)
        while stack:
            cur = stack.pop()

            if self.goal_state(cur):
                # print result
                with open(os.path.join(outdir,self.input.replace("input", "output")), "w") as f:
                    states = []
                    while cur:
                        states.append(cur)
                        cur = cur.parent
                    states.reverse()
                    for i in range(len(states)):
                        f.write("Step " + str(i) + "\n")
                        f.write(str(states[i]))
            else:
                move = self.get_all_next_state(cur)
                for i in move:
                    stack.append(i)
    