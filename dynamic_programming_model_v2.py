# Libraries
import itertools
import pickle
import numpy as np
import math
import networkx as nx


### FUNCTIONS

def get_time_distance(node1, node2):
    """Returns time-distance between two nodes, memoizes result"""
    dist = g.edge[node1][node2]['cost']
    return int(dist)



# DATA SOURCE

# TEMPORARY: Simplified nodes input
NODES = {
	0: 0,
	1: 10,
	2: -10,
	3: 10,
	4: -10,
	5: 10,
	6: -10,
	7: 10,
	8: -10,
	9: 10,
	10: -10,
	11: 10,
	12: -10,
	13: 10
}



# Time matrix
access_path = '/home/eolus/Dropbox/610 Project Data'

time_matrix_array = pickle.load( open(access_path + '/time_matrix.pkl', 'rb') )

assert(time_matrix_array.shape[0] == time_matrix_array.shape[1]), \
	"Time matrix is not square: {columns} columns // {rows} rows".format(columns = time_matrix_array.shape[0], rows = time_matrix_array.shape[1])

INSTANCE_SIZE = 14

# Network
g = nx.Graph()

# Populate nodes
for node in range(INSTANCE_SIZE):
	g.add_node(node, load = NODES[node])

# Populate edges
for i in range(INSTANCE_SIZE):
	for j in range(INSTANCE_SIZE):
		cost_ij = time_matrix_array[i,j]
		g.add_edge(i,j, cost = cost_ij)




# CONSTANTS
list_all_nodes = list(NODES.keys())
NODE_COUNT = len(NODES)

# GLOBAL VARIABLES
level = 0
routes_in_progress = {(0,): (0, 0)}   	# {(route): (total_load, total_distance)}

best_times = []

sorted(best_times, key=lambda student: student[2])


print('STARTING LOOP')
# DYNAMIC ITERATION
while(level <= NODE_COUNT):
	
	# Routes tested in current loop: length == level+1
	level += 1
	print(level)

	# Update `routes_in_progress`: Remove routes with: length < level
	if(level > 1):
		for key in [key for key in routes_in_progress.keys() if (len(key) < level)]:
			routes_in_progress.pop(key, None)

	# List all routes in progress
	list_routes_in_progress = list(routes_in_progress.keys())

	# Iterate through routes in progress
	for current_route in list_routes_in_progress:
		nodes_remaining = []

		# Case: connection to last node
		if (level == NODE_COUNT):
			nodes_remaining = [0]

		# Case: connection to all possible remaining nodes
		else:
			nodes_remaining = [node for node in list_all_nodes if node not in current_route]

		# Iterate through possible nodes remaining
		for node_test in nodes_remaining:
			# Load test:
			local_load = NODES[node_test]
			legacy_load = routes_in_progress[current_route][0]
			total_load = legacy_load + local_load
			if(total_load > 0):
				continue
			else:
				local_distance = get_time_distance(current_route[0], node_test)
				legacy_distance = routes_in_progress[current_route][1]
				total_distance = local_distance + legacy_distance

				updated_route = tuple(list(current_route) + [node_test])
				routes_in_progress[updated_route] = (total_load, total_distance)
				if(len(updated_route) >= NODE_COUNT):
					print('New: {route} \t {load} \t {distance}'.format(route= updated_route,load = total_load, distance = total_distance))


import operator

optimal_route = max(routes_in_progress.iteritems(), key=operator.itemgetter(1))[0]
print(optimal_route)
