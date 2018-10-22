# This Python file uses the following encoding: utf-8
import os

###############################################################################################
# SET PARAMETERS

# Age limits (XyXm):
age_min_input = '0y0m' # Eventually make this input user-defined
age_max_input = '2y0m'

# Define which transcription to load (orthographic or phonological):
phono_transcript = True # True for phonological transcription, False for orthographic transcription
if phono_transcript:
	folder = 'output'
	filename = '/recoded_L_D_E.txt'  #'/recoded_L_D_S_E.txt' # Note: specify here which version of the phonologized corpus to use.
	outname = 'phono'
else:
	folder = 'corpora'
	filename = '/clean/extract.txt'
	outname = 'ortho'

# Print fileID and age?
printInfo = True
if printInfo:
	printInfoTag = '_withFileInfo'
else:
	printInfoTag = '_noFileInfo'

# Print in lower-case?
lowerCase = False

# Remove parentheses? (Symbolises unpronounced parts of words)
removeParentheses = False
if removeParentheses:
	removeParenthesesTag = '_noParnths'
else:
	removeParenthesesTag = ''

###############################################################################################
# FUNCTIONS

def parse_age(age_string):
	age = age_string.replace('y','-').replace('m','')
	age = age.split('-')
	age = [int(x) for x in age]
	return age

age_min_y, age_min_m = parse_age(age_min_input)
age_max_y, age_max_m = parse_age(age_max_input)
total_months_min = age_min_y * 12 + age_min_m
total_months_max = age_max_y * 12 + age_max_m


def check_age(current_age):
	years  = current_age[0]
	months = current_age[1]
	days   = current_age[2]
	total_months = years*12 + months
	if (total_months in range(total_months_min,total_months_max) or (total_months == total_months_max and days == 0)):
		include = True
	else:
		include = False
	return include

###############################################################################################
# COMPILE & PRINT
# Open output file for writing
f = open('corpus_' + outname + '_' + age_min_input + '_' + age_max_input + printInfoTag + removeParenthesesTag + '.txt', 'w')
# List of files
dirlist = [ item for item in os.listdir(folder) if os.path.isdir(os.path.join(folder, item)) ]

for corpusdir in dirlist:
	location = folder + '/' + corpusdir
	with open(location + filename) as recoded_file:
		for line_ID, line_text in enumerate(recoded_file):
			if lowerCase:
				line_text = line_text.lower()
			if removeParentheses:
				line_text = line_text.replace('(','').replace(')','')
			line = line_text.split()
			age = [int(x) for x in line[1:4]]
			if check_age(age):
				if printInfo:
					print >> f, corpusdir + ' ' + line_text.strip()
				else:
					print >> f, ' '.join(line[4:])

f.close()