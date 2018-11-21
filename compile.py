# This Python file uses the following encoding: utf-8

######################################################################################
#
#    CORPUS COMPILER (2018)
#
#    Authors: Julia Carbajal, Camillia Bouchon, Emmanuel Dupoux & Sharon Peperkamp
#    Contact: carbajal.mjulia@gmail.com   or   sharon.peperkamp@ens.fr
#
######################################################################################

# NOTE: Please verify that you have successfully run clean_corpus.py and phonologize.py
# before running this script.

import os

# SET PARAMETERS

### Age limits (XyXm) ###
age_min_input = '0y0m'
age_max_input = '2y0m'

### Define which transcription to load (orthographic or phonological) ###
# Note: use option 4 for the phonologized corpus described in Carbajal, Bouchon, Dupoux & Peperkamp (2018)
option = 4

if option == 1:
	# Orthographic transcription
	phono_transcript = False
	folder = 'corpora'
	filename = '/clean/extract.txt'
	outname = 'ortho'
	fullname = '*Transcription type: orthographic'
elif option in [2,3,4,5]:
	phono_transcript = True
	folder = 'output'
	if option == 2:
		# Phonological transcription with Liaison (no other rules)
		filename = '/phonologized_L.txt'
		outname = 'phono_L'
		fullname = '*Transcription type: phonological\n*Phonological rules: liaison'
	elif option == 3:
		# Phonological transcription with Liaison and Liquid Deletion
		filename = '/phonologized_L_D.txt'
		outname = 'phono_L_D'
		fullname = '*Transcription type: phonological\n*Phonological rules: liaison and liquid deletion'
	elif option == 4:
		# Phonological transcription with Liaison, Liquid Deletion and Enchainement plus Je-devoicing (resyllabification)
		filename = '/phonologized_L_D_E.txt'
		outname = 'phono_L_D_E'
		fullname = '*Transcription type: phonological\n*Phonological rules: liaison, liquid deletion,\n enchainement and je-devoicing'
	elif option == 5:
		# Phonological transcription with Liaison, Liquid Deletion, Schwa Insertion and Enchainement plus Je-devoicing (resyllabification)
		filename = '/phonologized_L_D_S_E.txt'
		outname = 'phono_L_D_S_E'
		fullname = '*Transcription type: phonological\n*Phonological rules: liaison, liquid deletion, \n schwa insertion, enchainement and je-devoicing'

		
### Other options (set to True or False) ###

# Print fileID and age?
printInfo = True

# Print in lower-case? (IMPORTANT: lower-case cannot be used in phonological transcriptions as capital letters may mean different phonemes)
lowerCase = False

# Remove parentheses? (They mark unpronounced parts of words - only useful in orthographic transcriptions)
removeParentheses = False

# Collapse nasal oe (symbol "1") and nasal ɛ (symbol "5") into single category (symbol "5")?
# Note: in many dialects of French, this contrast doesn't exist. E.g., "brun" and "brin" are both pronounced with nasal ɛ.
collapseNasals = True

###########################################################################################
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

###########################################################################################
# COMPILE & PRINT

if not os.path.exists('compiled_corpus'):
	os.makedirs('compiled_corpus')

# Tags and options info:
if printInfo:
	printInfoTag = ''
	infofullname = '*Print file ID and age: True'
else:
	printInfoTag = '_noFileInfo'
	infofullname = '*Print file ID and age: False'
if (not phono_transcript) and removeParentheses:
	removeParenthesesTag = '_noParnths'
	parenthesischoice = '*Print parentheses: False'
else:
	removeParenthesesTag = ''
	parenthesischoice = '*Print parentheses: True'
if collapseNasals:
	nasalsfullname = '*Collapse mid-front nasals: True'
else:
	nasalsfullname = '*Collapse mid-front nasals: False'

# Open output file for writing
f = open('compiled_corpus/corpus_' + outname + '_' + age_min_input + '_' + age_max_input + printInfoTag + removeParenthesesTag + '.txt', 'w')

# List of files
dirlist = [ item for item in os.listdir(folder) if os.path.isdir(os.path.join(folder, item)) ]

# Print options info:
print '\nCompiling corpora with the following options:\n'
print fullname
print '*Age range: ' + age_min_input + ' - ' + age_max_input
print infofullname
if (not phono_transcript):
	print parenthesischoice
else:
	print nasalsfullname
print '*Included corpora:'
	
for corpusdir in dirlist:
	print ' -' + corpusdir
	location = folder + '/' + corpusdir
	with open(location + filename) as recoded_file:
		for line_ID, line_text in enumerate(recoded_file):
			if (not phono_transcript) and lowerCase:
				line_text = line_text.lower()
			if (not phono_transcript) and removeParentheses:
				line_text = line_text.replace('(','').replace(')','')
			line = line_text.split()
			if phono_transcript and collapseNasals:
				line[5:] = [text.replace('1','5') for text in line[5:]] # NOT WORKING (to do!)
			age = [int(x) for x in line[1:4]]
			if check_age(age):
				if printInfo:
					print >> f, corpusdir + ' ' + ' '.join(line)
				else:
					print >> f, ' '.join(line[4:])

f.close()