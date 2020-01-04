import random
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import sys
import copy


class OceanEdge:
    def __init__(self):
        self.edges = {}
        self.cost = {}

ocean_edges = OceanEdge()
ocean_edges.coordinates = {
    0: (0, 3),
    1: (1, 2),
    2: (5, 5),
    3: (4, 3),
    4: (2, 5)
}

ocean_edges.neigbors = {
    0: [1, 3],
    1: [0, 2, 3, 4],
    2: [1],
    3: [4, 1],
    4: [1, 3]
}

fig, ax = plt.subplots(3, 3)
#ax.get_yaxis().set_visible(True)
#ax.get_xaxis().set_visible(True)

is_all_none = lambda L: not len(filter(lambda e: not e is None, L))

def cost_calculation(A,B):
    Ax = list(A)[0]
    Ay = list(A)[1]
    Bx = list(B)[0]
    By = list(B)[1]
    distance = ((Ax-Bx) ** 2 + (Ay-By)**2)**.5
    return distance

def a_star_search(ocean_edges, start, end):
    current = start
    costs_so_far = 0
    visited = []
    dead_end = []
    costs = [None] * len(ocean_edges.neigbors[current])
    visited.append(current)
    while visited[-1] != end_node:
        var = input(" ")
        current = visited[-1]
        costs = [None] * len(ocean_edges.neigbors[current])
        #print('at ', current)
        print('at ', current, 'potentials ', ocean_edges.neigbors[current])
        for potential_next in range(len(ocean_edges.neigbors[current])):
            if not ocean_edges.neigbors[current][potential_next] in visited + dead_end:
                next = ocean_edges.neigbors[current][potential_next]
                cost = ocean_edges.cost[current][potential_next]
                estimated_cost = cost_calculation(
                  ocean_edges.coordinates[current], ocean_edges.coordinates[potential_next]
                )
                #for next, cost in (ocean_edges.neigbors[start], ocean_edges.cost[start]):
                #print(potential_next)
                costs[potential_next] = cost + estimated_cost
        if [x for x in costs if x]: #is_all_none(costs):
            mincosts = costs.index(min(x for x in costs if x is not None))
            visited.append(ocean_edges.neigbors[current][mincosts])
            #print('with lowest costs', ocean_edges.neigbors[current][mincosts])
            costs_so_far += ocean_edges.cost[current][mincosts]
            #print(costs)
            delete_edge = True
        else: #no further point is reachable from current point, search for another way
            print('dead end')
            dead_end.append(current)
            # go back to previous node and delete current from visited
            #costs_so_far = ocean_edges.cost[visited[-2]][mincosts]
            print(visited)
            if len(visited) == 1:
                delete_edge = False
                visited[-1] = end_node
            else:
                del visited[-1]
                current = visited[-1]
            #delete_edge = False
            #visited[-1] = end_node
    return delete_edge, visited

for k in ocean_edges.coordinates.keys():
    #print('id ',k)
    ocean_edges.cost[k] = []
    ax[0, 0].scatter(list(ocean_edges.coordinates[k])[0], list(ocean_edges.coordinates[k])[1], marker='o', color='red')
    ax[0, 0].annotate(str(k), ocean_edges.coordinates[k])
    for n in ocean_edges.neigbors[k]:
        #print('neigh ',n)
        #print(list(ocean_edges.coordinates[k])[0])
        cost = cost_calculation(ocean_edges.coordinates[k], ocean_edges.coordinates[n])
        ocean_edges.cost[k].append(cost)
        ax[0,0].arrow(
            list(ocean_edges.coordinates[k])[0],
            list(ocean_edges.coordinates[k])[1],
            (list(ocean_edges.coordinates[n])[0] - list(ocean_edges.coordinates[k])[0]) / 1.2,
            (list(ocean_edges.coordinates[n])[1] - list(ocean_edges.coordinates[k])[1]) / 1.2,
            color='blue', head_width=0.1
        )


invalid_edges = [(0, 3), (1, 4),  (4, 1), (1, 2)]
xx = [0, 0, 1, 1, 1, 2, 2, 2]
yy = [1, 2, 0, 1, 2, 0, 1, 2]
c = 0
for i in invalid_edges:
    #print('hier',i)
    #print(ocean_edges.cost)
    #print(ocean_edges.neigbors)
    start_node = list(i)[0]
    end_node = list(i)[1]


# plt.plot([list(ocean_edges.coordinates[start_node])[0], list(ocean_edges.coordinates[start_node])[0]],
#          [list(ocean_edges.coordinates[end_node])[1], list(ocean_edges.coordinates[end_node])[1]], '-', lw=2)

    ocean_edges2 = copy.deepcopy(ocean_edges)
    index = ocean_edges.neigbors[start_node].index(end_node)
    #print('index', ocean_edges.neigbors[start_node].index(end_node))
    del ocean_edges.neigbors[start_node][index]
    del ocean_edges.cost[start_node][index]

    a = a_star_search(ocean_edges, start_node, end_node)
    if not list(a)[0]:
        print('not reachable')
        ocean_edges = copy.deepcopy(ocean_edges2)
        # dont delete edge
    for k in ocean_edges.coordinates.keys():
        ax[xx[c], yy[c]].scatter(list(ocean_edges.coordinates[k])[0], list(ocean_edges.coordinates[k])[1], marker='o', color='red')
        ax[xx[c], yy[c]].annotate(str(k), ocean_edges.coordinates[k])
        for n in ocean_edges.neigbors[k]:
            ax[xx[c], yy[c]].arrow(
                list(ocean_edges.coordinates[k])[0],
                list(ocean_edges.coordinates[k])[1],
                (list(ocean_edges.coordinates[n])[0]-list(ocean_edges.coordinates[k])[0])/1.2,
                (list(ocean_edges.coordinates[n])[1]-list(ocean_edges.coordinates[k])[1])/1.2,
                color='blue', head_width=0.1
            )
            #ax[0, 1].plot([list(ocean_edges.coordinates[k])[0], list(ocean_edges.coordinates[n])[0]],
             #     [list(ocean_edges.coordinates[k])[1], list(ocean_edges.coordinates[n])[1]], '-', lw=1, color='blue')
    c += 1
    print('for edge ', i, ': ', a)


plt.show()

