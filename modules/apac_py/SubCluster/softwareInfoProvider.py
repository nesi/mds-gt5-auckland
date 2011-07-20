#!/usr/bin/env python

"""Parses ARACGLUE1.2 xml and APAC softwareMap xml to produce a list of software
It reads from multiple files and combines any duplicate software definitions.

Individual blocks are identified by their attributes. If any two elements have the same tag and the same attributes they are considered
identical and their subelements are combined.

If any two elements have the same tag but different attributes they are considered different and are both added to the resultant xml. 

Once the source xml documents have been combined, it passed through the validator. If the validator fails, the combination is done again but this time passing the resultant xml
through the validator after each combination. The point at which it fails is reported.
"""

__author__ = "Ronald Jones (ronald@ivec.org)"
__version__ = "$Revision: 1.2.0 $"
__date__ = "$Date: 2006/11/27$"
__copyright__ = "Copyright (c) 2006 Ronald Jones"
__license__ = "Python"


# standard libraries
import urllib, os, sys, string, re, os.path
# full xml parser with xslt and xsd support
from lxml import etree
# simple xml parser to clean up the output
from xml.dom import minidom
# parse the command line options
from optparse import OptionParser
# parse the configuration file
import ConfigParser
# create the log files
import logging
# allow strings to be treated like files
from StringIO import StringIO

import copy

class Log:
	''' Manage the log. Provides a simple interface to creating and writing a log
	'''
	def __init__(self, path):
		'''create the log, it creates the log file at the path specified'''
		self.logger = logging.getLogger('softwareParser')
		try:
			hdlr = logging.FileHandler(path)
		except IOError:
			# cannot write to the file somehow. Report the error, internally flag that log file will not work and return
			sys.stderr.write('ERROR : cannot write to log file ' + str(path) + "\n")
			self.validLog = False
			return
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		self.logger.addHandler(hdlr)
		self.logger.setLevel(logging.DEBUG)
		self.validLog = True
		
	def message(self, message, status = 'error'):
		''' create a log entry with default status of error'''
		# only do anything is the log is working
		if self.validLog:
			if status == 'info':
				self.logger.info(message)
			else:
				self.logger.error(message)


class ConfigurationReader:
	''' read a windows.ini style configuration file'''
	def __init__(self, file):
		'''create the parser and read the configuration file'''
		if not(os.path.exists(file)):
			sys.stderr.write('Configuration file ' + os.path.abspath(file) + ' cannot be found\n')
			sys.exit()
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.read(file)
		except  ConfigParser.MissingSectionHeaderError:
			sys.stderr.write('Configuration file ' + os.path.abspath(file) + ' has no section headers\n')
			sys.exit()

	def getSourceNames(self, hostname, action):
		'''return a list of all the sources and the format they have. Format is [ (source uri, format), ...]'''
		# get list of all source defns
		sourceDefns = []
		for section in self.config.sections():
			if section[:6] == 'source':
				sourceDefns.append(section)
		if len(sourceDefns) == 0:
			self.writeErrorMessage(action ,'No sources are defined in configuration file ' + os.path.abspath(file))
		sourceDefns.sort()
		# return a list of the locations of the sources
		sources = []
		for sourceDefn in sourceDefns:
			try:
				uri = re.sub('@@subcluster@@', hostname, self.config.get(sourceDefn, 'uri'))
				format = self.config.get(sourceDefn, 'format')
			except ConfigParser.NoOptionError:
				self.writeErrorMessage(action ,'One of the sources is not defined correctly. ' + str(sys.exc_info()[1]))
				sys.exit()
			sources.append( (uri, format) )
		return sources

	def getDataLocation(self):
		try:
			return self.config.get('definitionMapulations', 'xmlSpecDirectory')
		except ConfigParser.NoOptionError:
			return 'softwareInfoData'
			
	def getAPACSchemaLocation(self):
		try:
			return self.config.get('definitionMapulations', 'SchemaDirectory')
		except ConfigParser.NoOptionError:
			return self.getDataLocation()
			
			
	def getAction(self):
		'''return the action, whether it is email or log and the respective details. 
		If it is email, it returns ('email', recipient, subject)
		If it is log file, it returns ('log', path)
		'''
		# check if it is email or log
		try:
			actionType = self.config.get('action', 'type')
			if actionType == 'email':
				# get email details
				recipient = self.config.get('email', 'recipient')
				subject = self.config.get('email', 'subject')
				return ('email', recipient, subject)
			elif actionType == 'log':
				# get log details
				path = self.config.get('log', 'location')
				return ('log', path)			
			else:
				# unknown type
				defaultLog = 'softwareParser.log'
				sys.stderr.write('Unknown action type ' + actionType + '. Setting action type to log, with log file ./' + defaultLog)
				return ('log', defaultLog)
		except ConfigParser.NoOptionError:
				sys.stderr.write('The action, email or log section is not defined correctly : ' + str(sys.exc_info()[1]))
				sys.exit()

	def writeErrorMessage(self, action, message, level = None):
		sys.stderr.write(message + '\n')
		if not(level==None):
			action(message, level)
		else:
			action(message)


