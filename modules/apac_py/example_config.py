#~ For instructions on how configure the mip see twiki page
#~ http://www.vpac.org/twiki/bin/view/APACgrid/ConfigureAPACInfoServiceProvider. When referred to 
#~ a twiki page in this document, it means this page

#~ The configuration is divided in to X main segments

#~ Package 
	#~ Site
	#~ Cluster (M)
		#~ Computing element (M)
			#~ VOView (M)
		#~ Subcluster (M)
			#~ Processor 
			#~ Memory
			#~ Operating system
	#~ Storage Element (M)
		#~ Area (M)
		#~ Protocol (M)


#~ The items with a (M) next to them can be multiple instances in a single configuration. 
#~ For example there maybe 3 subcluster in a single cluster, or many VOViews in a computing element

#~ Below is the minimum configuration options possible. If your site does have multiple instances of the 
#~ items above fileX which contains ready made duplicates of each element may be useful to you. 

###############

# changelog:
# * APAC-mip-module-py-1.0.384-1, Gerson Galang, 11 Dec 2007
#   - added support for publishing SRM information
#   - added support publishing ComputeElement.GRAMVersion
#   - an instance of 'protocols' which used to refer to SE.AccessProtocol is now access_protocols. 
#     SE.ControlProtocols can be published using control_protocols
#   - default version of GridFTP protocol has been corrected
#   - removed ANUPBS from list of LRMSTypes as it is not supported by GLUE Schema 1.2
#   - ComputeElement.Status' default value is now Production
# * version APAC-mip-module-py-1.0.374-1, Andrew Sharpe
#   - initial release




# package name : this name must be the same as in pkgs in source.pl
# there is only one package per configuration file
package = config['default'] = Package()

# This name will be used as the name of another configuration file, in this case the file would be called default.pl.  
# This config file will be referred to as package.pl in the rest of these comments. See twiki page for more details.


###############


# SITE INFORMATION
# There can only be one site in a configuration
# this is the name defined in site line in package.pl
# see twiki page for further details on this section
site = package.Site['TEST'] = Site()
 
site.Name = 'ExampleSite'
site.Description = 'An example site'
site.OtherInfo = ['some info', 'other info']
site.Web = 'http://example.apac.site'

site.Sponsor = [ 'sponsor 1', 'sponsor 2' ]
site.Location = 'Town, Country'
site.Latitude = '0'
site.Longitude = '0'

# if you set Contact the you don't need to set the others
site.Contact = 'mailto:support@example.apac.site'
#site.SysAdminContact = 'mailto:admin@example.apac.site'
#site.SecurityContact = 'mailto:security@example.apac.site'
#site.UserSupportContact = 'mailto:support@example.apac.site'


###############

# CLUSTER
# this name is defined in cluster line in package.pl
# see twiki page for further details on this section
cluster = package.Cluster['cluster1'] = Cluster()
 
cluster.Name = 'clusterhostname'
cluster.WNTmpDir = '/working/tmp/dir'
cluster.TmpDir = '/std/tmp/dir'

####

# COMPUTING ELEMENT
# this name is defined in computing element of package.pl
# see twiki page for further details on this section
computeElement = package.ComputingElement['compute1'] = ComputingElement()

#computeElement.nodePropertyFilter = 'property'
computeElement.Name = 'queue_name'
computeElement.Status = 'Production'
computeElement.JobManager = 'jobmanager-pbs'
computeElement.HostName = 'ng2.example.apac.site'
computeElement.GateKeeperPort = 8443
computeElement.ContactString = 'ng2.hostname/jobmanager-pbs' # or if WSGRAM, https://ng2.hostname:8443/wsrf/services/ManagedJobFactoryService
computeElement.DefaultSE = 'ngdata.example.apac.site'
computeElement.ApplicationDir = 'UNAVAILABLE'
computeElement.DataDir = cluster.TmpDir
computeElement.LRMSType = 'Torque' # Torque|PBSPro|OpenPBS
computeElement.GRAMVersion = '4.0.5'

computeElement.qstat = '/usr/bin/qstat'
computeElement.pbsnodes = '/usr/bin/pbsnodes'

# this information can be retrieved from your LRMS (if defined)
#computeElement.MaxTotalJobs = 9999999
#computeElement.MaxRunningJobs = 9999999
#computeElement.MaxCPUTime = 9999999
#computeElement.MaxWallClockTime = 9999999
#computeElement.MaxTotalJobsPerUser = 9999999

# you can define these if you want, but it's not advised
#computeElement.LRMSVersion = '2.1.4'
#computeElement.Priority = 1
#computeElement.FreeCPUs = 1
#computeElement.TotalCPUs = 1
        
#computeElement.WaitingJobs = 0
#computeElement.RunningJobs = 0
#computeElement.TotalJobs = 0
#computeElement.FreeJobSlots = 0

#computeElement.ACL = [ '/VO3', '/VO4' ]


# VOVIEW
# this name is defined must be unique for each voview in the computing element. It is not refered to anywhere else
# see twiki page for further details on this section
voview = computeElement.views['view1'] = VOView()

# the RealUser is used in working out the job information for the VOView, ie WaitingJobs, TotalCPUs, etc
# it should be retrieved from GUMS in the future
voview.RealUser = 'grid-admin'
voview.DefaultSE = 'ngdata.example.apac.site'
voview.DataDir = '/path/to/area1'
voview.ACL = [ '/VO1', '/VO2' ]
# /VOVIEW

