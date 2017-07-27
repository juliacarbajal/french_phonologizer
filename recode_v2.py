# This Python file uses the following encoding: utf-8
import sys # This is not necessary anymore (but I'll keep it as a reminder that I might reintroduce it for batch-processing)

f = open('liaison_cases.txt', 'w')
foutput = open('recoded_with_liaison.txt','w')

# Special symbols to be added to dictionary:
dico = {}
dico[","]=","
dico["?"]="?"
dico["!"]="!"
dico["."]="."
dico[";"]=";"
dico[":"]=":"

dico["\*"]="#"  
dico["l'"]="l'" 
dico["d'"]="d'" 
dico["m'"]="m'" 
dico["n'"]="n'" 
dico["c'"]="s'" 
dico["t'"]="t'" 
dico["s'"]="s'" 
dico["j'"]="Z'"

# Load the Lexique dictionary (pre-compiled):
with open('french.dic') as dic:
	for line in dic:
		line = line.decode('cp1252').encode('utf-8')
		aux = line.split()
		if len(aux) == 2:
			dico[aux[0]] = aux[1]

# Liaison vowels and consonants
vowels = ['a','i','e','E','o','O','u','y','§','1','5','2','9','@']

liaison = {}
liaison['s'] = 'z'
liaison['z'] = 'z'
liaison['t'] = 't'
liaison['p'] = 'p'
liaison['n'] = 'n'
liaison['d'] = 't'
liaison['f'] = 'v'
liaison['x'] = 'z'
liaison['r'] = 'R'

punctuation = [',', '?', '!', '.', ';', ':']

# Load the adjectives:
adjectives = [] # Only adjectives finishing in a liaison consonant, to add to mandatory list
V_adjectives =[] # All vowel-initial adjectives, for plural noun + adjective rule
with open('output_ADJ.txt') as ADJlist:
	for line in ADJlist:
		line = line.strip()
		if line[0] in vowels: 
			V_adjectives.append(line) 
		if line[-1] in liaison: 
			adjectives.append(line)

adjectives = adjectives + ['deux', 'trois', 'vingt', 'cent']

# Load the plural nouns:
plural_nouns = []
with open('output_NOMp.txt') as NOMlist:
	for line in NOMlist:
		line = line.strip()
		if line[-1] in liaison: # Only nouns finishing in a liaison consonant (this only excludes very few cases that don't finish in s or x)
			plural_nouns.append(line)

