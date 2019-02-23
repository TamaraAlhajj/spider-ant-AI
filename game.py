from collections import deque
from random import randint
from time import clock
from myPQ import PriorityQueue
from math import sqrt

############################ Initial Setup ############################

# GLOBALS #

# Dimensions #
board = 16

""" 
# Defining all spider movement partterns for playable game #
moves = [
    'NNW': [-1, 2],
    'NNE': [1, 2],
    'NW': [-2, 1],
    'NE': [2, 1],
    'W': [-1, 0],
    'E': [1, 0],
    'SW': [-1, -1],
    'SE': [1, -1],
    'S': [0, -1]
] """

# Production system #
moves = [
    [-1, 2],
    [1, 2],
    [-2, 1],
    [2, 1],
    [-1, 0],
    [1, 0],
    [-1, -1],
    [1, -1],
    [0, -1]
]

# State space as a set (hash table) O(1) membership check #
seen_states = {}

# Search path #
path = deque()

# Defining all ant moves #
vectors = [[0, 1], [-1, 0], [0, -1], [1, 0]]
#vectors = [[0, 2], [-2, 0], [0, -2], [2, 0]]
#vectors = [[0, 3], [-3, 0], [0, -3], [3, 0]]

direction = vectors[0]
#######################################################################

###### ant stuff ######

def ant_init():
    # one dim must be 0 or 16 to be an edge
        
    if(randint(0,10) <= 5):
        if(randint(0,10) <= 5):
            x = 0
        else:
            x = 15
        y = randint(0, 15)
    else:
        if(randint(0,10) <= 5):
            y = 0
        else:
            y = 15
        x = randint(0, 15)

    return [x,y]

def ant_dir(init):
    if(init[0] == 0):
        return vectors[3]      
    elif(init[0] == 15):
        return vectors[1]
    elif(init[1] == 0):
        return vectors[0]
    else:
        return vectors[2]

#############################################################################


def off_board(state):
    for coord in state:
        if(coord > 15 or coord < 0):
            return True
    return False

### UPDATE CREATURES ###
def make_move(state, move):
    spider = state[:2]
    ant = state[2:]
    new_spider = [spider[0]+move[0], spider[1]+move[1]]
    new_ant = [ant[0]+direction[0], ant[1]+direction[1]]
    new_state = new_spider + new_ant
    if(off_board(new_state)):
        return False
    return new_state


### GENERATE POSSIBLE MOVES ###
def expand(state):
    global seen_states, path, fringe

    for move in moves:
        new_state = make_move(state, move)
        if((new_state != False) and (tuple(new_state) not in seen_states)):
            path.append(new_state)
            seen_states[tuple(new_state)] = state


### PRINT CURRENT BOARD ###
def display_board(state):

    print('\n' + '-'*27 + 'spider: {}   ant: {}'.format(state[:2], state[2:]) + '-'*27)

    # spider location
    sx = state[0]
    sy = state[1]

    # ant location
    ax = state[2]
    ay = state[3]

    hex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']

    print("    ", end="")
    for y in hex:
        print("  {}  ".format(y), end="")
    print()
    for y in range(board):
        print(" {} ".format(hex[y]), end=" ")
        for x in range(board):
            if(x == sx and y == sy):
                print('[=0=]', end='')
            elif(x == ax and y == ay):
                print('[...]', end='')
            else:
                print('[   ]', end='')
        print()

### ONCE FOUND SHOW PATH TO GOAL ###
def display_path(goal, blind=True):
    current = goal
    moves = 0
    while(current != None):
        moves += 1
        display_board(current)
        current = seen_states[tuple(current)]
    print('\nDONE! {} states searched, {} move solution found. \nScroll up to see solution.'.format(len(seen_states), moves))


### CHECK IF GOAL STATE REACHED ###
def goal_check(state):
    if(state[0] == state[2] and state[1] == state[3]):
        return True
    return False

def reset():
    global seen_states, path

    seen_states = {}
    path = deque()

    return

def bfs(init):
    # searching is false once goal state game over is reached
    state = init

    while (path):
        state = path.popleft()
        expand(state)
        if(goal_check(state)):
            display_path(state)
            return
    print("No Solution Found for state : \n")
    display_board(init)


def dfs(init):
    # false once goal state game over is reached #
    state = init

    while (path):
        state = path.pop()
        expand(state)
        if(goal_check(state)):
            display_path(state)
            return
    print("No Solution Found for state : \n")
    display_board(init)

def raw(state):
    # raw distance on a square grid
    sx = state[0]
    sy = state[1]
    ax = state[2]
    ay = state[3]

    dx = abs(sx - ax)
    dy = abs(sy - ay)
    
    return (dx + dy)/2


def euclid(state):
    # pythagorean distance on a square grid
    sx = state[0]
    sy = state[1]
    ax = state[2]
    ay = state[3]

    dx = abs(sx - ax)
    dy = abs(sy - ay)
    return sqrt(dx**2 + dy**2)

def avg(state):
    c1 = raw(state)
    c2 = euclid(state)
    return (c1 + c2)/2

def A_star(init, heuristic):
    global moves

    if(heuristic == 1):
        heuristic = raw
    elif(heuristic == 2):
        heuristic = euclid
    else:
        heuristic = avg

    # cost_so_far , Dijkstra dist value
    # came_from , Dijkstra dist value
    # fringe , ordered by cost to get to a state + heuristic

    fringe = PriorityQueue()
    came_from = {}
    cost_so_far = {}

    fringe.put(tuple(init), 0)
    came_from[tuple(init)] = None
    cost_so_far[tuple(init)] = 0
    move_count = 0

    while(not fringe.empty()):
        current = fringe.get()

        if(goal_check(current)):
            count = 0
            while(current != None):
                count += 1
                display_board(current)
                current = came_from[current]
            print('\nDONE! {} states generated, {} move solution found. \nScroll up to see solution.'.format(move_count, count))
            return
        
        for move in moves:
            new_move = make_move(current, move)
            if((new_move != False)):
                new_move = tuple(new_move)
                new_cost = cost_so_far[current] + 1 
                if(new_move not in cost_so_far or new_cost < cost_so_far[new_move]):
                    cost_so_far[new_move] = new_cost
                    priority = new_cost + heuristic(list(new_move))
                    fringe.put(new_move, priority)
                    move_count += 1
                    came_from[new_move] = current
    print("No Solution Found for state {}: \n".format(init))
    display_board(init)

def play():
    global direction, seen_states, path

    playing = True

    while(playing):

        spider = [randint(0,15), randint(0,15)]
        ant = ant_init()
        initial_state = spider + ant

        # globals
        direction = ant_dir(ant)
        seen_states[tuple(initial_state)] = None
        path.append(initial_state)

        search = input('Choose an AI! (bfs, dfs, a*) : ')

        if(search == 'bfs'):
            start = clock()
            bfs(initial_state)
            elapsed = clock()
            print('Run Time: {:0.3f} seconds\n'.format(elapsed - start))
        elif(search == 'dfs'):
            start = clock()
            dfs(initial_state)
            elapsed = clock()
            print('Run Time: {:0.3f} seconds\n'.format(elapsed - start))
        elif(search == 'a*'):
            start = clock()
            h = input("Which heuristic? (1 raw, 2 euclid, 3 avg) : ")
            A_star(initial_state, h)
            elapsed = clock()
            print('Run Time: {:0.3f} seconds\n'.format(elapsed - start))
        else:
            print('Invalid search')
        reset()
        check = input('Try again? (n to exit, any key to play) : ')
        if(check == 'n'):
            playing = False


def main():
    play()


if __name__ == "__main__":
    main()