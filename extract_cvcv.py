# This Python file uses the following encoding: utf-8
import re
from collections import Counter

f = open('disyllables.txt', 'w')

# Define phonemes:
obstruents = ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'S', 'Z']
liquids = ['l', 'R']
nasals = ['m', 'n', 'N']
foreign = ['x', 'G']

consonants = obstruents + liquids + nasals + foreign
vowels = ['a','i','e','E','o','O','u','y','§','1','5','2','9','@','°','3']
semivowels = ['j','8','w']

def syllabic_structure(syl):
	# This functions extracts the syllabic structure of any syllable (e.g. CV, CVC, etc)
	structure = ''
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

# First: retrieve all disyllables
syllabic_dict = {}
with open('recoded_L_D_S_E.txt') as corpus:
	for line in corpus:
		line = line.replace('-',' ')
		line = line.split()
		text = line[4:]
		for i, syllable in enumerate(text[:-1]):
			if (syllable not in syllabic_dict):
				syllabic_dict[syllable] = [text[i+1]]
			else:
				syllabic_dict[syllable] = syllabic_dict[syllable] + [text[i+1]]

# Second: extract syllabic structure and count
for S1 in syllabic_dict:
	following_syllables = syllabic_dict[S1]
	syl_counts = Counter(following_syllables)
	S1_structure = syllabic_structure(S1.decode('utf-8').encode('cp1252'))
	for S2 in list(set(following_syllables)):
		N = syl_counts[S2]
		S2_structure = syllabic_structure(S2.decode('utf-8').encode('cp1252'))
		print_output(S1, S2, N, S1_structure, S2_structure, f)

f.close()