#lambda test
import copy


def cost_calculation(A,B):
    Ax = list(A)[0]
    Ay = list(A)[1]
    Bx = list(B)[0]
    By = list(B)[1]
    distance = ((Ax-Bx) ** 2 + (Ay-By)**2)**.5
    return distance


nodes = list(range(0, 5))
print(nodes)
coordinates = {
    0: (0, 3),
    1: (1, 2),
    2: (5, 5),
    3: (4, 3),
    4: (2, 5)
}

neighbours = {
    0: [1, 3],
    1: [0, 2, 3, 4],
    2: [1],
    3: [4, 1],
    4: [1, 3]
}
ocean_edges = {}
testcost ={}
for key in nodes:
    ocean_edges[key] = {
        'coordinates': coordinates[key],
        'neighbours': neighbours[key],
        'cost': list(map(lambda v: cost_calculation(coordinates[v], coordinates[key]), neighbours[key]))
    }
    testcost[key] = list(map(lambda v: cost_calculation(coordinates[v], coordinates[key]), neighbours[key]))

print(testcost[0])
print(ocean_edges[0]['coordinates'])