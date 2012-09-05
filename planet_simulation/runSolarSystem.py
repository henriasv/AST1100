from planets import *
import sys
import os
import glob

try:
	# Get outputPath. This is relative to the path of the python program file.
	systemPath = sys.argv[1]
except IndexError:
	print "Solar system source file not provided"
	print "Usage: >> python runSolarSystem.py <sourcefile> <outputpath>"
	sys.exit(1)
try:
	endPath = sys.argv[2];
except IndexError:
	print "OutputPath not provided"
path = os.getcwd() + "/" + endPath + "/"

if not os.path.exists(path):
	print "\n creating output path.."
	os.makedirs(path)

if os.listdir(path):
	print " \nThere are already files contained in the outpath: \nCommand to be excecuted and list of files to be deleted" 
	rmCommand = "rm " + path + "*.bin" + " " + path + "*.radius"
	print(rmCommand)
	for item in os.listdir(path):
		print item
	choice = raw_input(" \nDelete *.bin with latter command? (yes/no) ")
	if (choice == "yes"):
		os.system(rmCommand)
	else:
		print "OK, quitting"
		sys.exit(1)
else:
	"\n Output path is empty"

print "\nStarting program.."

execfile(systemPath)

print "Finished. Output in %s" % path
