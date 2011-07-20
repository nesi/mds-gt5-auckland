import os, sys

class Package:
	def __init__(self):
		self.Site = {}
		self.Cluster = {}
		self.ComputingElement = {}
		self.SubCluster = {}
		self.StorageElement = {}

class Site:
	def __init__(self):
		self.Name = ""
		self.Description = ""
		self.OtherInfo = []
		self.Web = ""
		self.Sponsor = []
		self.Location = ""
		self.Longitude = ""
		self.Latitude = ""

		self.SysAdminContact = None
		self.SecurityContact = None
		self.UserSupportContact = None

		# using this value sets defaults for the above 3, but each is overwritten
		# if defined directly
		self.Contact = None

class Cluster:
	def __init__(self):
		self.Name = None
		self.WNTmpDir = ""
		self.TmpDir = ""

class StorageElement:
	def __init__(self):
		self.RootDirectory = None
		self.SizeTotal = None
		self.SizeFree = None
		self.Architecture = None
		self.areas = {}
		self.access_protocols = {}
		self.control_protocols = {}

class StorageArea:
	def __init__(self):
		self.Path = None
		self.VirtualPath = None
		self.Type = None
		self.AvailableSpace = None
		self.UsedSpace = None
		self.ACL = []

class AccessProtocol:
	def __init__(self):
		self.Type = ""
		self.Version = ""
		self.Endpoint = ""
		self.Capability = []

class ControlProtocol:
	def __init__(self):
		self.Type = ""
		self.Version = ""
		self.Endpoint = ""
		self.Capability = []

class ComputingElement:
	def __init__(self):
		# this is queue name
		self.Name = None
		self.Status = None # Production|Queueing|Draining|Closed
		self.JobManager = None
		self.HostName = None
		self.GateKeeperPort = None
		self.ContactString = None
		self.DefaultSE = None # match UniqueID of SE?
		self.ApplicationDir = None
		self.DataDir = None
		# standard VO ACL
		self.ACL = []

		self.LRMSType = None # Torque | PBSPro
		self.LRMSVersion = None
		
		self.GRAMVersion = None

		# a list of VOViews
		self.views = {}

		# us absolute paths
		self.qstat = None
		self.pbsnodes = None

		# TODO: enumerate all of these (in case above paths aren't used)
		self.Priority = None
		self.MaxTotalJobs = 9999999
		self.MaxRunningJobs = 9999999
		self.MaxCPUTime = 9999999
		self.MaxWallClockTime = 9999999
		self.MaxTotalJobsPerUser = 9999999

		self.WaitingJobs = None
		self.TotalCPUs = None
		self.FreeCPUs = None
		self.FreeJobSlots = None
		self.RunningJobs = None
		self.TotalJobs = None

class VOView:
	def __init__(self):
		self.RealUser = None
		self.DefaultSE = None
		self.DataDir = None
		self.ApplicationDir = None
		self.ACL = []

		self.RunningJobs = None
		self.WaitingJobs = None
		self.TotalJobs = None
		self.FreeJobSlots = None

class SubCluster:
	def __init__(self):
		self.Name = ""
		self.InboundIP = False
		self.OutboundIP = False
		self.PlatformType = ""
		self.SMPSize = 1

		self.PhysicalCPUs = 1
		self.LogicalCPUs = 1
		self.WNTmpDir = ""
		self.TmpDir = ""

		self.Processor = None
		self.MainMemory = None
		self.OperatingSystem = None

class Processor:
	def __init__(self):
		self.Model = None
		self.ClockSpeed = None
		self.Vendor = None
		self.InstructionSet = None

		self.File = None
		self.FileType = None

class MainMemory:
	def __init__(self):
		self.RAMSize = None
		self.VirtualSize = None

		self.File = None

class OperatingSystem:
	def __init__(self):
		self.Name = None
		self.Release = None
		self.Version = None

		self.File = None
		
default_config = """
config['example'] = Package()
config['example'].Site['site1'] = Site()
config['example'].Cluster['cluster1'] = Cluster()
config['example'].SubCluster['sub1'] = SubCluster()
config['example'].ComputingElement['compute1'] = ComputingElement()
config['example'].StorageElement['storage1'] = StorageElement()
"""

def read_config(config_path):
	config_file = os.path.join(config_path, "apac_config.py")
	config = {}
	try: 
		#print "reading config from %s" % config_file
		execfile(config_file)
	except Exception, e:
		sys.stderr.write("error reading config file: %s\n" % e)
		sys.stderr.write("using builtin config\n")
		exec default_config

	return config

def has_config(config, key):
	return contains(config, key)

def contains(object, key):
	if type(object) == type({}):
		return object.has_key(key)
	elif hasattr(object, '__dict__'):
		return object.__dict__.has_key(key)

def assert_contains(object, key):
	if not contains(object, key):
		sys.stderr.write("%s doesn't contain %s\n" % (object, key))
		sys.exit()

def run_command(command):
#	print command
	version = sys.version.split()[0].split(".")

	if map(int, version) >= [2, 4]:
		from subprocess import Popen, PIPE
		if type(command) == type(""):
			stdout = Popen([command], stdout=PIPE).communicate()[0]
			return [l.strip() for l in stdout.splitlines()]
		else:
			stdout = Popen(command, stdout=PIPE).communicate()[0]
			return [l.strip() for l in stdout.splitlines()]

	else:
		if type(command) == type(""):
			return [l.strip() for l in os.popen2(command)[1].readlines()]
		else:
			return [l.strip() for l in os.popen2(" ".join(command))[1].readlines()]

