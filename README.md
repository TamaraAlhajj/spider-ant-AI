# The Spider and The Ant

## Overview

### To run game from working directory:

`python3 game.py`

Then follow instructions to try different AI techniques:

- BFS
- DFS
- A*

### A* Heuristics

- raw difference between cartesian coordinates of spider and ant
- euclidean difference between cartesian coordinates of spider and ant
- average difference given by raw and euclidean differences.

## Reflection on AI Techniques

### State Space

My state space is stored as a tuple of the spider and ant cartesian coordinates. So I never store the whole board which would take up quadratic space for each state stored. Since the blind searches often searched hundreds of states this space and time complexity would be sufficiently large to notice the efficient storage. Instead, by storing only 4 numbers to represent only the needed knowledge of the board I use constant space for each state stored. Using a tuple means that my explored states can be stored in a python dictionary. This is python's equivalent to a hash table. Since my explored states are stored in a hash
table, I avoid cycles by avoiding collisions of the same key states. I search the state space with data driven searches, including two blind searches and a an intelligent search. These search algorithms are used to generate successors of explored states, however it is the data structures that prove to be the main difference between them.

### Analysis of Blind Search Strategies

The two blind searches used are the Breadth First Search, Depth First Search. The DFS performed worse, as expected. With a DFS the state space was searched using a queue where as the BFS used a stack. A LIFO data structure is not favorable in a game like this because it favours deep exploration, thus expanding many states to find a costly solution. However, using a FIFO as the BFS means it will always find the optimal path as it would search all nine moves given by the production system before moving on to the next nine moves. In this game BFS often returned solutions that played few moves and had to search a few hundred states. The DFS always returned solutions with around 16 moves (the size of the board), such that the spider would wander around the board before tracing back to the ant. Moreover, the DFS would search hundreds more states than the BFS, without returning an optimal solution. Regardless of these differences, the run times of both searches were both miniscule, where both would usually return after 0.01 seconds.

### A* Heuristics 

Of all the searches the intelligent search performed the best: A* heuristic search. To implement A* I used a priority queue with three different heuristics. I choose to implement a raw distance heuristic which calculates half the (x, y) difference between the spider and the ant. Next I implemented a euclidean distance heuristic, which calculates the difference between the spider and ant coordinates then calculates the pythagorean formula with these values. Lastly I implemented an average of the two, which simply calls each adds their returned values and divides by two. Both the raw and euclidean heuristics performed quite
well and thus the average of the two performed well too. I found average performed slightly better than the other two, since it would search less states return a low move solution. The runtime would usually be around 0.005 seconds, which is a bit faster than the blind searches mentioned. However, where A* is impressive is in it’s intelligent expansion of the state space. Bad moves are avoided, and a direct chase is favoured. Due to this property of the A* search, it would never search above 80 states. In fact, it would usually expand around 30
states before finding the optimal solution. This is a significant improvement to the blind search.