# This Python file uses the following encoding: utf-8
import re
import os
from collections import Counter
import unicodedata

corpus = []
with open('corpus0y0m-2y0m.txt') as recoded_file:
	for line in recoded_file:
		corpus.append(line.strip())

# OLD WAY OF LOADING CORPORA (REPLACED BY COMPILED CORPUS)
# root='output'
# dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

# corpus = []
# for corpusdir in dirlist:
	# location = 'output/' + corpusdir
	# with open(location + '/recoded_L_D_S_E.txt') as recoded_file:
		# for line_ID, line_text in enumerate(recoded_file):
			# corpus.append(line_text.strip())
			
f = open('syllables/disyllables.txt', 'w')
fcvcv = open('syllables/cvcv.txt', 'w')

# Define phonemes:
obstruents = ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'S', 'Z']
liquids = ['l', 'R']
nasals = ['m', 'n', 'N']
foreign = ['x', 'G']

consonants = obstruents + liquids + nasals + foreign
vowels = ['a','i','e','E','o','O','u','y','4','1','5','2','9','@','6','3'] # Note: replacing § with 4 and ° with 6 for comparison
semivowels = ['j','8','w']

# FUNCTIONS:
def syllabic_structure(syl):
	# This function extracts the syllabic structure of any syllable (e.g. CV, CVC, etc)
	# C: Consonants, V: Vowels, S: Semi-vowels, O: Other symbols (not a phoneme)
	structure = ''
	syl = syl.replace('§', '4').replace('°', '6') # Replacing unicode symbols to match vowels with special characters 
	for phone in syl:
		if phone in consonants:
			structure += 'C'
		elif phone in vowels:
			structure += 'V'
		elif phone in semivowels:
			structure += 'S'
		else:
			structure += 'O'
	return structure

def print_output(syllable1, syllable2, counts, structure1, structure2, file):
	structure = (str(structure1) + ' ' + str(structure2)).ljust(15)
	syllables = (str(syllable1) + ' ' + str(syllable2)).decode('utf-8').encode('cp1252').ljust(15)
	syllables = syllables.decode('cp1252').encode('utf-8')
	print >> file, structure + syllables + str(counts)

# SCRIPT:
# First: retrieve all disyllables
syllabic_dict = {}
for line in corpus:
	line = line.replace('-',' ')
	line = line.split()
	text = line[4:]
	for i, syllable in enumerate(text[:-1]):
		if (syllable not in syllabic_dict):
			syllabic_dict[syllable] = [text[i+1]]
		else:
			syllabic_dict[syllable] = syllabic_dict[syllable] + [text[i+1]]

# Second: extract syllabic structure and count syllable pairs
syll_count = []
for S1 in syllabic_dict:
	S1 = str(S1)
	following_syllables = syllabic_dict[S1]
	syl_counts = Counter(following_syllables)
	S1_structure = syllabic_structure(S1)
	for S2 in list(set(following_syllables)):
		S2 = str(S2)
		N = syl_counts[S2]
		S2_structure = syllabic_structure(S2)
		syll_count.append([S1,S2,N,S1_structure,S2_structure])

# Third: Order by frequency of occurrence and print:
for syll_pair in sorted(syll_count, key=lambda x: x[2], reverse = True):
	S1 = syll_pair[0]
	S2 = syll_pair[1]
	N = syll_pair[2]
	S1_structure = syll_pair[3]
	S2_structure = syll_pair[4]
	print_output(S1, S2, N, S1_structure, S2_structure, f)
	if (S1_structure=='CV') and (S2_structure=='CV'):
		print_output(S1, S2, N, S1_structure, S2_structure, fcvcv)
		
f.close()
fcvcv.close()

def count_syllables(syllable_dictionary):
	syll_count = []
	for S1 in syllable_dictionary:
		S1 = str(S1)
		following_syllables = syllable_dictionary[S1]
		syl_counts = Counter(following_syllables)
		S1_structure = syllabic_structure(S1)
		for S2 in list(set(following_syllables)):
			S2 = str(S2)
			N = syl_counts[S2]
			S2_structure = syllabic_structure(S2)
			syll_count.append([S1,S2,N,S1_structure,S2_structure])
	return syll_count

# NEW: Alternative way
f2 = open('prueba.txt', 'w')
syll_1word = {}
syll_partword = []
syll_2words = []
syll_across = []
for line in corpus:
	line = line.split()
	text = line[4:]
	for i, word in enumerate(text[:-1]):
		syllables = word.split('-')
		if len(syllables) == 2:
			if (syllables[0] not in syll_1word):
				syll_1word[syllables[0]] = [syllables[1]]
			else:
				syll_1word[syllables[0]] = syll_1word[syllables[0]] + [syllables[1]]
		#for j, syllable in enumerate(syllables):
		#	if (syllable not in syll_1word)

syll_1word_count = count_syllables(syll_1word)
# Third: Order by frequency of occurrence and print:
for syll_pair in sorted(syll_1word_count, key=lambda x: x[2], reverse = True):
	S1 = syll_pair[0]
	S2 = syll_pair[1]
	N = syll_pair[2]
	S1_structure = syll_pair[3]
	S2_structure = syll_pair[4]
	print_output(S1, S2, N, S1_structure, S2_structure, f2)
	#if (S1_structure=='CV') and (S2_structure=='CV'):
	#	print_output(S1, S2, N, S1_structure, S2_structure, fcvcv)
#print >> f2, syll_1word
f2.close()
