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
package = config['gram5.ceres.auckland.ac.nz'] = Package()

# This name will be used as the name of another configuration file, in this case the file would be called default.pl.  
# This config file will be referred to as package.pl in the rest of these comments. See twiki page for more details.


###############


# SITE INFORMATION
# There can only be one site in a configuration
# this is the name defined in site line in package.pl
# see twiki page for further details on this section
site = package.Site['auckland.ac.nz'] = Site()
 
site.Name = 'Auckland'
site.Description = 'Auckland''s BeSTGRID'
site.OtherInfo = ['', '']
site.Web = 'http://www.bestgrid.org'

site.Sponsor = [ 'ITS']
site.Location = 'Auckland, New Zealand'
site.Latitude = '-36.853'
site.Longitude = '174.768'

# if you set Contact the you don't need to set the others
site.Contact = 'mailto:eresearch-admin@list.auckland.ac.nz'
#site.SysAdminContact = 'mailto:admin@example.apac.site'
#site.SecurityContact = 'mailto:security@example.apac.site'
#site.UserSupportContact = 'mailto:support@example.apac.site'


###############

# CLUSTER
# this name is defined in cluster line in package.pl
# see twiki page for further details on this section
cluster = package.Cluster['gram5.ceres.auckland.ac.nz'] = Cluster()
 
cluster.Name = 'cluster.ceres.auckland.ac.nz'
cluster.WNTmpDir = '/tmp'
cluster.TmpDir = '/tmp'

def createQueue(package,cluster,id, name, acl):
    queue = package.ComputingElement[id] = ComputingElement()
    queue.Name = name
    queue.Status = 'Production'
    queue.JobManager = 'jobmanager-pbs'
    queue.HostName = 'gram5.ceres.auckland.ac.nz'
    queue.GatekeeperPort = 2119
    queue.ContactString = 'gram5.ceres.auckland.ac.nz:8443/jobmanager-pbs'
    queue.DefaultSE = 'gram5.ceres.auckland.ac.nz'
    queue.ApplicationDir = '/share/apps'
    queue.DataDir = cluster.TmpDir
    queue.LRMSType = 'Torque'
    queue.GRAMVersion = '5.0.0'
    queue.qstat = '/opt/torque/bin/qstat'
    queue.pbsnodes = '/opt/torque/bin/pbsnodes'
    queue.ACL = acl
    return queue


####
goldCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-gold', 'gold', [ '/nz/virtual-screening/jobs' ])

goldView = goldCE.views['cluster.nz.virtual-screening.jobs'] = VOView()
goldView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
goldView.DataDir = '${GLOBUS_USER_HOME}'
goldView.ACL = [ '/nz/virtual-screening/jobs' ]

####
uoaMechCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoaMechCE', 'uoamech', [ '/nz/uoa/mechanical-engineering' ])

mechView = uoaMechCE.views['cluster.nz.uoa.mechanical-engineering'] = VOView()
mechView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
mechView.DataDir = '${GLOBUS_USER_HOME}'
mechView.ACL = [ '/nz/uoa/mechanical-engineering' ]


####

statsCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoastats', 'uoastats', [ '/nz/uoa/stats' ])

statsView = statsCE.views['cluster.nz.uoa.stats'] = VOView()
statsView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
statsView.DataDir = '${GLOBUS_USER_HOME}'
statsView.ACL = [ '/nz/uoa/stats' ]

####

mathCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoamath', 'uoamath', [ '/nz/uoa/math' ])

mathView = mathCE.views['cluster.nz.uoa.math'] = VOView()
mathView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
mathView.DataDir = '${GLOBUS_USER_HOME}'
mathView.ACL = [ '/nz/uoa/math' ]

####

chemCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoacompchem', 'uoacompchem', [ '/nz/uoa/comp-chem' ])

chemView = chemCE.views['cluster.nz.uoa.compchem'] = VOView()
chemView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
chemView.DataDir = '${GLOBUS_USER_HOME}'
chemView.ACL = [ '/nz/uoa/comp-chem' ]

####

evolCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoaEvolCE', 'uoaevol', [ '/nz/uoa/comp-evol' ])

evolView = evolCE.views['cluster.nz.uoa.compEvol'] = VOView()
evolView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
evolView.DataDir = '${GLOBUS_USER_HOME}'
evolView.ACL = [ '/nz/uoa/comp-evol' ]

####

engSciCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoaEngSciCE', 'uoaengsci', [ '/nz/uoa/engineering-science' ])

engSciView = engSciCE.views['cluster.nz.uoa.engsci'] = VOView()
engSciView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
engSciView.DataDir = '${GLOBUS_USER_HOME}'
engSciView.ACL = [ '/nz/uoa/engineering-science' ]



####

qOpticsCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-uoaqoptics', 'uoaqoptics', [ '/nz/uoa/quantum-optics' ])

