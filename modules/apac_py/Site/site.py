#!/usr/bin/env python

# $ARGV[0] = clustername
# $ARGV[1] = uid from apac.pl
# $ARGV[2] = MIP config dir

import os, sys, copy
import apac_lib as lib

if __name__ == '__main__':

	c = lib.read_config(sys.argv[3])

	lib.assert_contains(c, sys.argv[1])
	lib.assert_contains(c[sys.argv[1]], 'Site')
	lib.assert_contains(c[sys.argv[1]].Site, sys.argv[2])
		
	config = c[sys.argv[1]].Site[sys.argv[2]]
	c = copy.deepcopy(config)

	# standard glue keys
	if lib.contains(config, 'Contact'):
		for key in ('SysAdminContact', 'UserSupportContact', 'SecurityContact'):
			c.__dict__[key] = config.__dict__['Contact']
	
	for key in ('SysAdminContact', 'UserSupportContact', 'SecurityContact'):
		if lib.contains(config, key) and config.__dict__[key] is not None:
			c.__dict__[key] = config.__dict__[key]

	for key in ('Name', 'Description', 'Web', 'Location', 'Latitude', 'Longitude', 'SysAdminContact', 'UserSupportContact', 'SecurityContact'):
		if lib.contains(c, key):
			print "<%s>%s</%s>" % (key, c.__dict__[key], key)

	for key in ('Sponsor', 'OtherInfo'):
		if lib.contains(c, key) and len(c.__dict__[key]) > 0:
			for value in c.__dict__[key]:
				print "<%s>%s</%s>" % (key, value, key)

