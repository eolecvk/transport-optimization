# Description:
# Generate list of possible routes based on input nodes.
# Nodes need to be parameterized with:
#	1. Time window
#	2. Capacity (supply/demand)

# 1. Generate all the routes that take less than `TIME_LIMIT` to complete
# 2. Filter out routes that violate truck load non-negativity constraint
# 3. Filter out routes that violate node time-window constraint

# Access path
access_path = '/home/eolus/Dropbox/610 Project Data'

# Model Parameters
TIME_LIMIT = 3300

# Libraries
import itertools
import pickle
import numpy as np
import math

# Instantiate network

import networkx as nx

print('Building network...')

g = nx.Graph()

g.graph['title'] 	= 'Test network'
g.graph['day'] 		= 'Tuesday'
g.graph['driver']	= 'John SMITH'
g.graph['zone']		= 'East Boston'

print('NETWORK DETAILS')
print('***************************')
print(g.graph)
print('***************************')



# Load input
print('Loading input data...')

## Time matrix
time_matrix_array = pickle.load( open(access_path + '/time_matrix.pkl', 'rb') )

assert(time_matrix_array.shape[0] == time_matrix_array.shape[1]), \
	"Time matrix is not square: {columns} columns // {rows} rows".format(columns = time_matrix_array.shape[0], rows = time_matrix_array.shape[1])

INSTANCE_SIZE = time_matrix_array.shape[0]


## Other input: node attributes


# ******************************
load_scores = [
0,
650,
-614,
137,
532,
-127,
429,
-187,
-616,
374,
235,
-178,
-201,
-434
]


time_windows = [
(0,86340),
(32400, 54000), 
(39600, 46800), 
(28800, 54000), 
(32400, 46800), 
(36000, 46800), 
(32400, 50400), 
(32400, 50400), 
(36000, 46800), 
(36000, 54000), 
(36000, 54000), 
(32400, 61200), 
(39600, 72000), 
(43200, 72000)
]


# ******************************


# Populate graph

## Populate nodes
for node in range(INSTANCE_SIZE):
	g.add_node(node, load = load_scores[node], time_window = time_windows[node])

## Populate edges
for i in range(INSTANCE_SIZE):
	for j in range(INSTANCE_SIZE):
		cost_ij = time_matrix_array[i,j]
		g.add_edge(i,j, cost = cost_ij)


import time

# Input check
print('**********************************')
print('Nodes:')
for node in g.nodes():
	print('\t {node}'.format(node = node))
print('**********************************')
print()

input('Press [ENTER] to continue')

print('**********************************')
print('Node data:')
for node in g.nodes(data=True):
	print('\t {node}'.format(node = node))
print('**********************************')
print()

input('Press [ENTER] to continue')

print('**********************************')
print('Edge data:')
for edge in g.edges(data=True):
	print('\t {edge}'.format(edge = edge))
print('**********************************')
print()

input('Press [ENTER] to continue')


def get_time(node1, node2):
    dist = g.edge[node1][node2]['cost']
    return int(dist)


# Returns load_score (in pound) of node1
# >0 for supply nodes and <0 for demand nodes
def get_load_score(node1):
	load_score = g.node[node1]['load']
	return load_score

def get_time_window(node1):
	time_window = g.node[node1]['time_window']
	return time_window


def printRoute(route, time, fail, completion):
	if fail == 'Load':
		print("[{completion}%]	ROUTE: {route} | FAIL: Load constraint".format(completion= completion, route=route))
	elif fail == 'TimeWindow':
		print("[{completion}%]	ROUTE: {route} | \t\t\t\t FAIL: Time Window".format(completion= completion, route=route))
	elif fail == 'Success':
		print("[{completion}%]	ROUTE: {route} | \t\t\t\t\t\t\t TIME: {time}".format(completion= completion, route=route, time=time))
	else:
		print("-------------------------------------------------PROBLEM------------------------")


def gen_optimal_routes():
	
	compteur_completion	= 0

	for route in itertools.permutations(range(1, INSTANCE_SIZE)):

		compteur_completion	+= 1
		completion = round((compteur_completion/permu_size)*100,2)
		current_time = 0
		fail = False

		second_node 	= route[0]
		prev_node 		= 0
		before_last_node= route[len(route)-1]

		current_time = get_time(before_last_node, 0)
		current_load = 0
		route_builder=[0]

		for next in route:
			
			next_node = next


			# check for non-negativity of total current load
			current_load += get_load_score(next_node)
			if(current_load < 0):
				fail = 'Load'
				route_builder = [0]
				route_builder += list(route)
				route_builder.append(0)
				
				printRoute(route_builder, current_time, fail, completion)
				break

			current_time += get_time(prev_node, next_node)

			time_window_node = get_time_window(next_node)
			start_time_node = time_window_node[0]
			end_time_node = time_window_node[1]

			if(current_time > end_time_node):
				fail = 'TimeWindow'
				route_builder = [0]
				route_builder += list(route)
				route_builder.append(0)
				
				printRoute(route_builder, current_time, fail, completion)
				break

			elif(current_time < start_time_node):
				current_time = start_time_node
		
			# add node to route in the making
			route_builder.append(next_node)

			if(len(route_builder) == INSTANCE_SIZE):
				route_builder.append(0)
				fail = 'Success'
				printRoute(route_builder, current_time, fail, completion)		
				break

			prev_node = next_node

permu_size = math.factorial(INSTANCE_SIZE-1)
print("Going through all {permu_size} possible routes...\n\n".format(permu_size = permu_size))

input('Press [ENTER] to continue')

gen_optimal_routes()
