from collections import deque
from random import randint

# TODO refactor!!

############################ Initial Setup ############################

# GLOBALS #

# Dimensions #
board = 16

# Defining all ant moves, NWSE -- logic is wonky here TODO #
vectors = [[0, 1], [-1, 0], [0, -1], [1, 0]]

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

direction = vectors[0]

# State space as a set (hash table) O(1) membership check #
seen_states = {}

# Search path #
path = deque()

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
        return vectors[2]      
    elif(init[0] == 16):
        return vectors[0]
    elif(init[1] == 0):
        return vectors[1]
    else:
        return vectors[3]

#############################################################################


def off_board(state):
    for coord in state:
        if(coord > 15 or coord < 0):
            return True
    return False

### UPDATE CREATURES ###
def make_move(state, move):
    if(off_board(state)):
        return False
    spider = state[:2]
    ant = state[2:]
    new_spider = [spider[0]+move[0], spider[1]+move[1]]
    new_ant = [ant[0]+direction[0], ant[1]+direction[1]]
    new_state = new_spider + new_ant
    return new_state


### GENERATE POSSIBLE MOVES ###
def expand(state):
    for move in moves:
        new_state = make_move(state, move)
        if((new_state != False) and (tuple(new_state) not in seen_states)):
            path.append(new_state)
            seen_states[tuple(new_state)] = state

### PRINT CURRENT BOARD ###
def display_board(state):

    print(state)

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
def display_path(goal):
    current = goal
    while(current != 0):
        display_board(current)
        current = seen_states[tuple(current)]


### CHECK IF GOAL STATE REACHED ###
def goal_check(state):
    if(state[0] == state[2] and state[1] == state[3]):
        display_path(state)
        return False
    return True


def bfs(init):
    # false once goal state game over is reached #
    state = init
    searching = True

    while (searching):
        if(path):
            state = path.popleft()
            expand(state)
            searching = goal_check(state)
        else:
            searching = False
            print('---end of game---')


def dfs(init):
    # false once goal state game over is reached #
    state = init
    searching = True

    while (searching):
        if(path):
            state = path.pop()
            expand(state)
            searching = goal_check(state)
        else:
            searching = False
            print('---end of game---')


def A_star():
    pass


def play():
    spider = [randint(0,15), randint(0,15)]
    ant = ant_init()
    initial_state = spider + ant
    direction = ant_dir(initial_state)

    seen_states[tuple(initial_state)] = 0
    path.append(initial_state)

    #bfs(initial_state)
    dfs(initial_state)

def main():
    play()


if __name__ == "__main__":
    main()
