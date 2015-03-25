# Trims quotes from start and end of every line in a given file
# 25 March 2015

############################################
# User Input section
############################################

# EXPECTED USER INPUT 1:
# Enter the path to the file to be trimmed of quotes
source = "/Users/adithya/Desktop/30rs4"

############################################
# Constants
############################################

file_write_mode = "w+"

############################################
# Begin processing
############################################

# Read content
content = open(source).read().splitlines()

# Remove quotes
for i in range(len(content)):
	content[i] = content[i].lstrip("\"")
	content[i] = content[i].rstrip("\"")

# Write back to file
file = open(source, file_write_mode)

content_len = len(content)

for i in range(content_len):
	file.write(content[i])

	if content_len - i > 1:
		file.write("\n")
		
file.close()