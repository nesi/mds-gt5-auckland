#!/usr/bin/env python

# $ARGV[0] = clustername
# $ARGV[1] = uid from apac.pl
# $ARGV[2] = MIP config dir

import os, sys
import apac_lib as lib

if __name__ == '__main__':
	c = lib.read_config(sys.argv[3])

	lib.assert_contains(c, sys.argv[1])
	lib.assert_contains(c[sys.argv[1]], 'StorageElement')
	lib.assert_contains(c[sys.argv[1]].StorageElement, sys.argv[2])

	config = c[sys.argv[1]].StorageElement[sys.argv[2]]

	# vlad's workaround to the max limit of int32
	maxInt32 = 2147483647

	if config.RootDirectory is not None and os.path.exists(config.RootDirectory):
		lines = lib.run_command(['df', '-k', config.RootDirectory])
		if len(lines) == 3:
			free_index = 2
			total_index = 0
		else:
			free_index = 3
			total_index = 1
		if config.SizeTotal is None:
			total_space = int(lines[-1].split()[total_index])
			if total_space > 0:
				if total_space <= maxInt32:
					config.SizeTotal = total_space
				else:
					config.SizeTotal = maxInt32
		if config.SizeFree is None:
			free_space = int(lines[-1].split()[free_index])
			if free_space > 0:
				if free_space <= maxInt32:
					config.SizeFree = free_space
				else:
					config.SizeFree = maxInt32

	for key in ['SizeTotal', 'SizeFree', 'Architecture']:
		if config.__dict__[key] is not None:
			print "<%s>%s</%s>" % (key, config.__dict__[key], key)

	# standard glue keys
	for area_key in config.areas.keys():
		area = config.areas[area_key]

		print "<StorageArea LocalID=\"%s\">" % area_key

		# work out free/used space
		if area.Path is not None and os.path.exists(area.Path):
			lines = lib.run_command(['df', '-k', area.Path])

			if len(lines) == 3:
				free_index = 2
				used_index = 1
			else:
				free_index = 3
				used_index = 2

			# config file overrides this
			if area.AvailableSpace is None:
#				free_space = int(lines[-1].split()[3])
				free_space = int(lines[-1].split()[free_index])
				if free_space > 0:
					if free_space <= maxInt32:
						area.AvailableSpace = free_space
					else:
						area.AvailableSpace = maxInt32

			# config file overrides this
			if area.UsedSpace is None:
#				used_space = int(lines[-1].split()[2])
				used_space = int(lines[-1].split()[used_index])
				if used_space > 0:
					if used_space <= maxInt32:
						area.UsedSpace = used_space
					else:
						area.UsedSpace = maxInt32


		if area.VirtualPath is not None:
			print "\t<Path>%s</Path>" % area.VirtualPath
		else:
			print "\t<Path>%s</Path>" % area.Path

		for key in ['Type', 'AvailableSpace', 'UsedSpace']:
#			if lib.contains(area, key):
			if area.__dict__[key] is not None:
				print "\t<%s>%s</%s>" % (key, area.__dict__[key], key)

		print "\t<ACL>"

		for acl in area.ACL:
			print "\t\t<Rule>%s</Rule>" % acl

		print "\t</ACL>"

		print "</StorageArea>"

	for protocol_key in config.access_protocols.keys():
		protocol = config.access_protocols[protocol_key]

		print "<AccessProtocol LocalID=\"%s\">" % protocol_key

		for key in ['Endpoint', 'Type', 'Version']:
#			if lib.contains(protocol, key):
			if protocol.__dict__[key] is not None:
				print "\t<%s>%s</%s>" % (key, protocol.__dict__[key], key)

#		if lib.contains(protocol, 'Capability'):
		for capability in protocol.Capability:
			print "\t<Capability>%s</Capability>" % capability

		print "</AccessProtocol>"

	for protocol_key in config.control_protocols.keys():
		protocol = config.control_protocols[protocol_key]
		print "<ControlProtocol LocalID=\"%s\">" % protocol_key
		for key in ['Endpoint', 'Type', 'Version']:
			if protocol.__dict__[key] is not None:
				print "\t<%s>%s</%s>" % (key, protocol.__dict__[key], key)
		for capability in protocol.Capability:
			print "\t<Capability>%s</Capability>" % capability
		print "</ControlProtocol>"



