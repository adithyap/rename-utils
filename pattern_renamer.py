# Renames files in a folder based on the specified rules
# Has no validations, tread carefully

############################################
# Imports
############################################

import os
import re
import sys
import glob

############################################
# User Input section
############################################

# EXPECTED USER INPUT 1:
# Enter the folder containing the episodes
# (Enter the trailing slash too)
directory = ""

# OPTIONAL USER INPUT 2:
# Enter the file extension to process
# Doesn't support processing multiple file extension filters
extension = "*.*"

# OPTIONAL USER INPUT 3:
# Enter a list of filenames to exclude from processing
# This is added to skip over annoyances like Thumbs.db and .DS_Store
# Separate file names by ',' or ';'
filenames_to_exclude = "Thumbs.db;.DS_Store"

# OPTIONAL USER INPUT 4:
# Enter the log file name to be used
logfile_name = "pattern_renamer.log"

############################################
# Constants
############################################

test = "test"
regex_separator = ';|,'
file_write_mode = "w+"

############################################
# Process command line args (if any)
############################################

if test in sys.argv: 
	testMode = 1
else:
	testMode = 0

############################################
# Begin processing
############################################

# Windows specific directory path sanitization
# TODO: Must enable this section and make it OS independant
# directory.replace(r"\\", r"\\\\")
# directory += "\\"

# Fetch filenames into files[]
files = []
files = glob.glob(directory + extension)
# files = os.listdir(directory)

# print files

directory_len = len(directory)

for i in range(len(files)):
	files[i] = files[i][directory_len:]

# Generate exclude list
exclude_list = re.split(regex_separator, filenames_to_exclude)

# Rename Rules
rename = {}
for i in range(len(files)):

	fileName = files[i]

	# Skip excludes
	if fileName.lower() in (x.lower() for x in exclude_list):
		continue
		
	fileName = files[i]


	################################################################
	# THIS IS A MANDATORY USER INPUT SECTION
	# Kind of sad that it is embedded deeply into the code
	# TODO: Should find some way to separate out the rule defining part
	
	# Begin adding custom rules

	# Example rename rules
	# fileName = fileName.lstrip("0") --> To remove any common prefix
	# fileName = fileName.replace("720p", "") --> To remove some common pattern
	# fileName = fileName[:6] + fileName[-4:] --> To keep the first 6 characters along with the file extension


	# End adding custom rules
	# Seriously, don't modify anything below this
	################################################################

	rename[directory + files[i]] = directory + fileName

# Logger
if not testMode:
	log = {}
	for key, value in rename.iteritems():
		log[value] = key

	file = open(directory + logfile_name, file_write_mode)
	file.write(str(log))
	file.close()

# Rename
for key, value in rename.iteritems():
	if testMode:
		print value
	else:
		os.rename(key, value)
