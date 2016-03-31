# Access path
access_path = '/home/eolus/Dropbox/610 Project Data'

# Model Parameters
TIME_LIMIT = 4 * 3600

# Libraries
import itertools
import pickle
import numpy as np
import math

# Instantiate network

import networkx as nx

print('Building network...')

g = nx.Graph()

g.graph['title'] 	= 'Transportation Network v1'
g.graph['author']	= 'Eole CERVENKA'
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
10,
10,
10,
10,
10,
10,
10,
-10,
10,
-10,
10,
-10,
10
]
# ******************************


# Populate graph

## Populate nodes
for node in range(INSTANCE_SIZE):
	g.add_node(node, load = load_scores[node])

## Populate edges
for i in range(INSTANCE_SIZE):
	for j in range(INSTANCE_SIZE):
		cost_ij = time_matrix_array[i,j]
		g.add_edge(i,j, cost = cost_ij)


# Input check
print('**********************************')
print('Nodes:')
for node in g.nodes():
	print('\t {node}'.format(node = node))
print('**********************************')
print()

print('**********************************')
print('nodes w data:')
for node in g.nodes(data=True):
	print('\t {node}'.format(node = node))
print('**********************************')
print()


print('**********************************')
print('edges w data:')
for edge in g.edges(data=True):
	print('\t {edge}'.format(edge = edge))
print('**********************************')
print()



# Dynamic programming memoize function
def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


@memoize
def get_time(node1, node2):
    """Returns time-distance between two nodes, memoizes result"""
    dist = g.edge[node1][node2]['cost']
    return int(dist)


# Returns load_score (in pound) of node1
# >0 for supply nodes and <0 for demand nodes
def get_load_score(node1):
	load_score = g.node[node1]['load']
	return load_score

# Returns True if load_score of node1 >0, false otherwise
def is_supply(node1):
	if get_load_score(node1) > 0:
		return True
	return False


stack_size = 5
# List of best routes found: [(route, time), (route, time), (route, time)]
solution_stack = []

def update_stack(stack, input, time_limit):
	if len(stack) < stack_size:
		stack.append(input)
	elif input[1] < time_limit:
		stack.pop()
		stack.append(input)
		stack = sorted(stack, key=lambda route: route[1])   # sort by desc time
		time_limit = stack[-1][1]
	return stack, time_limit

def gen_optimal_routes(route_stack, time_limit):

	route_stack = []
	time_limit = 999999999999999

	# Keep track of progress
	permu_size = math.factorial(INSTANCE_SIZE-1)
	compteur_completion	= 1

	for route in itertools.permutations(range(1, INSTANCE_SIZE)):
		
		compteur_completion	+= 1
		second_node 	= route[1]
		prev_node 		= 0
		before_last_node= route[len(route)-1]

		#How much do we load to last (demand) node?
		remaining_extra_load = 0

		print('COMPLETE: {completion}%'.format(completion = round((compteur_completion/permu_size)*100,2)))

		if not is_supply(second_node) or is_supply(before_last_node):
			continue

		else:
			current_time 	= get_time(before_last_node, 0)
			current_load	= 0
			route_builder = [0]

			for next in route:
				
				# check for non-negativity of total current load
				current_load += get_load_score(next)
				if(current_load < 0):
					break

				# check for time constraint
				current_time += get_time(prev_node, next)
				if(current_time > time_limit):
					break
				
				# add node to route in the making
				route_builder.append(next)

				if(len(route_builder) == INSTANCE_SIZE -1):
					route_builder.append(0)
					remaining_extra_load = current_load

					route_stack, time_limit = update_stack(route_stack, route_builder, time_limit)

					print('ROUTE: {route} | TIME: {time} | {completion}% '\
						.format(route = route_builder, time = current_time, completion = round((compteur_completion/permu_size)*100,2) ))
					continue

				prev_node = next

	return route_stack

solution_stack = gen_optimal_routes(solution_stack, TIME_LIMIT)
print('OPTIMAL ROUTE: {routes}'.format(routes = solution_stack ))
