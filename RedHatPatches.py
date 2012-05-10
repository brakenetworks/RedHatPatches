
# Created by JB on 03-22-2012
# Updated: 4/13/2012 - added loop to rename eml to txt. Apparently on certain eml files, python would not open them
# 
# This is a script that takes the RedHat security update emails saved to 'srcdir' and strips out the
# relevant information and formats it in 'wiki markup' to allow for quicker wiki page updates (copy / paste)
#
# Known Issues: This can only be run from TextMate currently, as there is an issue running it from Terminal, where
# the output is incorrect. Believed to be an issue with '|' characters. Researching...
#
# TO DO: Would like a way to save the 'wiki markup' to a text file (Doesn't work due to above issue), to further 
# automate the procedure. Would like to find a way to automate adding the markup to the actual wiki, without 
# having to do a copy / paste job. API?

import os

srcdir = "/Users/jbrake/Desktop/RedHatPatches/"
#wikifile = '/Users/jbrake/Desktop/redhatwikimarkup.txt'
#wfile = open(wikifile, 'w')

advisoryurl = ""
priority = ""
issuedate = ""
patch = ""
version = ""
newfilepath = ""

# 4/13/2012 - Rename to .txt to correct random issues with parsing .eml files
for file in os.listdir(srcdir):
	filepath = srcdir + file
	if filepath.endswith('.eml'):
		newfilepath = filepath.replace('.eml', '.txt')
		os.rename(filepath, newfilepath)
	else:
		continue

for file in os.listdir(srcdir):
	serverver = ""
	filepath = srcdir + file
	if ".DS_Store" in filepath:
		continue
	file = open(filepath,'r')
	
	
	for line in file:
		
		if "Synopsis" in line:
			patch = line
			#print file
			if "Low" in line:
				priority = "{color:#339966}{*}4-Low{*}{color}"
				patch = patch[24:]
				patch = patch.replace("\n","")
			elif "Moderate" in line:
				priority = "{color:#ffcc00}{*}3-Moderate{*}{color}"
				patch = patch[29:]
				patch = patch.replace("\n","")
			elif "Important" in line:
				priority = "{color:#ff9900}{*}2-Important{*}{color}"
				patch = patch[30:]
				patch = patch.replace("\n","")
			elif "Critical" in line:
				priority = "{color:#ff0000}{*}1-Critical{*}{color}"
				patch = patch[29:]
				patch = patch.replace("\n","")
				
		#if "Advisory URL" in line:
		#	advisoryurl = line
		#	advisoryurl = advisoryurl[19:]
		#	advisoryurl = advisoryurl.replace("\n","")
		
		elif "Issue date" in line:
			issuedate = line
			issuedate = issuedate[19:]
			issuedate = issuedate.replace("\n","")
				
		elif "Red Hat Enterprise Linux (v. 5 server):" in line:
				#if "server" in line:
					#if "i386" in line:
						#continue	
					#else:
			serverver = line
			serverver = serverver.replace(":","")
			serverver = serverver.replace("\n","")
					
		elif ".rpm" in line:
			if "ftp" in line:
				continue
			else:
				version = line
				version = version.replace("\n","")
		
		elif "/data/cve" in line:
			advisoryurl = line
			advisoryurl = advisoryurl.replace("\n","")
	
	file.close()
	
	#This checks if the 'serverver' variable has been assigned data from above. If it has no
	#data, it could only mean the script did not find a line with v.5 server in it, therefore meaning we do 
	#not need to worry about it. It then continues with the next iteration of the loop, bypassing printing
	#out 'wikimarkup'
	if serverver == '':
		#skipped = ''
		#skipped = skipped + '\n' + filepath
		continue
	
	
	wikimarkup = '| %s | %s | %s | %s | %s | | | | %s |' %(issuedate,patch,version,priority,serverver,advisoryurl)
 
	#wfile.write(wikimarkup)
	
	print wikimarkup
	
#print '\n\n\nSkipped the following files (not server v.5): %s' %skipped
	#wfile.close()
