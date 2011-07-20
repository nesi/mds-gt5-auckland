#!/usr/bin/env python

# $ARGV[0] = clustername 
# $ARGV[1] = uid from apac.pl
# $ARGV[2] = MIP config dir

import os, sys
import apac_lib as lib

if __name__ == '__main__':
	c = lib.read_config(sys.argv[3])

	lib.assert_contains(c, sys.argv[1])
	lib.assert_contains(c[sys.argv[1]], 'SubCluster')
	lib.assert_contains(c[sys.argv[1]].SubCluster, sys.argv[2])

	config = c[sys.argv[1]].SubCluster[sys.argv[2]]


	if config.Processor is not None:
		processor = lib.Processor()

		# do file first
		if config.Processor.File is not None:
			f = file(config.Processor.File)
			contents = [line.strip() for line in f.readlines()]

			cpuinfo = {'vendor':'vendor_id', 'model':'model name', 'flags':'flags', 'speed':'cpu MHz'}
			if config.Processor.FileType == 'SGI_Altix':
				cpuinfo = {'vendor':'vendor', 'model':'family', 'flags':'features', 'speed':'cpu MHz'}
			for line in contents:
				if line.startswith(cpuinfo['vendor']):
					processor.Vendor = " ".join(line.split()[2:])
				elif line.startswith(cpuinfo['model']):
					processor.Model = " ".join(line.split()[3:])
				elif line.startswith(cpuinfo['flags']):
					processor.InstructionSet = " ".join(line.split()[2:])
				elif line.startswith(cpuinfo['speed']):
					processor.ClockSpeed = line.split()[-1].split(".")[0]

		# override with specific values
		for key in ('Vendor', 'Model', 'ClockSpeed', 'InstructionSet'):
			if config.Processor.__dict__[key] is not None:
				processor.__dict__[key] = config.Processor.__dict__[key]


	if config.MainMemory is not None:
		memory = lib.MainMemory()

		# do file first
		if config.MainMemory.File is not None:
			f = file(config.MainMemory.File)
			contents = [line.strip() for line in f.readlines()]

			ramsize = 0

			# NOTE: this relies on order in the file
			# - ramsize is used to calculate VirtualSize
			for line in contents:
				if line.startswith('MemTotal'):
					ramsize = memory.RAMSize = int(line.split()[-2]) / 1024
				elif line.startswith('SwapTotal'):
					memory.VirtualSize = int(line.split()[-2]) / 1024 + ramsize

		# override with specific values
		for key in ('RAMSize', 'VirtualSize'):
			if config.MainMemory.__dict__[key] is not None:
				memory.__dict__[key] = config.MainMemory.__dict__[key]


	if config.OperatingSystem is not None:
		os_ = lib.OperatingSystem()

		# do file first
		if config.OperatingSystem.File is not None:
			if os.path.isfile(config.OperatingSystem.File):
				lines = lib.run_command([config.OperatingSystem.File, '-a'])
				
				for line in lines:
					if line.startswith('Distributor'):
						os_.Release = " ".join(line.split()[2:])
					elif line.startswith('Description'):
						os_.Name = " ".join(line.split()[1:])
					elif line.startswith('Release'):
						os_.Version = " ".join(line.split()[1:])

		# override with specific values
		for key in ('Release', 'Name', 'Version'):
			if config.OperatingSystem.__dict__[key] is not None:
				os_.__dict__[key] = config.OperatingSystem.__dict__[key]


#	if type(config.OperatingSystem) == type(""):
#		if os.path.isfile(config.OperatingSystem):
#			lines = lib.run_command([config.OperatingSystem, '-a'])
#
#			os = config.OperatingSystem = lib.Config()
#
#			for line in lines:
#				if line.startswith('Distributor'):
#					os.Release = " ".join(line.split()[2:])
#				elif line.startswith('Description'):
#					os.Name = " ".join(line.split()[1:])
#				elif line.startswith('Release'):
#					os.Version = " ".join(line.split()[1:])


	print "<Name>%s</Name>" % sys.argv[2]

	# standard glue keys
	for key in ('PhysicalCPUs', 'LogicalCPUs', 'TmpDir', 'WNTmpDir'):
		if lib.contains(config, key):
			print "<%s>%s</%s>" % (key, config.__dict__[key], key)

	sys.stdout.write("<Processor ")
	for key in ('Model', 'ClockSpeed', 'Vendor', 'InstructionSet'):
		if processor.__dict__[key] is not None:
			sys.stdout.write("%s=\"%s\" " % (key, processor.__dict__[key]))
	print "/>"

	sys.stdout.write("<MainMemory ")
	for key in ('VirtualSize', 'RAMSize'):
		if memory.__dict__[key] is not None:
			sys.stdout.write("%s=\"%s\" " % (key, memory.__dict__[key]))
	print "/>"

	sys.stdout.write("<OperatingSystem ")
	for key in ('Name', 'Release', 'Version'):
		if os_.__dict__[key] is not None:
			sys.stdout.write("%s=\"%s\" " % (key, os_.__dict__[key]))
	print "/>"

	sys.stdout.write("<Architecture ");
	for key in ('PlatformType', 'SMPSize'):
		if lib.contains(config, key):
			sys.stdout.write("%s=\"%s\" " % (key, config.__dict__[key]))
	print "/>"

	# TODO: check if these attributes are mandatory in glue and adjust
	sys.stdout.write("<NetworkAdapter ");
	for key in ('InboundIP', 'OutboundIP'):
		if lib.contains(config, key):
			sys.stdout.write("%s=\"%s\" " % (key, str(config.__dict__[key]).lower()))
	print "/>"