qOpticsView = qOpticsCE.views['cluster.nz.uoa.qoptics'] = VOView()
qOpticsView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
qOpticsView.DataDir = '${GLOBUS_USER_HOME}'
qOpticsView.ACL = [ '/nz/uoa/quantum-optics' ]

###

gpuCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-gpu', 'gpu', ['/nz/nesi'])

gpuView = gpuCE.views['cluster.nz.nesi'] = VOView()
gpuView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
gpuView.DataDir = '${GLOBUS_USER_HOME}'
gpuView.ACL = ['/nz/nesi']

###

demoCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-demo', 'demo', ['/nz/demo'])

demoView = demoCE.views['cluster.nz.demo'] = VOView()
demoView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
demoView.DataDir = '${GLOBUS_USER_HOME}'
demoView.ACL = ['/nz/demo']



# COMPUTING ELEMENT
# this name is defined in computing element of package.pl
# see twiki page for further details on this section
defaultCE = createQueue(package,cluster,'gram5.ceres.auckland.ac.nz-ce-GT5', 'default', [ '/nz/nesi','/nz/uoa','/nz/virtual-screening/jobs' ])

# this information can be retrieved from your LRMS (if defined)
#defaultCE.MaxTotalJobs = 9999999
#defaultCE.MaxRunningJobs = 9999999
#defaultCE.MaxCPUTime = 9999999
defaultCE.MaxWallClockTime = 1000
#defaultCE.MaxTotalJobsPerUser = 9999999

# you can define these if you want, but it's not advised
#defaultCE.LRMSVersion = '2.1.4'
#defaultCE.Priority = 1
#defaultCE.FreeCPUs = 1
#defaultCE.TotalCPUs = 1
        
#defaultCE.WaitingJobs = 0
#defaultCE.RunningJobs = 0
#defaultCE.TotalJobs = 0
#defaultCE.FreeJobSlots = 0

#defaultCE.ACL = [ '/VO3', '/VO4' ]


# VOVIEW
# this name is defined must be unique for each voview in the computing element. It is not refered to anywhere else
# see twiki page for further details on this section


# the RealUser is used in working out the job information for the DefaultView, ie WaitingJobs, TotalCPUs, etc
# it should be retrieved from GUMS in the future
#nesiView.RealUser = 'grid-admin'
nesiView = defaultCE.views['cluster.nz.nesi'] = VOView()
nesiView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
nesiView.DataDir = '${GLOBUS_USER_HOME}'
nesiView.ACL = [ '/nz/nesi','/nz/demo','/nz/virtual-screening/jobs' ]
# /DEFAULTVIEW

# /COMPUTING ELEMENT

####

# SUBCLUSTER
# this name is defined in the subcluser line in package.pl 
# see twiki page for further details on this section
subcluster = package.SubCluster['gram5.ceres.auckland.ac.nz-subcluster-GT5'] = SubCluster()
 
subcluster.InboundIP = False
subcluster.OutboundIP = True
subcluster.PlatformType = ''
subcluster.SMPSize = 1

subcluster.PhysicalCPUs = 204
subcluster.LogicalCPUs = 204
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
subcluster.OperatingSystem.Name = 'CentOS 5'
subcluster.OperatingSystem.Release = '5'
#subcluster.OperatingSystem.Version = '1.0.0'
# /SUBCLUSTER

# /CLUSTER

###############

# STORAGE ELEMENT
# this name is defined in the storage element line package.pl
# see twiki page for further details on this section
gram5StorageElement = package.StorageElement['gram5.ceres.auckland.ac.nz'] = StorageElement()

# the value of this field usually is the root directory of all the storage area locations
# most of the time this directory will be mounted from another host and is made available
# on the grid gateway host
#gram5StorageElement.RootDirectory = '/path/to/root/of/area/dir'

# can be disk, tape, multidisk, or other
gram5StorageElement.Architecture = 'disk'

# STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
nesiArea = gram5StorageElement.areas['gram5.nz.nesi'] = StorageArea()
nesiArea.Path = '${GLOBUS_USER_HOME}'
nesiArea.VirtualPath = '${GLOBUS_USER_HOME}'
nesiArea.Type = 'volatile'
nesiArea.ACL = [ '/nz/nesi',
                 '/nz/demo',
                 '/nz/virtual-screening/jobs',
                 '/nz/uoa/quantum-optics',
                 '/nz/uoa/mechanical-engineering',
                 '/nz/uoa/engineering-science',
                 '/nz/uoa/math',
                 '/nz/uoa/comp-chem',
                 '/nz/uoa/comp-chem/gaussian',
                 '/nz/uoa/comp-evol',
                 '/nz/uoa/stats']
# /STORAGE ELEMENT AREA


