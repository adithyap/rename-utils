# Appends episode names
# Expects a file containing the list of episode names, one per line in chronological order
# Has no validations, tread carefully
# 25-March-2015

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
# Enter the path to the file containing the episode names
# (Enter the trailing slash too)
epname_source = ""

# EXPECTED USER INPUT 2:
# Enter the folder containing the episodes
episodes_dir = ""

# OPTIONAL USER INPUT 3:
# Enter the prefix for each episode name
# This could be something like 'S06E'
epname_prefix = "S06E"

# OPTIONAL USER INPUT 4:
# Enter the file extension to process
# Doesn't support processing multiple file extension filters
epname_extension = "*.*"

# OPTIONAL USER INPUT 5:
# Enter a list of filenames to exclude from processing
# This is added to skip over annoyances like Thumbs.db and .DS_Store
# Separate file names by ',' or ';'
filenames_to_exclude = "Thumbs.db;.DS_Store"

# OPTIONAL USER INPUT 6:
# Enter the seperator to use between the episode numbering and the episode name
epname_separator = " - "

# OPTIONAL USER INPUT 7:
# Enter the log file name to be used
logfile_name = "appender.log"

# OPTIONAL USER INPUT 7:
# Enter the error report file name to be used
errorfile_name = "appender_errors.log"

############################################
# Constants
############################################

debug_flag = "test"
file_write_mode = "w+"
regex_separator = ';|,'
file_extension_splitter = '.'

############################################
# Helper functions
############################################

#########################
# Substitute for TryParse
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

############################################
# Process command line args (if any)
############################################

# Set Mode
if debug_flag in sys.argv: 
	debugMode = 1
else:
	debugMode = 0

############################################
# Begin processing
############################################

epname_map = {}			# Map of (episode number, episode name)
rename_targets = {} 	# Map of (current file name, target file name)
ep_files = []			# List of files to be considered for renaming
errors = [] 			# List of errors encountered during processing

# Read all episode names
epnames = open(epname_source).read().splitlines()

# Populate episode name map
for i in range(len(epnames)):
	# Convert 0-index to 1-index
	epname_map[i+1] = epnames[i]

# Create a map for rename list

# Fetch episode files into array
ep_files = glob.glob(episodes_dir + epname_extension)

# Strip off everything except the file name
directory_len = len(episodes_dir)
for i in range(len(ep_files)):
	ep_files[i] = ep_files[i][directory_len:]

# Generate exclude list
exclude_list = re.split(regex_separator, filenames_to_exclude)

############################
# Generate rename candidates
for i in range(len(ep_files)):

	ep_file_name = ep_files[i]

	# Skip excludes
	if ep_file_name.lower() in (x.lower() for x in exclude_list):
		continue

	# Handle prefixes
	ep_file_name = (ep_file_name.lstrip(epname_prefix)).split(file_extension_splitter)[0]

	# Don't process file if it can't be casted to int
	if RepresentsInt(ep_file_name) == False:
		errors.append("Unable to identify episode number for " + ep_files[i])
		continue
	
	# Parse filename into INT
	ep_index = int(ep_file_name)

	# Use the computed episode index to search the episode name map
	
	if ep_index in epname_map:

		# Corresponding episode name has been found, push it to rename list
		
		# Split filename into name and extension
			# Rant:
			# This is screwed if the file has no extension
			# But then, which media file doesn't have an extension?
		filename = ep_files[i].split(file_extension_splitter)[0]
		extension = ep_files[i].split(file_extension_splitter)[1]

		# Generate target file name
		target_filename = episodes_dir + filename + epname_separator + epname_map[ep_index] + file_extension_splitter + extension

		# Push it into rename targets map
		rename_targets[episodes_dir + ep_files[i]] = target_filename
	else:
		errors.append("No matching episode name found for " + ep_files[i])

#######################
# Generate Log Contents

if not debugMode:
	log = {}		# Map of (current file name, previous file name)
	for key, value in rename_targets.iteritems():
		log[value] = key

	file = open(episodes_dir + logfile_name, file_write_mode)
	file.write(str(log))
	file.close()

##############
# Begin rename
for key, value in rename_targets.iteritems():
	if debugMode:
		print value
	else:
		os.rename(key, value)

#######################
# Generate Error Report
if len(errors) > 0:

	if debugMode:
		print errors
	else:
		file = open(episodes_dir + errorfile_name, file_write_mode)
		file.write(str(errors))
		file.close()
