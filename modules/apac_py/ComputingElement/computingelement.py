#!/usr/bin/env python

# $ARGV[0] = clustername
# $ARGV[1] = uid from apac.pl
# $ARGV[2] = MIP config dir

import os, sys
import apac_lib as lib
import os.path, new

def minutes(pbs_time):
	(hours, minutes, seconds) = map(int, pbs_time.split(":"))
	return hours * 60 + minutes

def processNodeInfo(node_info, ce, filterArg):
	try:
		from nodeFilter import filter
		if not filter(node_info, filterArg):
			return
		
	except Exception, e:
		sys.stderr.write("error running node filter: %s\n" % e)

	if not 'state' in node_info:
		return

	if 'down' in node_info['state'] or 'offline' in node_info['state']:
		return

	if config.LRMSType == "PBSPro":
		np = int(node_info['resources_available.ncpus'][0])
	else: # we'll assume that everything will use openpbs or torque
		np = int(node_info['np'][0])
	ce.TotalCPUs += np
	ce.FreeCPUs += np

	if node_info.has_key('jobs'):
		ce.FreeCPUs -= len(node_info['jobs'])

#	for key, value in node_info.items():
#		print "%s: %s" % (key, value)


if __name__ == '__main__':

	#sys.stderr.write('in the computing element calculation\n')

	c = lib.read_config(sys.argv[3])

	lib.assert_contains(c, sys.argv[1])
	lib.assert_contains(c[sys.argv[1]], 'ComputingElement')
	lib.assert_contains(c[sys.argv[1]].ComputingElement, sys.argv[2])

	config = c[sys.argv[1]].ComputingElement[sys.argv[2]]

	ce = lib.ComputingElement()
	ce.users = []


	# caclculate the number of cpus and free cpus, ie ce.TotalCPUs and ce.FreeCPUs
	if config.LRMSType == "Torque" or config.LRMSType == "PBSPro":
		#sys.stderr.write('in the Torque / PBSPro number of cpus section\n')
		if config.pbsnodes is not None and os.path.isfile(config.pbsnodes):
			ce.TotalCPUs = 0
			ce.FreeCPUs = 0

			filterArg = None
			if hasattr(config, 'nodePropertyFilter'):
				filterArg = config.nodePropertyFilter

			node_info = {}

			lines = lib.run_command([config.pbsnodes, '-a'])
			for line in lines:
				if not line:
					processNodeInfo(node_info, ce, filterArg)
					node_info = {}
					continue

				values = line.split('=')
				if len(values) == 1:
					node_info['name'] = values[0]
				else:
					node_info[values[0].strip()] = [v.strip() for v in values[1].split(",")]
	# ANUPBS <=> OpenPBS
	#elif config.LRMSType == "ANUPBS":
	elif config.LRMSType == "OpenPBS":
		#sys.stderr.write('in the ANUPBS number of cpus section\n')
		if config.qstat is not None and os.path.isfile(config.qstat):
			lines = lib.run_command([config.qstat, '-B', '-f', config.HostName])

			for line in lines:
				#sys.stderr.write('line is : ' + line + '\n')
				if line.startswith('resources_available.ncpus'):
					#sys.stderr.write('matched line to resources_available' + '\n')
					ce.TotalCPUs = int(line.split()[-1])
					#sys.stderr.write('total cpus is calculated to be ' + str(ce.TotalCPUs) + '\n')
				if line.startswith('resources_assigned.ncpus'):
					# assumes that TotalCPUs always appears first in the command
					#sys.stderr.write('matched line to resources_assigned' + '\n')
					ce.FreeCPUs = ce.TotalCPUs - int(line.split()[-1])

	else:
		# do nothing, the LRMS type is not understood
		pass
		
	# get information about the queues and the running jobs
	# ANUPBS <=> OpenPBS
	#if config.LRMSType == "Torque" or config.LRMSType == "PBSPro" or config.LRMSType == "ANUPBS":
	if config.LRMSType == "Torque" or config.LRMSType == "PBSPro" or config.LRMSType == "OpenPBS":
		if config.qstat is not None and os.path.isfile(config.qstat):
			lines = lib.run_command([config.qstat, '-B', '-f'])

			for line in lines:
				if line.startswith('pbs_version'):
					ce.LRMSVersion = line.split()[-1]


			lines = lib.run_command([config.qstat, '-Q', '-f', config.Name])

			import socket
			hostname = socket.getfqdn()

			do_host_acl = do_user_acl = True
			user_acl_done = enabled = started = False

			for line in lines:
				if line.startswith("queue_type ="):
					if not line.split()[-1] == "Execution":
						print "Not execution queue"
						break
				elif line.startswith("acl_host_enable ="):
					if not line.split()[-1] == "True":
						do_host_acl = False
				elif line.startswith("acl_users_enable ="):
					if not line.split()[-1] == "True":
						do_user_acl = False
				elif line.startswith("acl_hosts = ") and do_host_acl:
					allowed = False
					for name in line.split("=")[1].strip().split(","):
						if name == hostname:
							allowed = True
						# wildcard
						elif hostname.endswith(name.split("*")[-1]):
							allowed = True
					# this host isn't allowed to submit!
					if not allowed:
						pass
						# wipe
