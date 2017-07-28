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
vowels = ['a','i','e','E','o','O','u','y','§','1','5','2','9','@','°','3']

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
			
# Exceptions
# Words beginning with h-aspiré (list retrieved from wikipedia article: https://fr.wikipedia.org/wiki/H_aspiré)
h_aspire = []
with open('h_aspire.txt') as Hlist:
	for line in Hlist:
		line = line.strip()
		h_aspire.append(line)
			
exceptions_next = ['et', 'oh', 'euh', 'hum', 'ah', 'ou', 'u', 'i', 'où', 'apparemment', 'alors', 'attends'] + h_aspire

# Liaison cases:

# Cases that apply always except if followed by specific items:
always_except = {}
always_except['un'] = exceptions_next + ['à']
always_except["quelqu'un"] = exceptions_next
always_except['les'] = exceptions_next + ['avec']
always_except['des'] = exceptions_next + ['avec']
always_except['ces'] = exceptions_next + ['avec']
always_except['mon'] = exceptions_next + ['avec']
always_except['ton'] = exceptions_next + ['avec']
always_except['son'] = exceptions_next + ['avec']
always_except['mes'] = exceptions_next + ['avec']
always_except['tes'] = exceptions_next + ['avec']
always_except['ses'] = exceptions_next + ['avec']
always_except['nos'] = exceptions_next + ['avec']
always_except['vos'] = exceptions_next + ['avec']
always_except['leurs'] = exceptions_next
always_except['aux'] = exceptions_next
always_except['aucun'] = exceptions_next
always_except['tout'] = exceptions_next
always_except['toutes'] = exceptions_next
always_except['quels'] = exceptions_next
always_except['quelles'] = exceptions_next
always_except['quelques'] = exceptions_next
always_except['lesquels'] = exceptions_next + ['il', 'ils', 'elle', 'elles']
always_except['lesquelles'] = exceptions_next + ['il', 'ils', 'elle', 'elles']
always_except['auxquels'] = exceptions_next
always_except['auxquelles'] = exceptions_next
always_except['desquels'] = exceptions_next
always_except['desquelles'] = exceptions_next
always_except['plusieurs'] = exceptions_next
always_except['certains'] = exceptions_next
always_except['certaines'] = exceptions_next
always_except['autres'] = exceptions_next + ['à', 'au']
always_except['on'] = exceptions_next
always_except['nous'] = exceptions_next + ['à']
always_except['vous'] = exceptions_next
always_except['ils'] = exceptions_next
always_except['elles'] = exceptions_next
always_except['est'] = exceptions_next + ['adrien']
always_except['ont'] = exceptions_next
always_except['chez'] = exceptions_next
always_except['dans'] = exceptions_next
always_except['en'] = exceptions_next
always_except['sans'] = exceptions_next
always_except['sous'] = exceptions_next
always_except['plus'] = exceptions_next + ['après']
always_except['moins'] = exceptions_next
always_except['très'] = exceptions_next
always_except['bien'] = exceptions_next + ['écoutez', 'écoute', 'il', 'elle']
always_except['trop'] = exceptions_next
always_except['beaucoup'] = exceptions_next

for adjective in adjectives:
	always_except[adjective] = exceptions_next + ['il', 'elle', 'un', 'une', 'en', 'alors', 'à', 'écoutez', 'écoute', 'adrien', 'avec']

