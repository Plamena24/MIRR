#!/usr/bin/env python

import csv
import numpy as np
import scipy
import scipy.sparse
import scipy.sparse.csgraph as csgraph

import sys

file_name = 'hopcount.h'

'''
Compute the node-to-node spreading effect. The basic idea is to take a 
hand-entered adjacency matrix and compute the shortest path between each node
(also stored as a matrix). The adjacency matrix is enough data that the logic
for writing the effect itself is then simple. To get it into the code we
generate a C++ header file.
'''

# Load the data
l = list(csv.reader(open('diamondAdjacency.csv'), quoting=csv.QUOTE_NONE))
l2 = [[int('0'+y) for y in x] for x in l]  # to convert strings and empty to int
a = np.array(l2)
g = csgraph.csgraph_from_dense(a, 0)
#import code; code.interact(local=locals())

# Generate a new matrix with the shortest paths between nodes.
shortest_paths = csgraph.shortest_path(g, directed=False)


out_file = open(file_name, 'w')
#out_file = sys.stdout

out_file.write(
'''#ifndef __hopcount_h
#define __hopcount_h

const unsigned char HOPCOUNTS[%d][%d] = {
''' % shortest_paths.shape)

for row in shortest_paths:
	out_file.write('  ')
	for entry in row:
		val = -1
		try:
			val = int(entry)
		except:
			pass
		out_file.write("%2d" % val)
		out_file.write(', ')
	out_file.write('\n')

out_file.write('''};

#endif
''')

out_file.close()

print("Generated hopcount matrix in '%s' with shape %s" % (file_name, str(shortest_paths.shape)))
