import sys

def filter(node_info, property):
	passed = True
	if node_info.has_key('properties') and property:
		passed = property in node_info['properties']

	# other tests

	return passed