# Cases that apply only if followed by specific items:
only_before = {}
# Modal verbs in clitic groups:
only_before['fait'] = ['il','elle','on']
only_before['veut'] = ['il','elle','on']
only_before['peut'] = ['il','elle','on','être']
only_before['doit'] = ['il','elle','on']
only_before['sait'] = ['il','elle','on']
only_before['vaut'] = ['il','elle','on']
only_before['font']    = ['ils','elles']
only_before['veulent'] = ['ils','elles']
only_before['peuvent'] = ['ils','elles']
only_before['doivent'] = ['ils','elles']
only_before['savent']  = ['ils','elles']
only_before['valent']  = ['ils','elles']
only_before['faisait'] = ['il','elle','on']
only_before['voulait'] = ['il','elle','on']
only_before['pouvait'] = ['il','elle','on']
only_before['devait']  = ['il','elle','on']
only_before['savait']  = ['il','elle','on']
only_before['valait']  = ['il','elle','on']
only_before['faisaient'] = ['ils','elles']
only_before['voulaient'] = ['ils','elles']
only_before['pouvaient'] = ['ils','elles']
only_before['devaient']  = ['ils','elles']
only_before['savaient']  = ['ils','elles']
only_before['valaient']  = ['ils','elles']
only_before['faudrait']  = ['il','elle','on']
only_before['voudrait'] = ['il','elle','on']
only_before['pourrait'] = ['il','elle','on']
only_before['devrait']  = ['il','elle','on']
only_before['saurait']  = ['il','elle','on']
only_before['vaudrait'] = ['il','elle','on']
only_before['faudraient'] = ['ils','elles']
only_before['voudraient'] = ['ils','elles']
only_before['pourraient'] = ['ils','elles']
only_before['devraient']  = ['ils','elles']
only_before['sauraient']  = ['ils','elles']
only_before['vaudraient'] = ['ils','elles']
# Auxiliaries in clitic groups:
only_before['était']  = ['il','elle','on', 'un', 'une']
only_before['serait'] = ['il','elle','on']
only_before['allait'] = ['il','elle','on']
only_before['irait']  = ['il','elle','on']
only_before['sont']     = ['ils','elles']
only_before['étaient']  = ['ils','elles']
only_before['seraient'] = ['ils','elles']
only_before['allaient'] = ['ils','elles']
only_before['iraient']  = ['ils','elles']
only_before['vas'] = 'y'
only_before['allez'] = 'y'
only_before['allons'] = 'y'
only_before['prends'] = 'en'
only_before['prenez'] = 'en'
only_before['prenons'] = 'en'
# Others
only_before['comment'] = 'allez'
only_before['quand'] = 'est'
only_before['quant'] = ['à', 'aux']


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
			
		# Case 1: List of cases that apply only before specific items (see above)
		if (current_word in only_before) and (next_word in only_before[current_word]) :
			do_liaison = True
			# Correct 'tu vas y + infinitif' cases:
			if (current_word == 'vas') and ((prev_word == 'tu') or (next_word_2[-2:] in ['er','ir'])) :
				do_liaison = False 
			# Correct 'en fait il/elle' cases, 'tout à fait', 'il fait', etc:
			if (current_word == 'fait') and (prev_word in ['en', 'à', 'il', 'elle', 'i(l)']) :
				do_liaison = False
				
		# Case 2: List of cases that apply always except if followed by specific items
		elif (current_word in always_except) and (next_word not in always_except[current_word]):
			do_liaison = True
			if (current_word == 'aux') and (next_word == 'à'):
				do_liaison = False
				
		# Case 3: Plural noun + vowel-initial adjective
		elif (current_word in plural_nouns) and (next_word in V_adjectives) :
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
					#nextword = words[i+1]
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
	
def print_applied_cases(line_index, all_words_phon, k, all_words_ort, transcribed_word, file_name):
	# This function prints a list of all the liaison cases that were applied.
	current_word_ort = all_words_ort[k]
	next_word_ort    = all_words_ort[k+1]
	next_word_phon    = all_words_phon[k+1]
	unedited = (current_word_ort + ' ' + next_word_ort).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
	unedited = unedited.decode('cp1252').encode('utf-8')                                   # Back to unicode for printing
	edited   = (transcribed_word + ' ' + next_word_phon).decode('utf-8').encode('cp1252').ljust(30)
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
					#nextword = words[i+1]
					print_applied_cases(line_ID, words, i, words_ort, newwords[i], f2)
			newwords.append(full_line[-1])
			print >> foutput2 , ' '.join(info + newwords) # Concatenate with ID and age and print
f2.close()
foutput2.close()