#						ce = lib.ComputingElement()
#						break
				elif line.startswith("acl_users = ") and do_user_acl:
					for name in line.split("=")[1].strip().split(","):
						ce.users.append(name)
					user_acl_done = True
				elif line.startswith("enabled = "):
					if line.split()[-1] == "True":
						enabled = True
				elif line.startswith("started = "):
					if line.split()[-1] == "True":
						started = True
				elif line.startswith("max_queuable ="):
					ce.MaxTotalJobs = line.split()[-1]
				elif line.startswith("total_jobs ="):
					ce.TotalJobs = line.split()[-1]
				elif line.startswith("Priority = "):
					ce.Priority = int(line.split()[-1])
				elif line.startswith("max_running = "):
					ce.MaxRunningJobs = int(line.split()[-1])
				elif line.startswith("max_user_run = "):
					ce.MaxTotalJobsPerUser = int(line.split()[-1])
				elif line.startswith("resources_max.cput = "):
					ce.MaxCPUTime = minutes(line.split()[-1])
				elif line.startswith("resources_max.walltime = "):
					ce.MaxWallClockTime = minutes(line.split()[-1])
				elif line.startswith("state_count ="):
					ce.WaitingJobs = 0
					entries = line.split()
					for index in [3, 4, 5]:
						ce.WaitingJobs += int(entries[index].split(":")[-1])

					ce.RunningJobs = int(entries[6].split(":")[-1])

				elif line.startswith("resources_max.ncpus = "):
					ce.resources_max_ncpus = int(line.split()[-1])
				
			if enabled and started:
				# no user acl processing done, grab the list of users from the vo map
				# TODO: hmmm, this work is questionable
				# it just copies from the config to an emtpy VOView!
				ce.ACL = config.ACL
				if not user_acl_done and len(config.views) > 0:

					for viewkey in config.views.keys():
						view = lib.VOView()
						
						for key in ('DefaultSE', 'DataDir', 'RealUser'):
							if config.views[viewkey].__dict__[key] is not None:
								view.__dict__[key] = config.views[viewkey].__dict__[key]

						if len(config.views[viewkey].ACL) > 0:
							view.ACL = config.views[viewkey].ACL
							ce.ACL += view.ACL

						ce.views[viewkey] = view

				for viewkey in ce.views.keys():
					view = ce.views[viewkey]
					view.ApplicationDir = ce.ApplicationDir
					view.TotalJobs = 0
					view.RunningJobs = 0
					view.WaitingJobs = 0

					if view.RealUser is not None:

						lines = lib.run_command([config.qstat, '-u', view.RealUser, config.Name])

						import re

						select_expr = re.compile(r"^\d+")
						running_expr = re.compile(r"\d+\s+[RE]\s+")
						waiting_expr = re.compile(r"\d+\s+[QHTW]\s+")

						for line in lines:
							if select_expr.match(line):
								view.TotalJobs += 1
								if running_expr.search(line):
									view.RunningJobs += 1
								elif waiting_expr.search(line):
									view.WaitingJobs += 1

					view.FreeJobSlots = ce.FreeCPUs
					# voview's freejob slots should be maxtotaljobsperuser - running jobs (not totaljobs)
					#if ce.MaxTotalJobsPerUser and ce.FreeCPUs > ce.MaxTotalJobsPerUser - view.TotalJobs:
					#	view.FreeJobSlots = ce.MaxTotalJobsPerUser - view.TotalJobs
					if ce.MaxTotalJobsPerUser and ce.FreeCPUs > ce.MaxTotalJobsPerUser - view.RunningJobs:
						view.FreeJobSlots = ce.MaxTotalJobsPerUser - view.RunningJobs

