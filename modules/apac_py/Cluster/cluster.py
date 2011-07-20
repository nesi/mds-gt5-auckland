#!/usr/bin/env python


# $ARGV[0] = clustername
# $ARGV[1] = uid from apac.pl
# $ARGV[2] = MIP config dir

import os, sys
import apac_lib as lib

if __name__ == '__main__':

	c = lib.read_config(sys.argv[3])

	lib.assert_contains(c, sys.argv[1])
	lib.assert_contains(c[sys.argv[1]], 'Cluster')
	lib.assert_contains(c[sys.argv[1]].Cluster, sys.argv[2])

	config = c[sys.argv[1]].Cluster[sys.argv[2]]
		
	# standard glue keys
	for key in ('WNTmpDir', 'TmpDir'):
		if lib.contains(config, key):
			print "<%s>%s</%s>" % (key, config.__dict__[key], key)

	if lib.contains(config, 'Name') and config.__dict__['Name'] is not None:
		print "<Name>%s</Name>" % config.__dict__['Name']
	else:
		print "<Name>%s</Name>" % sys.argv[2]