# Mandatory liaison:
liaison_words = ['un', "quelqu'un", 'des', 'les', 'ces',\
                 'mon', 'ton', 'son', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs',\
				 'aux', 'aucun', 'tout', 'toutes', 'quels', 'quelles', 'quelques',\
				 'lesquels', 'lesquelles', 'auxquels', 'auxquelles', 'desquels', 'desquelles',\
				 'plusieurs', 'certains', 'certaines', 'autres',\
				 'on', 'nous', 'vous', 'ils', 'elles',\
				 'est', 'ont', 'chez', 'dans', 'en', 'sans', 'sous',\
				 'plus', 'moins', 'très', 'bien', 'trop', 'beaucoup']


# Special cases:
special = {}
# Modal verbs in clitic groups:
special['fait'] = ['il','elle','on']
special['veut'] = ['il','elle','on']
special['peut'] = ['il','elle','on','être']
special['doit'] = ['il','elle','on']
special['sait'] = ['il','elle','on']
special['vaut'] = ['il','elle','on']
special['font']    = ['ils','elles']
special['veulent'] = ['ils','elles']
special['peuvent'] = ['ils','elles']
special['doivent'] = ['ils','elles']
special['savent']  = ['ils','elles']
special['valent']  = ['ils','elles']
special['faisait'] = ['il','elle','on']
special['voulait'] = ['il','elle','on']
special['pouvait'] = ['il','elle','on']
special['devait']  = ['il','elle','on']
special['savait']  = ['il','elle','on']
special['valait']  = ['il','elle','on']
special['faisaient'] = ['ils','elles']
special['voulaient'] = ['ils','elles']
special['pouvaient'] = ['ils','elles']
special['devaient']  = ['ils','elles']
special['savaient']  = ['ils','elles']
special['valaient']  = ['ils','elles']
special['faudrait']  = ['il','elle','on']
special['voudrait'] = ['il','elle','on']
special['pourrait'] = ['il','elle','on']
special['devrait']  = ['il','elle','on']
special['saurait']  = ['il','elle','on']
special['vaudrait'] = ['il','elle','on']
special['faudraient'] = ['ils','elles']
special['voudraient'] = ['ils','elles']
special['pourraient'] = ['ils','elles']
special['devraient']  = ['ils','elles']
special['sauraient']  = ['ils','elles']
special['vaudraient'] = ['ils','elles']
# Auxiliaries in clitic groups:
special['était']  = ['il','elle','on']
special['serait'] = ['il','elle','on']
special['allait'] = ['il','elle','on']
special['irait']  = ['il','elle','on']
special['sont']     = ['ils','elles']
special['étaient']  = ['ils','elles']
special['seraient'] = ['ils','elles']
special['allaient'] = ['ils','elles']
special['iraient']  = ['ils','elles']
special['vas'] = 'y'
special['allez'] = 'y'
special['allons'] = 'y'
special['prends'] = 'en'
special['prenez'] = 'en'
special['prenons'] = 'en'
# Others
special['comment'] = 'allez'
special['quand'] = 'est'
special['quant'] = ['à', 'aux']

# Exceptions
# Words beginning with h-aspiré (list retrieved from wikipedia article: https://fr.wikipedia.org/wiki/H_aspiré)
h_aspire = []
with open('h_aspire.txt') as Hlist:
	for line in Hlist:
		line = line.strip()
		h_aspire.append(line)
			
exceptions_next = ['et', 'oh', 'euh', 'hum', 'ah', 'ou', 'u', 'i', 'où', 'apparemment', 'alors', 'attends'] + h_aspire

# Functions:

def check_liaison(all_words, k) :
	# This function checks if liaison applies, returns True or False
	do_liaison = False
	current_word = all_words[k]
	next_word    = all_words[k+1]
	next_word_starts_with_vowel = (next_word in dico) and (next_word not in punctuation) and (dico[next_word][0] in vowels)
	
	if (current_word not in punctuation) and (next_word_starts_with_vowel):
		next_word_2  = all_words[k+2]
		prev_word    = '#'
		if (k>0) :
			prev_word   = all_words[k-1]
			
		# Case 1: List of mandatory special cases (see above)
		if (current_word in special) and (next_word in special[current_word]) :
			do_liaison = True
			# Correct 'tu vas y + infinitif' cases:
			if (current_word == 'vas') and ((prev_word == 'tu') or (next_word_2[-2:] in ['er','ir'])) :
				do_liaison = False 
			# Correct 'en fait il/elle' cases, 'tout à fait', 'il fait', etc:
			if (current_word == 'fait') and (prev_word in ['en', 'à', 'il', 'elle', 'i(l)']) :
				do_liaison = False
				
		# Case 2: Mandatory words + any vowel-initial word, excluding words in exception list
		elif (current_word in liaison_words) and (next_word not in exceptions_next):
			do_liaison = True
			if (current_word == 'aux') and (next_word == 'à'):
				do_liaison = False
				
		# Case 3: Plural noun + vowel-initial adjective
		elif (current_word in plural_nouns) and (next_word in V_adjectives) :
			do_liaison = True

		# Case 4: Adjectives + vowel-initial words (Note: should probably constrain to vowel-initial nouns)
		elif (current_word in adjectives) and (next_word not in exceptions_next) and (next_word not in ['il', 'elle', 'un', 'une', 'en', 'alors', 'à', 'écoutez', 'écoute']) :
			do_liaison = True
		
	return do_liaison

def print_edited(line_index, all_words, k, transcribed_word, file_name):
	# This function prints a list of all the liaison cases that were applied.
	current_word = all_words[k]
	next_word    = all_words[k+1]
	unedited = (current_word + ' ' + next_word).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
	unedited = unedited.decode('cp1252').encode('utf-8')                                   # Back to unicode for printing
	edited   = (transcribed_word + ' ' + dico[next_word]).decode('utf-8').encode('cp1252').ljust(30)
	edited   = edited.decode('cp1252').encode('utf-8')
	# Add a part of the sentence to clarify the context:
	if len(all_words)<6:
		context = all_words
	elif (len(all_words)>=6) and (k<=2):
		context = all_words[:6]
	elif (len(all_words)>=6) and (k>2) and (k<= len(all_words)-2):
		context = all_words[k-2:k+3]
	else:
		context = all_words[-6:]
	context = ' '.join(context)
	print >> file_name, (str(line_index + 1).ljust(5) + unedited + edited + context)
	

# Read line by line, transcribe from dictionary and apply liaison if appropriate
with open('extract.txt') as input_file:
	for line_ID, line_text in enumerate(input_file):
		newwords  = []
		full_line = line_text.lower().split()
		info  = full_line[:4] # ID and age
		words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		for i, word in enumerate(words[:-1]): 
			if word in dico:
				newwords.append(dico[word]) # Transcribe the word
				lastletter = word[-1]
				if (lastletter in liaison) and check_liaison(words, i) :
					newwords[i] += liaison[lastletter] # Attach liaison consonant
					nextword = words[i+1]
					print_edited(line_ID, words, i, newwords[i], f)
			else:
				newwords.append('#') 
		newwords.append(full_line[-1])
		print >> foutput , ' '.join(info + newwords) # Concatenate with ID and age and print
f.close()
foutput.close()

# LIQUID DELETION
f2 = open('liquid_deletion_cases.txt', 'w')
foutput2 = open('recoded_L_D.txt', 'w')

# Symbols used as in Lexique: http://www.lexique.org/outils/Manuel_Lexique.htm#_Toc108519023
obstruents = ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'S', 'Z']
liquids = ['l', 'R']
nasals = ['m', 'n', 'N']
consonants = obstruents + liquids + nasals

