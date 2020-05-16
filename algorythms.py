import math


def neighbors(field, r, c, do_diag=True):
    straight = [(field.get_cell(rw, cl), 1.0) for rw, cl in field.get_neighbors(r, c, diag=False) if
                not field.get_cell(rw, cl).is_wall]
    diag = []
    if do_diag:
        diag = [(field.get_cell(rw, cl), math.sqrt(2)) for rw, cl in field.get_neighbors(r, c, straight=False) if
                not field.get_cell(rw, cl).is_wall]
    return straight + diag


def dijkstra(field, callback, diag=True):
    unvisited = []
    #  1. Mark all nodes unvisited and store them
    for row in range(field.get_rows()):
        for col in range(field.get_cols()):
            if field.get_cell(row, col) and (row, col) != field.start_point:
                unvisited.append([row, col])
                field.set_value(row, col, math.inf)

    previous_nodes = {}
    for node in unvisited:
        previous_nodes[tuple(node)] = None

    #  2. Set the distance to zero for our initial node
    field.set_value(*field.start_point, 0)
    curr_node = None

    while unvisited and any([not field.get_cell(r, c).is_wall for r, c in unvisited]) and curr_node != field.end_point:
        #  3. Select the unvisited node with the smallest distance, it's current node now
        unvisited.sort(key=lambda x: field.get_value(*x))
        curr_node = unvisited[0]

        #  4. Find unvisited neighbors for the current node and calculate their distances through the current node.
        for neighbor in [x for x in neighbors(field, *curr_node, diag) if list(x[0].get_pos(field)) in unvisited]:
            dist = field.get_value(*curr_node) + neighbor[1]
            if neighbor[0].get_value() > dist:
                neighbor[0].set_value(dist)
                previous_nodes[neighbor[0].get_pos(field)] = tuple(curr_node)

        #  5. Mark the current node as visited and remove it from the unvisited set.
        unvisited.remove(curr_node)
        callback(field, curr_node)
    path_node = tuple(field.end_point)
    path = []
    while path_node != tuple(field.start_point):
        print(path_node, ':', previous_nodes[path_node])
        path.append(path_node)
        path_node = previous_nodes[path_node]
    path.append(tuple(field.start_point))
    return path



algorythms = {"Djikstra's algorithm": dijkstra}
