# This Python file uses the following encoding: utf-8
import re
from collections import Counter

f = open('CVCV.txt', 'w')

obstruents = ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'S', 'Z']
liquids = ['l', 'R']
nasals = ['m', 'n', 'N']
foreign = ['x', 'G']
consonants = obstruents + liquids + nasals + foreign

vowels = ['a','i','e','E','o','O','u','y','§','1','5','2','9','@','°','3']

semivowels = ['j','8','w']

def syllabic_structure(syl):
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

for key in syllabic_dict:
	following_syllables = syllabic_dict[key]
	syl_counts = Counter(following_syllables)
	S1_structure = syllabic_structure(key.decode('utf-8').encode('cp1252'))
	for syllable in list(set(following_syllables)):
		N = syl_counts[syllable]
		# Here add line to translate the syllable into CV, CYV etc coding.
		S2_structure = syllabic_structure(syllable.decode('utf-8').encode('cp1252'))
		to_print = [S1_structure, S2_structure, str(key), str(syllable), str(N)]
		print >> f, '\t'.join(to_print)

f.close()