def check_liquid_deletion(all_words, k) :
	do_liquid_deletion = False
	current_word = all_words[k]
	next_word = all_words[k+1]
	is_OL_cluster = (len(current_word)>2) and (current_word[-2] in obstruents) and (current_word[-1] in liquids)
	if (is_OL_cluster) and (next_word[0] in consonants):
		do_liquid_deletion = True
	return do_liquid_deletion
	
def print_liquid_del(line_index, all_words_phon, k, all_words_ort, transcribed_word, file_name):
	# This function prints a list of all the liaison cases that were applied.
	current_word = all_words_phon[k]
	next_word    = all_words_phon[k+1]
	unedited = (current_word + ' ' + next_word).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
	unedited = unedited.decode('cp1252').encode('utf-8')                                   # Back to unicode for printing
	edited   = (transcribed_word + ' ' + next_word).decode('utf-8').encode('cp1252').ljust(30)
	edited   = edited.decode('cp1252').encode('utf-8')
	# Add a part of the sentence to clarify the context:
	if len(all_words_ort)<6:
		context = all_words_ort
	elif (len(all_words_ort)>=6) and (k<=2):
		context = all_words_ort[:6]
	elif (len(all_words_ort)>=6) and (k>2) and (k<= len(all_words_ort)-2):
		context = all_words_ort[k-2:k+3]
	else:
		context = all_words_ort[-6:]
	context = ' '.join(context)
	print >> file_name, (str(line_index + 1).ljust(5) + unedited + edited + context)

text_ort = []
with open('extract.txt') as original_file:
	for line_ID, line_text in enumerate(original_file):
		text_ort.append(line_text.strip())
		
with open('recoded_with_liaison.txt') as input_file:
	
		for line_ID, line_text in enumerate(input_file):
			newwords  = []
			full_line = line_text.split()
			full_line_ort = text_ort[line_ID].split()
			info  = full_line[:4] # ID and age
			words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
			words_ort = full_line_ort[4:]
			for i, word in enumerate(words[:-1]): 
				newwords.append(word)
				if (word != '#') and check_liquid_deletion(words, i) :
					newwords[i] = word[:-1] # Delete liquid
					nextword = words[i+1]
					print_liquid_del(line_ID, words, i, words_ort, newwords[i], f2)
			newwords.append(full_line[-1])
			print >> foutput2 , ' '.join(info + newwords) # Concatenate with ID and age and print
f2.close()
foutput2.close()