# SCHWA INSERTION

f3 = open('schwa_insertion_cases.txt', 'w')
foutput3 = open('recoded_L_D_S.txt', 'w')

def check_C_cluster(word_phon,onset_or_coda):
	is_C_cluster = False
	if len(word_phon)>2 :
		if onset_or_coda == 'coda':
			phon1 = word_phon[-2]
			phon2 = word_phon[-1]
		elif onset_or_coda == 'onset':
			phon1 = word_phon[0]
			phon2 = word_phon[1]
		if (phon1 in consonants) and (phon2 in consonants):
			is_C_cluster = True
	return is_C_cluster
			
def check_schwa_insertion(all_words, k) :
	do_insert_schwa = False
	current_word = all_words[k]
	next_word    = all_words[k+1]
	if check_C_cluster(current_word,'coda') and check_C_cluster(next_word,'onset'):
		do_insert_schwa = True
	return do_insert_schwa

with open('recoded_L_D.txt') as input_file:
	for line_ID, line_text in enumerate(input_file):
		newwords  = []
		full_line = line_text.split()
		full_line_ort = text_ort[line_ID].split()
		info  = full_line[:4] # ID and age
		words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		words_ort = full_line_ort[4:]
		for i, word in enumerate(words[:-1]): 
			newwords.append(word)
			if (word != '#') and check_schwa_insertion(words, i) :
				newwords[i] += '°' # Add schwa
				#nextword = words[i+1]
				print_applied_cases(line_ID, words, i, words_ort, newwords[i], f3)
		newwords.append(full_line[-1])
		print >> foutput3 , ' '.join(info + newwords) # Concatenate with ID and age and print
	
f3.close()
foutput3.close()


# ENCHAINEMENT

f4 = open('enchainement_cases.txt', 'w')
foutput4 = open('recoded_L_D_S_E.txt', 'w')
			
def check_enchainement(all_words, k) :
	do_enchainement = False
	current_word = all_words[k]
	next_word    = all_words[k+1]
	if (current_word[-1] in (consonants + ["'"])) and (next_word[0] in vowels):
		do_enchainement = True
	return do_enchainement

def print_enchainement(line_index, k, all_words_ort, transcribed_word, transcribed_word_2, file_name):
	# This function prints a list of all the liaison cases that were applied.
	current_word_ort = all_words_ort[k]
	next_word_ort    = all_words_ort[k+1]
	unedited = (current_word_ort + ' ' + next_word_ort).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
	unedited = unedited.decode('cp1252').encode('utf-8')                                   # Back to unicode for printing
	edited   = (transcribed_word + ' ' + transcribed_word_2).decode('utf-8').encode('cp1252').ljust(30)
	edited   = edited.decode('cp1252').encode('utf-8')
	if (edited[0] == ' '):
		edited = edited[1:] # Correct empty spaces when the first word was absorbed fully by second word
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
	
with open('recoded_L_D_S.txt') as input_file:
	for line_ID, line_text in enumerate(input_file):
		newwords  = []
		full_line = line_text.split()
		full_line_ort = text_ort[line_ID].split()
		info  = full_line[:4] # ID and age
		newwords = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		words_ort = full_line_ort[4:]
		for i, word in enumerate(newwords[:-1]): 
			if (word != '#') and check_enchainement(newwords, i) :
				currentword = newwords[i]
				final_consonant = word[-1]
				if final_consonant != "'":
					newwords[i] = currentword[:-1] # Enchainement
					newwords[i+1] = final_consonant + newwords[i+1]
				else:
					newwords[i] = currentword[:-2] # Enchainement
					newwords[i+1] = currentword[-2:] + newwords[i+1]
					newwords[i+1] = newwords[i+1].replace("'",'') # Erase the apostrophe
				print_enchainement(line_ID, i, words_ort, newwords[i], newwords[i+1], f4)
		newwords = filter(None, newwords)
		print >> foutput4 , ' '.join(info + newwords) # Concatenate with ID and age and print
	
f4.close()
foutput4.close()
