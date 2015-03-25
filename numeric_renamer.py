# Renames all the files in a folder by numbers
# Has no validations, tread carefully

############################################
# Imports
############################################

import glob
import os
import sys

############################################
# User Input section
############################################

# EXPECTED USER INPUT 1:
# Enter the path to the directory containing files to be renamed
# (Enter the trailing slash too)
search_dir = ''

# EXPECTED USER INPUT 2:
# Enter the file extension to process
# Doesn't support processing multiple file extension filters
# Example: extension = ".txt"
extension = ""

# OPTIONAL USER INPUT 3:
# Enter the mode of ordering files
# The modes are:
# 	Order by date
# 	Order by time
# The valid inputs are
# 'time' and 'name'
ordering_mode = 'time'

# OPTIONAL USER INPUT 4:
# Enter the starting number to be used to rename files
filename = 0

# OPTIONAL USER INPUT 5:
# Enter a flag to indicate if single digit numbers need to be prefixed with 0
zero_prefix_required = True

############################################
# Constants
############################################

ordering_mode_time = 'time'
ordering_mode_name = 'name'
debug_flag = "test"

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

# Read Start number

files = filter(os.path.isfile, glob.glob(search_dir + "*"))

if ordering_mode == ordering_mode_name:
	files.sort(key=lambda x: os.path.basename(x))
else:
	files.sort(key=lambda x: os.path.getmtime(x))

for f in files:

	target_name = ""

	# Identify target name
	if zero_prefix_required:
		if filename < 10:
			target_name = search_dir + "0" + str(filename) + extension
		else:
			target_name = search_dir + str(filename) + extension
	else:
		target_name = search_dir + str(filename) + extension

	# Final step - rename or print to console
	if debugMode:
		print "Renaming " + f + " to " + target_name
	else:
		os.rename(f, target_name)

	filename += 1