# TODO: in pbs.pl $jobs{MaxTotalJobsPerUser} is always undefined!
#					$jobs{FreeJobSlots}=$queues{$myqueue}{MaxTotalJobsPerUser}-$jobs{TotalJobs} if defined $jobs{MaxTotalJobsPerUser} and defined $jobs{TotalJobs};
#					conf.user_info.__dict__[user].FreeJobSlots = cp.MaxTotalJobsPerUser - conf.user_info.__dict__[user].TotalJobs


	# overridable values
	for key in ['JobManager', 'ApplicationDir', 'DataDir', 'DefaultSE', 'ContactString', 'Status', 'HostName', 'GateKeeperPort', 'Name', 'LRMSType', 'LRMSVersion', 'GRAMVersion', 'TotalCPUs', 'FreeCPUs', 'RunningJobs', 'FreeJobSlots', 'TotalJobs', 'Priority', 'WaitingJobs']:
		if config.__dict__[key] is not None:
			ce.__dict__[key] = config.__dict__[key]

	# only override the Max* attributes if they are less than the default
	for key in ['MaxWallClockTime', 'MaxCPUTime', 'MaxRunningJobs', 'MaxTotalJobs']:
		if config.__dict__[key] is not None and config.__dict__[key] < ce.__dict__[key]:
			ce.__dict__[key] = config.__dict__[key]


	if ce.MaxTotalJobs is not None and ce.TotalJobs is not None:
		ce.FreeJobSlots = int(ce.MaxTotalJobs) - int(ce.TotalJobs)

	if ce.FreeCPUs < ce.FreeJobSlots:
		ce.FreeJobSlots = ce.FreeCPUs

	# print
	for key in ['JobManager', 'ApplicationDir', 'DataDir', 'DefaultSE', 'ContactString', 'Status', 'HostName', 'GateKeeperPort', 'Name', 'LRMSType', 'LRMSVersion', 'GRAMVersion', 'TotalCPUs', 'FreeCPUs', 'MaxWallClockTime', 'MaxCPUTime', 'RunningJobs', 'FreeJobSlots', 'MaxRunningJobs', 'MaxTotalJobs', 'TotalJobs', 'Priority', 'WaitingJobs']:
		if ce.__dict__[key] is not None:
			print "<%s>%s</%s>" % (str(key), str(ce.__dict__[key]), str(key))


	for viewkey in ce.views.keys():
		view = ce.views[viewkey]

		print "<VOView LocalID=\"%s\">" % viewkey

		for key in ('FreeJobSlots', 'TotalJobs', 'RunningJobs', 'WaitingJobs', 'DefaultSE', 'ApplicationDir', 'DataDir'):
			if view.__dict__[key] is not None:
				print "\t<%s>%s</%s>" % (key, view.__dict__[key], key)

		print "<FreeJobSlots>%s</FreeJobSlots>" % view.FreeJobSlots
		print "\t<ACL>"
		for rule in view.ACL:
			print "\t\t<Rule>%s</Rule>" % rule
		print "\t</ACL>"
		print "</VOView>"


	import sets

	print "<ACL>"
	for rule in sets.Set(ce.ACL):
		print "\t<Rule>%s</Rule>" % rule
	print "</ACL>"



