# DYNAMIC PROGRAMMING ALGORITHM

'''
F(s(start, end)) = 
	min(
		(
			F(s(start, prior_feasible)) +
			w(prior_feasible, end)
		)
	for prior_feasible in prior_feasibles
	)
'''


shortest_path_recursion_table = {}

NODE_COUNT = 13

def shortest_path_recursion(node_start, end_route, current_load, current_time, max_node_count = NODE_COUNT+1):
'''
starts at the end node and find by recursion the best, feasible route
'''

	node_end = end_route[0]

	# Deal with the base case:
	# The only possibility is a direct connection from node_start to node_end
	if len(end_route) == max_node_count - 1:
		# Route
		end_route = node_start + end_route
		# Time
		current_time = current_time + get_time_distance(node_start, node_end)
		# Load
		# ...
		assert len(end_route) == max_node_count, 'END ROUTE COUNT IS WRONG : {node_count}'.format(node_count = len(end_route))
		return (end_route, current_time)

	# Deal with recursion
	else:
		# Define which are the remaining and feasible nodes
		prior_feasibles = []
		for node in nodes:
			if node not in end_route and current_load + get_load_score(node) < 0:
				prior_feasibles.append(node)

		# Recursive call
		for prior_node in prior_feasibles:
			case = (prior_node, end_route)
			if case in shortest_path_recursion_table:
				return shortest_path_recursion_table[case]
			else:
				shortest_path_recursion_table[case] = shortest_path_recursion(prior_node, end_route, current_load, current_time)
				return shortest_path_recursion_table[case]




# OBJECTIVES:
# Find way to be memory efficient by dropping keys when they become irrelevant
# Find how to process the output (store in `optimal_route_stack` probably)