def parseOpts():
	usage = """usage: %prog clusterName subClusterName configurationDirectory
	
	clusterName is ignored
	subClusterName is the host name (eg cognac.ivec.org)
	configuration directory is the directory the script looks for the configuration file.
	
	To test the script has access to all the modules it requires use %prog test
	"""
	parser = OptionParser(usage)
	
	parser.add_option("-t", "--testLoading", action="store_true", dest='test', default=False, help='test if all the required modules are installed on the system')

	(options, args) = parser.parse_args()
	
	if (len(args) == 0 and options.test):
		sys.stdout.write('Successful\n')
		sys.exit(0)
	elif len(args) != 3:
		parser.error("incorrect number of arguments")

	return (args)

class XMLHandler:
	
	def __init__(self, formatToXSLMap, schemaName, action):
		# define the map from format to xslt file
		self.map = formatToXSLMap
		
		# define the schema
		self.schemaName = schemaName
		self.action = action
		try:
			filename, header = urllib.urlretrieve(schemaName)
		except:
			message = 'file ' + str(schemaName) + ' cannot be found.\nExiting script\n' 
			self.action(message)
			sys.stderr.write(message)
			sys.exit(1)
		f = open(filename)
		schema_doc = etree.parse(f)
		self.schema = etree.XMLSchema(schema_doc)
		
		

	def cleanText(self, string):
		if string == None:
			return None
		newString = string.strip()
		if  (newString == '') :
			return None
		return newString


	def readableXML(self, xml, flag = ''):
		if flag == 'skipRootNode':
			outputList = []
			printableXML = minidom.parseString(etree.tostring(xml)).documentElement
			for element in printableXML.childNodes:
				outputList.append(element.toprettyxml())
			return '\n'.join(outputList)
		else:	
			try:
				return minidom.parseString(etree.tostring(xml)).toprettyxml()
			except:
				return etree.tostring(xml)

	def transformXML(self, xmlFile, format):
		
		# get the file from whereever it is and make a local copy
		filename, header = urllib.urlretrieve(xmlFile)
		# clean the xml, before parsing it in etree, to it make it uniform so there are no formatting artifacts
		doc = etree.parse(StringIO(self.removeComments(minidom.parse(filename)).toxml()))
		transformFile = self.map[format]
		if transformFile != None:
			# get the transform and transform xml
			xslt_doc = etree.parse(transformFile)
			transform = etree.XSLT(xslt_doc)
			result = transform(doc)
			doc = result
		return doc

	def removeComments(self, xml):
		for child in xml._get_childNodes():
			if child.nodeType == minidom.Document.COMMENT_NODE:
				xml.removeChild(child)
			else:
				self.removeComments(child)
		return xml

	def loadSourceFiles(self, sources):
		#transforms both files to APACGlue1.2 format
		xmlSources = {}	
		for file, format in sources:
			xml = self.transformXML(file, format)
			# validate the xml
			try:
				if not self.schema.validate(xml):
					errorString = 'File ' + file +' is not valid xml with respect to the schema ' + self.schemaName + '\n'
					sys.stderr.write(errorString)
					self.action(errorString)
					os.sys.exit()
				# if get here the xml is valid
				xmlSources[file] = xml
			except ValueError :
				# catch if the xml is not actually xml, but an empty document. In this case the validator throws an exception
				self.action('file ' + str(file) + ' contains no data and has been ignored\n')
				continue
				
		return xmlSources

	def validateXML(self, name, xml):
		if not self.schema.validate(xml):
			return False
		return True

	def removeNameSpace(self, xml):
			
		# copy everything across except the namespace (which does not seem to be able to be copied anyway)
		pattern = re.compile(r'\{[^}]*\}(.*)')
		#print pattern.search('{abc}def').groups()
		if not type(xml.tag) == type(''):
			return xml
		# if get here then tag is of type string
		found = pattern.search(xml.tag).groups()
		if found == None:
			# this happens when there is no uri defined
			newTag = xml.tag
		else:
			newTag = found[0]
		
		newElement = etree.Element(newTag)
		for key, value in xml.items():
			newElement.attrib[key] = value
		newElement.text = xml.text
		for child in xml:
			newElement.append(self.removeNameSpace(child))
		return newElement

				
	def combineXML(self, source, target, errorCatchMode = False, sourceFileName = '', fulltree = None):
		''' source and target are equivalent nodes in their XML trees. Any new elements in source are copied across to target. And elements that are the same have their subelements recursively called by this function
		'''
		
		# check if this are any duplicates at the top level
		for element in source:
			# find all the possible candidates
			candidates = target.findall(element.tag)
			found = False
			foundElement = None
			for candidate in candidates:
				# check the attributes are the same
				if element.items() == candidate.items():
					# compare the text, so strings only made up of white space equal each other
					if self.cleanText(element.text) == self.cleanText(candidate.text):
						found = True
						foundElement = candidate
						break
			# if find entry that is same, use combineXML on it. Otherwise add it to the target XML because it is new)
			if found:
				self.combineXML(element, foundElement, errorCatchMode, sourceFileName, fulltree)
			else:
				target.append(element)
				if errorCatchMode:
					if not (self.validateXML('error catch tree', fulltree)):
						errorString = 'XML Tree is invalid with the addition of\n\n\t\t' + self.readableXML(element) + '\nfrom\n\n' + self.readableXML(source) + ' in file ' + sourceFileName + '\nto the target XML\n\n' + self.readableXML(target) + '\n'
						sys.stderr.write(errorString)
						action(errorString)
						break

	def makeNewXML(self, xml):
		return self.loadSourceFiles([(xml, 'APACGLUE')])[xml]

	def combineSources(self, sources, minimalXML):
		
		#transforms both files to APACGlue1.2 format
		xmlSources = self.loadSourceFiles(sources)
			
		# combine the two sources
		newSource = self.makeNewXML(blankXML)
		newXML = newSource.getroot()
		for xml in xmlSources:
			self.combineXML(xmlSources[xml].getroot(), newXML)

		# validate the result, if it is not valid, redo the combination with checking on
		if not self.validateXML('Combined XML', newXML):
			# read the original XML again because the elements have been moved.
			xmlSources = self.loadSourceFiles(sources)
			debugXMLTree = self.makeNewXML(blankXML)
			debugXML = debugXMLTree.getroot()
			for xml in xmlSources:
				self.combineXML(xmlSources[xml].getroot(), debugXML, True, xml, debugXML)
			return (False, '')
		
		return (True, newXML)
	
