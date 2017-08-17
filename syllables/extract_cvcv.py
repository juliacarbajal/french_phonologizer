# This Python file uses the following encoding: utf-8
import os
from collections import Counter

if not os.path.exists('syllables/output'):
	os.makedirs('syllables/output')

# Load corpus (IN THE FUTURE MAKE THIS AN INPUT)
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
	
def print_output(syllable_pair, file, context=[]):
	syllable1 = syllable_pair[0]
	syllable2 = syllable_pair[1]
	counts = syllable_pair[2]
	structure1 = syllable_pair[3]
	structure2 = syllable_pair[4]
	structure = (str(structure1) + ' ' + str(structure2)).ljust(15)
	syllables = (str(syllable1) + ' ' + str(syllable2)).decode('utf-8').encode('cp1252').ljust(15)
	syllables = syllables.decode('cp1252').encode('utf-8')
	if not context:
		print >> file, structure + syllables + str(counts)
	else:
		if isinstance(context[0], tuple):
			context = [' '.join(map(str,x)) for x in context]
		print >> file, structure + syllables + str(counts).ljust(10) + ', '.join(Counter(context))

# SCRIPT:
f = open('syllables/output/disyllables.txt', 'w')
fcvcv = open('syllables/output/cvcv.txt', 'w')

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
all_syll_count = count_syllables(syllabic_dict)

# Third: Order by frequency of occurrence and print:
for syll_pair in sorted(all_syll_count, key=lambda x: x[2], reverse = True):
	print_output(syll_pair, f)
	S1_structure = syll_pair[3]
	S2_structure = syll_pair[4]
	if (S1_structure=='CV') and (S2_structure=='CV'):
		print_output(syll_pair, fcvcv)
		
f.close()
fcvcv.close()



# NEW: Alternative way, separated by categories (within word, across words, etc)
f2 = open('syllables/output/bisyl_1word.txt', 'w')
f3 = open('syllables/output/bisyl_2words.txt', 'w')
f4 = open('syllables/output/bisyl_across.txt', 'w')
f5 = open('syllables/output/bisyl_partword.txt', 'w')

syll_1word = {}
syll_partword = {}
syll_2words = {}
syll_across = {}
partwords = {}
wordboundary = {}

for line in corpus:
	line = line.split()
	text = line[4:]
	for i, word in enumerate(text[:-1]):
		syllables = word.split('-')
		syllables_next = text[i+1].split('-')
				
		# Monosyllabic words:	
		if (len(syllables) == 1) and (len(syllables_next) == 1) and ('O' not in [syllabic_structure(syllables_next[0]), syllabic_structure(syllables[0])]):
			# Two monosyllabic words:
			if (syllables[0] not in syll_2words):
				syll_2words[syllables[0]] = [syllables_next[0]]
			else:
				syll_2words[syllables[0]] = syll_2words[syllables[0]] + [syllables_next[0]]
		elif (len(syllables) == 1) and (len(syllables_next) > 1) and (syllabic_structure(syllables[0]) != 'O'):
			# 1 monosyllabic + 1 multisyllabic word:
			if (syllables[0] not in syll_across):
				syll_across[syllables[0]] = [syllables_next[0]]
			else:
				syll_across[syllables[0]] = syll_across[syllables[0]] + [syllables_next[0]]
			# Save context:
			if ((syllables[0], syllables_next[0]) not in wordboundary):
				wordboundary[(syllables[0], syllables_next[0])] = [(word, text[i+1])]
			else:
				wordboundary[(syllables[0], syllables_next[0])] = wordboundary[(syllables[0], syllables_next[0])] + [(word, text[i+1])]
		
		# Bisyllabic words:
		elif len(syllables) == 2:
			# Within:
			if (syllables[0] not in syll_1word):
				syll_1word[syllables[0]] = [syllables[1]]
			else:
				syll_1word[syllables[0]] = syll_1word[syllables[0]] + [syllables[1]]
			# Across (final syllable):
			if (syllables[1] not in syll_across) and (syllabic_structure(syllables_next[0]) != 'O'):
				syll_across[syllables[1]] = [syllables_next[0]]
			elif (syllables[1] in syll_across) and (syllabic_structure(syllables_next[0]) != 'O'):
				syll_across[syllables[1]] = syll_across[syllables[1]] + [syllables_next[0]]
			# Save context:
			if ((syllables[1], syllables_next[0]) not in wordboundary):
				wordboundary[(syllables[1], syllables_next[0])] = [(word, text[i+1])]
			else:
				wordboundary[(syllables[1], syllables_next[0])] = wordboundary[(syllables[1], syllables_next[0])] + [(word, text[i+1])]
				
		# Trisyllabic words and beyond:
		if len(syllables) > 2:
			# Within:
			for j, syl in enumerate(syllables[:-1]):
				# Within:
				if (syl not in syll_partword):
					syll_partword[syl] = [syllables[j+1]]
				else:
					syll_partword[syl] = syll_partword[syl] + [syllables[j+1]]
				# Save context:
				if ((syl, syllables[j+1]) not in partwords):
					partwords[(syl,syllables[j+1])] = [word]
				else:
					partwords[(syl,syllables[j+1])] = partwords[(syl,syllables[j+1])] + [word]
			# Across (final syllable):
			if (syllables[-1] not in syll_across) and (syllabic_structure(syllables_next[0]) != 'O'):
				syll_across[syllables[-1]] = [syllables_next[0]]
			elif (syllables[-1] in syll_across) and (syllabic_structure(syllables_next[0]) != 'O'):
				syll_across[syllables[-1]] = syll_across[syllables[-1]] + [syllables_next[0]]
			# Save context:
			if ((syllables[-1], syllables_next[0]) not in wordboundary):
				wordboundary[(syllables[-1], syllables_next[0])] = [(word, text[i+1])]
			else:
				wordboundary[(syllables[-1], syllables_next[0])] = wordboundary[(syllables[-1], syllables_next[0])] + [(word, text[i+1])]

# Second: Count syllables
syll_1word_count = count_syllables(syll_1word)
syll_2words_count = count_syllables(syll_2words)
syll_across_count = count_syllables(syll_across)
syll_partword_count = count_syllables(syll_partword)

# Third: Order by frequency of occurrence and print:
for syll_pair in sorted(syll_1word_count, key=lambda x: x[2], reverse = True):
	print_output(syll_pair, f2)
for syll_pair in sorted(syll_2words_count, key=lambda x: x[2], reverse = True):
	print_output(syll_pair, f3)
for syll_pair in sorted(syll_across_count, key=lambda x: x[2], reverse = True):
	S1 = syll_pair[0]
	S2 = syll_pair[1]
	print_output(syll_pair, f4, wordboundary[(S1,S2)])
for syll_pair in sorted(syll_partword_count, key=lambda x: x[2], reverse = True):
	S1 = syll_pair[0]
	S2 = syll_pair[1]
	print_output(syll_pair, f5, partwords[(S1,S2)])

f2.close()
f3.close()
f4.close()
f5.close()