# SECOND STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
uoaArea = gram5StorageElement.areas['gram5.nz.uoa'] = StorageArea()
uoaArea.VirtualPath = '${GLOBUS_USER_HOME}'
uoaArea.Path = '${GLOBUS_USER_HOME}'
uoaArea.Type = 'volatile'
uoaArea.ACL = [ '/nz/uoa' ]
# /SECOND STORAGE ELEMENT AREA

# Virtual Screening Areas and Views

virtscreenView = defaultCE.views['cluster.nz.virtual-screening'] = VOView()
virtscreenView.RealUser = 'grid-vs'
virtscreenView.DataDir = '/home/grid-vs[label=Drug discovery home;user_subdir=False]'
virtscreenView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
virtscreenView.ACL = ['/nz/virtual-screening']

virtscreenAcsrcView = defaultCE.views['cluster.nz.virtual-screening.acsrc'] = VOView()
virtscreenAcsrcView.RealUser = 'grid-acsrc'
virtscreenAcsrcView.DataDir = '/home/grid-acsrc[label=Acsrc home;user_subdir=False]'
virtscreenAcsrcView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
virtscreenAcsrcView.ACL = ['/nz/virtual-screening/acsrc']

virtscreenSbsView = defaultCE.views['cluster.nz.virtual-screening.sbs-structural-biology'] = VOView()
virtscreenSbsView.RealUser = 'grid-sbs'
virtscreenSbsView.DataDir = '/home/grid-sbs[label=SBS home;user_subdir=False]'
virtscreenSbsView.DefaultSE = 'gram5.ceres.auckland.ac.nz'
virtscreenSbsView.ACL = ['/nz/virtual-screening/sbs-structural-biology']

virtscreenArea = gram5StorageElement.areas['gram5.nz.virtual-screening'] = StorageArea()
virtscreenArea.Path = '/home/grid-vs[label=Drug discovery home;user_subdir=False]'
virtscreenArea.Type = 'permanent'
virtscreenArea.ACL = ['/nz/virtual-screening']

acsrcArea = gram5StorageElement.areas['gram5.nz.virtual-screening.acsrc'] = StorageArea()
acsrcArea.Path = '/home/grid-acsrc[label=Acsrc home;user_subdir=False]'
acsrcArea.Type = 'permanent'
acsrcArea.ACL = ['/nz/virtual-screening/acsrc']

acsrcArea = gram5StorageElement.areas['gram5.nz.virtual-screening.sbs-structural-biology'] = StorageArea()
acsrcArea.Path = '/home/grid-sbs[label=SBS home;user_subdir=False]'
acsrcArea.Type = 'permanent'
acsrcArea.ACL = ['/nz/virtual-screening/sbs-structural-biology']


# STORAGE ELEMENT ACCESS PROTOCOL
# this name must be unique for each protocol in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
accessProtocol = gram5StorageElement.access_protocols['gram5.gsiftp'] = AccessProtocol()

accessProtocol.Type = 'gsiftp'
accessProtocol.Version = '3.28'
accessProtocol.Endpoint = 'gsiftp://gram5.ceres.auckland.ac.nz:2811'
accessProtocol.Capability = [ 'file transfer', 'other capability' ]
# /STORAGE ELEMENT ACCESS PROTOCOL

# SECOND STORAGE ELEMENT ACCESS PROTOCOL
#accessProtocol = gram5StorageElement.access_protocols['prot2'] = AccessProtocol()
#accessProtocol.Type = 'gsiftp'
#accessProtocol.Version = '2.3'
#accessProtocol.Endpoint = 'gsiftp://ng2.example.apac.site:2811'
#accessProtocol.Capability = [ 'file transfer', 'other capability' ]
# /SECOND STORAGE ELEMENT ACCESS PROTOCOL

# /STORAGE ELEMENT

# ANOTHER STORAGE ELEMENT EXAMPLE FOR AN SRM ENABLED HOST
#gram5StorageElement = package.StorageElement['storage2'] = StorageElement()

# the value of this field usually is the root directory of all the storage area locations
# most of the time this directory will be mounted from another host and is made available
# on the grid gateway host
#gram5StorageElement.RootDirectory = '/path/to/root/of/area/dir'

# can be disk, tape, multidisk, or other
#gram5StorageElement.Architecture = 'tape'

# STORAGE ELEMENT AREA
# this name must be unique for each storage area in the storage element. It is not reference anywhere else.
# see twiki page for further details on this section
#area = gram5StorageElement.areas['area1'] = StorageArea()

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
#controlProtocol = gram5StorageElement.control_protocols['prot1'] = ControlProtocol()

#controlProtocol.Type = 'srm'
#controlProtocol.Version = '2.1'
#controlProtocol.Endpoint = 'srm://srm.example.apac.site:8443'
#controlProtocol.Capability = [ 'file transfer', 'other capability' ]
# /STORAGE ELEMENT CONTROL PROTOCOL

# /ANOTHER STORAGE ELEMENT EXAMPLE FOR AN SRM ENABLED HOST
