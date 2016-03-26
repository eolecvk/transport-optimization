# Access path
access_path = '/home/eolus/Dropbox/610 Project Data'

# Model Parameters
TIME_LIMIT = 1.9 * 3600

# Libraries
import itertools
import pickle
import numpy as np
import math


# Input

# Time matrix
time_matrix_array = pickle.load( open(access_path + '/time_matrix.pkl', 'rb') )

assert(time_matrix_array.shape[0] == time_matrix_array.shape[1]), \
	"Time matrix is not square: {columns} columns // {rows} rows".format(columns = time_matrix_array.shape[0], rows = time_matrix_array.shape[1])

INSTANCE_SIZE = time_matrix_array.shape[0]


# Supply/Demand parameters
# NODES = { mode_k: supply_node_k }

NODES =
{
	0:	0
	1: 	10
	2: 	-10
	3:	10
	4:	-10
	5:	10
	6:	-10
	7:	10
	8:	-10
	9:	10
	10: -10
	11:	10
	12:	-10
	13:	10
}


# Helper functions 
def memorize(f):
    """ Memorization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

@memorize
def get_time(p1, p2):
    """Returns time-distance between two nodes, memorizes result"""
    d = time_matrix_array[p1-1,p2-1]
    return int(d)



def find_optimal_routes():
	"""Find shortest route of length route_length from nodes."""   

	optimal_routes = list()

	i = 0

	for route in itertools.permutations(range(2, INSTANCE_SIZE+1)):
		i += 1
		prev_node 		= 1
		before_last_node= route[len(route)-1]
		current_time 	= get_time(before_last_node, 1)

		for next in route:
			current_time += get_time(prev_node, next)

			if(current_time > TIME_LIMIT):
				break
			prev_node = next

		route_loop = [1]
		for node in route:
			route_loop.append(node)
		route_loop.append(1)

		if (current_time < TIME_LIMIT):
			print('ROUTE: {route} | TIME: {time}'.format(route = route_loop, time = current_time)
			optimal_routes.append(route_loop)
				
	return optimal_routes


route_options = find_optimal_routes()