if __name__ == '__main__':
	# change directory to location of script so the relative path names are correct
	oldLocation = os.getcwd()
	baseLocation = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.chdir(baseLocation)
	
	
	# get all the options from the command line
	clusterName, subClusterName, configDirectory = parseOpts()

	# hardcoded configuration
	configurationFile = "%s_%s_SIP.ini" % (clusterName, subClusterName)


	# read the configuration file, and use it contents to work out the settings
	cr = ConfigurationReader(configDirectory + os.sep + configurationFile)
	actionDef = cr.getAction()
	dataLocation = cr.getDataLocation()
	APACSchemaLocation = cr.getAPACSchemaLocation()
	if actionDef[0]== 'log':
		logger = Log(actionDef[1])
		action = logger.message

	formatToXSLMap = { 	'softwareMap' : os.path.join(dataLocation,'software_map_2.xsl'), 
						'APACGLUE' : None,
						'APACGLUE1.2' : None,
					}
	blankXML = os.path.join(dataLocation, 'minimal.xml')
	fullXML = os.path.join(dataLocation,'maximal.xml')
	schema = os.path.join(APACSchemaLocation,"APACSoftwareSubSchemaR2.xsd")

	sources = cr.getSourceNames(subClusterName, action)

	handler = XMLHandler(formatToXSLMap, schema, action)
	valid, resultXML = handler.combineSources(sources, blankXML)
	if valid:
		nsCleanXML =  handler.removeNameSpace(resultXML)
		sys.stdout.write(handler.readableXML(nsCleanXML, 'skipRootNode'))
	# change working directory back for calling script 
	os.chdir(oldLocation)