# /COMPUTING ELEMENT

####

# SUBCLUSTER
# this name is defined in the subcluser line in package.pl 
# see twiki page for further details on this section
subcluster = package.SubCluster['sub1'] = SubCluster()
 
subcluster.InboundIP = False
subcluster.OutboundIP = True
subcluster.PlatformType = ''
subcluster.SMPSize = 1

subcluster.PhysicalCPUs = 128
subcluster.LogicalCPUs = 128
subcluster.WNTmpDir = cluster.WNTmpDir
subcluster.TmpDir = cluster.TmpDir


# PROCESSOR
# each subcluster has one cpu reference
# see twiki page for further details on this section
subcluster.Processor = Processor()
subcluster.Processor.File = '/proc/cpuinfo'
# if you want to override any values, just uncomment
#subcluster.Processor.Model = 'prossy model'
#subcluster.Processor.Vendor = 'prossy vendor'
#subcluster.Processor.ClockSpeed = 10000
#subcluster.Processor.InstructionSet = 'fpu tsc msr pae mce cx8 apic mtrr mca'

# MAIN MEMORY
# each subcluster has one memory reference
# see twiki page for further details on this section
subcluster.MainMemory = MainMemory()
subcluster.MainMemory.File = '/proc/meminfo'
# uncomment to override
#subcluster.MainMemory.RAMSize = 1024
#subcluster.MainMemory.VirtualSize = 3072

# OPERATING SYSTEM
# each subcluster has one OS reference
# see twiki page for further details on this section
subcluster.OperatingSystem = OperatingSystem()
subcluster.OperatingSystem.File = '/usr/bin/lsb_release'
#subcluster.OperatingSystem.Name = 'OS of your choice'
#subcluster.OperatingSystem.Release = 'hopefully recent'
#subcluster.OperatingSystem.Version = '1.0.0'
# /SUBCLUSTER

# /CLUSTER

###############

# STORAGE ELEMENT
# this name is defined in the storage element line package.pl
# see twiki page for further details on this section
storageElement = package.StorageElement['storage1'] = StorageElement()

# the value of this field usually is the root directory of all the storage area locations
# most of the time this directory will be mounted from another host and is made available
# on the grid gateway host
storageElement.RootDirectory = '/path/to/root/of/area/dir'

# can be disk, tape, multidisk, or other
storageElement.Architecture = 'disk'

# STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
area = storageElement.areas['area1'] = StorageArea()
 
area.Path = '/path/to/area1'
area.Type = 'volatile'
area.ACL = [ '/VO1', '/VO2' ]
# /STORAGE ELEMENT AREA


# SECOND STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
area = storageElement.areas['area2'] = StorageArea()
 
area.Path = '/path/to/area2'
area.Type = 'volatile'
area.ACL = [ '/VO3', '/VO4' ]
# /SECOND STORAGE ELEMENT AREA


# STORAGE ELEMENT ACCESS PROTOCOL
# this name must be unique for each protocol in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
accessProtocol = storageElement.access_protocols['prot1'] = AccessProtocol()

accessProtocol.Type = 'gsiftp'
accessProtocol.Version = '2.3'
accessProtocol.Endpoint = 'gsiftp://ngdata.example.apac.site:2811'
accessProtocol.Capability = [ 'file transfer', 'other capability' ]
# /STORAGE ELEMENT ACCESS PROTOCOL

# SECOND STORAGE ELEMENT ACCESS PROTOCOL
#accessProtocol = storageElement.access_protocols['prot2'] = AccessProtocol()
#accessProtocol.Type = 'gsiftp'
#accessProtocol.Version = '2.3'
#accessProtocol.Endpoint = 'gsiftp://ng2.example.apac.site:2811'
#accessProtocol.Capability = [ 'file transfer', 'other capability' ]
# /SECOND STORAGE ELEMENT ACCESS PROTOCOL

# /STORAGE ELEMENT

# ANOTHER STORAGE ELEMENT EXAMPLE FOR AN SRM ENABLED HOST
#storageElement = package.StorageElement['storage2'] = StorageElement()

# the value of this field usually is the root directory of all the storage area locations
# most of the time this directory will be mounted from another host and is made available
# on the grid gateway host
#storageElement.RootDirectory = '/path/to/root/of/area/dir'

# can be disk, tape, multidisk, or other
#storageElement.Architecture = 'tape'

# STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
#area = storageElement.areas['area1'] = StorageArea()

# VirtualPath is the actual directory published for SRM enabled Storage Elements
#area.VirtualPath = '/pnfs/hostname/path/to/virtual/area'
# the Path attribute will be where the actual files will be stored so the 'du' or 'df' can
# be run on it
#area.Path = '/path/to/area1'
#area.Type = 'permanent'
#area.ACL = [ '/VO1', '/VO2' ]
# /STORAGE ELEMENT AREA

# STORAGE ELEMENT CONTROL PROTOCOL
# this name must be unique for each protocol in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
#controlProtocol = storageElement.control_protocols['prot1'] = ControlProtocol()

#controlProtocol.Type = 'srm'
#controlProtocol.Version = '2.1'
#controlProtocol.Endpoint = 'srm://srm.example.apac.site:8443'
#controlProtocol.Capability = [ 'file transfer', 'other capability' ]
# /STORAGE ELEMENT CONTROL PROTOCOL

# /ANOTHER STORAGE ELEMENT EXAMPLE FOR AN SRM ENABLED HOST
