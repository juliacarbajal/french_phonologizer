# This Python file uses the following encoding: utf-8
import sys # This is not necessary anymore (but I'll keep it as a reminder that I might reintroduce it for batch-processing)

f = open('liaisonv3.txt', 'w')
foutput = open('outputpruebav3.txt','w')

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

# Load the plural nouns:
plural_nouns = []
with open('output_NOMp.txt') as NOMlist:
	for line in NOMlist:
		line = line.strip()
		if line[-1] in liaison: # Only nouns finishing in a liaison consonant (this only excludes very few cases that don't finish in s or x)
			plural_nouns.append(line)

# Mandatory liaison:
liaison_words = ['un', 'des', 'les', 'ces',\
                 'mon', 'ton', 'son', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs',\
				 'aux', 'aucun', 'tout', 'quels', 'quelles', 'quelques',\
				 'on', 'nous', 'vous', 'ils', 'elles',\
				 'est', 'ont', 'chez', 'dans', 'en', 'sans',\
				 'plus','très','bien','quand','trop','beaucoup']

liaison_words = liaison_words + adjectives

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

# Exceptions
# Words beginning with h-aspiré (list retrieved from wikipedia article: https://fr.wikipedia.org/wiki/H_aspiré)
h_aspire = []
with open('h_aspire.txt') as Hlist:
	for line in Hlist:
		line = line.strip()
		h_aspire.append(line)
			
exceptions_next = ['et', 'oh', 'euh', 'ah', 'ou', 'u', 'i', 'où'] + h_aspire


def check_liaison(all_words, k) : #current_word, next_word, next_word_2) :
	# This function checks if liaison applies, returns True or False
	current_word = all_words[k]
	next_word    = all_words[k+1]
	next_word_2  = '#'
	prev_word    = '#'
	if (current_word not in punctuation) and (next_word not in punctuation) :
		next_word_2 = all_words[k+2]
	if (k>0) :
		prev_word   = all_words[k-1]
		
	# Case 1: List of mandatory special cases (see above)
	if (current_word in special) and (next_word in special[current_word]) :
		do_liaison = True
		# Correct 'tu vas y + infinitif' cases, e.g. tu vas y arriver:
		if (current_word == 'vas') and ((prev_word == 'tu') or (next_word_2[-2:] in ['er','ir'])) :
			do_liaison = False 
		# Correct 'en fait il/elle' cases, 'tout à fait', 'il fait', etc:
		if (current_word == 'fait') and (prev_word in ['en', 'à', 'il', 'elle', 'i(l)']) :
			do_liaison = False
			
	# Case 2: Mandatory words + any vowel-initial word, excluding words in exception list
	elif (current_word in liaison_words) and (next_word in dico) :
		firstphon = dico[next_word][0] # Read first phoneme of next word
		if (firstphon in vowels) and (next_word not in exceptions_next) :
			do_liaison = True
		else :
			do_liaison = False
			
	# Case 3: Plural noun + vowel-initial adjective
	elif (current_word in plural_nouns) and (next_word in V_adjectives) :
		do_liaison = True
	else :
		do_liaison = False
		
	return do_liaison

def print_edited(line_index, current_word, next_word, transcribed_word, file_name) :
	# This function prints a list of all the liaison cases that were applied.
	unedited = (current_word + ' ' + next_word).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
	unedited = unedited.decode('cp1252').encode('utf-8')                                   # Back to unicode for printing
	edited   = (transcribed_word + ' ' + dico[next_word])
	print >> file_name, (str(line_index + 1).ljust(5) + unedited + edited)
	

# Read line by line, transcribe from dictionary and apply liaison if appropriate
with open('extract.txt') as input_file:
	for j, line in enumerate(input_file):
		newwords  = []
		full_line = line.lower().split()
		info  = full_line[:4] # ID and age
		words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		for i, word in enumerate(words[:-1]): 
			if word in dico:
				newwords.append(dico[word]) # Transcribe the word
				lastletter = word[-1]
				if (lastletter in liaison) and check_liaison(words, i) :
					newwords[i] += liaison[lastletter] # Attach liaison consonant
					nextword = words[i+1]
					print_edited(j, word, nextword, newwords[i], f)
			else:
				newwords.append('#') 
		newwords.append(full_line[-1])
		print >> foutput , ' '.join(info + newwords) # Concatenate with ID and age and print
f.close()
foutput.close()