#!/usr/bin/env python
# Created by JB on 03-22-2012
# Updated: 4/13/2012 - added loop to rename eml to txt. Apparently on certain eml files, python would not open them
# Complete Refactor: 7/5/2012 - Broke out everything into separate functions to modularize and ease debugging.
# 
# This is a script that takes the RedHat security update emails saved to 'srcdir' and strips out the
# relevant information and formats it in 'wiki markup' to allow for quicker wiki page updates (copy / paste)
#
#
# TO DO: Would like a way to save the 'wiki markup' to a text file, to further 
# automate the procedure. Would like to find a way to automate adding the markup to the actual wiki, without 
# having to do a copy / paste job. API?

import os
import re
import xmlrpclib
import subprocess
import sys
import urllib

srcdir = "/Users/jbrake/Desktop/RedHatPatches/"
#wikifile = '/Users/jbrake/Desktop/redhatwikimarkup.txt'
#wfile = open(wikifile, 'w')

advisoryurl = ""
priority = ""
issuedate = ""
patch = ""
version = ""
newfilepath = ""
synopsisList = []
priorityList = []
issueDateList = []
serverVerList = []
advisoryUrlList = []
patchVersionList = []

def getSynopsis(filepath):
	file = open(filepath,'r')
	for line in file:
		if "Synopsis" in line:
			patch = line
			if "Low" in line:
				priority = "{color:#339966}{*}4-Low{*}{color}"
				patch = patch[24:]
				synopsisList.append(patch.strip())
				priorityList.append(priority.strip())
			elif "Moderate" in line:
				priority = "{color:#ffcc00}{*}3-Moderate{*}{color}"
				patch = patch[29:]
				synopsisList.append(patch.strip())
				priorityList.append(priority.strip())
			elif "Important" in line:
				priority = "{color:#ff9900}{*}2-Important{*}{color}"
				patch = patch[30:]
				synopsisList.append(patch.strip())
				priorityList.append(priority.strip())
			elif "Critical" in line:
				priority = "{color:#ff0000}{*}1-Critical{*}{color}"
				patch = patch[29:]
				synopsisList.append(patch.strip())
				priorityList.append(priority.strip())
	file.close()
	
def getIssueDate(filepath):
	file = open(filepath,'r')
	for line in file:
		if "Issue date" in line:
			issuedate = line
			issuedate = issuedate[19:]
			issueDateList.append(issuedate.strip())
	file.close()
	
def checkIfRedHatServerV5(filepath):
	isServerV5 = None
	serverver = ''
	file = open(filepath,'r')
	for line in file:
		if "Red Hat Enterprise Linux (v. 5 server):" in line:
				#if "server" in line:
					#if "i386" in line:
						#continue	
					#else:
			serverver = line
			serverver = serverver.replace(":","")
			serverVerList.append(serverver.strip())
			file.close()
			return True
	file.close()
	return False
	
def getPatchVer(filepath):
	file = open(filepath,'r')
	for line in file:
		if ".rpm" in line:
			if "ftp" in line:
				continue
			else:
				version = line
				patchVersionList.append(version.strip())
				break
	file.close()
			
def getAdvisoryUrl(filepath):
	file = open(filepath,'r')
	for line in file:
		if "/data/cve" in line:
			advisoryurl = line
			advisoryUrlList.append(advisoryurl.strip())
			break
	file.close()
		
def testListLength(a, b, c, d, e, f):
	print len(a)
	print len(b)
	print len(c)
	print len(d)
	print len(e)
	print len(f)

def renameExtensions(srcdir):
	for file in os.listdir(srcdir):
		filepath = srcdir + file
		if filepath.endswith('.eml'):
			newfilepath = filepath.replace('.eml', '.txt')
			os.rename(filepath, newfilepath)
		else:
			continue

def generateWikiMarkup(issueDateList,synopsisList,patchVersionList,priorityList,serverVerList,advisoryUrlList):
	c = 0
	while c < len(synopsisList):
		wikimarkup = '| %s | %s | %s | %s | %s | | | | %s |' %(issueDateList[c],synopsisList[c],patchVersionList[c],priorityList[c],serverVerList[c],advisoryUrlList[c])
		print wikimarkup
		c += 1	

def main():
	renameExtensions(srcdir)
	for file in os.listdir(srcdir):
		serverver = ""
		filepath = srcdir + file
		if ".DS_Store" in filepath:
			continue
		if checkIfRedHatServerV5(filepath):
			getIssueDate(filepath)
			getSynopsis(filepath)
			getPatchVer(filepath)
			getAdvisoryUrl(filepath)
	#testListLength(issueDateList,synopsisList,patchVersionList,priorityList,serverVerList,advisoryUrlList)
	generateWikiMarkup(issueDateList,synopsisList,patchVersionList,priorityList,serverVerList,advisoryUrlList)
	
main()