# This Python file uses the following encoding: utf-8
import sys # This is not necessary anymore (but I'll keep it as a reminder that I might reintroduce it for batch-processing)

f = open('liaisonv2.txt', 'w')
foutput = open('outputpruebav2.txt','w')

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
				 'plus','très','bien','quand','comment','trop','beaucoup']

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
special['font'] = ['ils','elles']
special['veulent'] = ['ils','elles']
special['peuvent'] = ['ils','elles']
special['doivent'] = ['ils','elles']
special['savent'] = ['ils','elles']
special['valent'] = ['ils','elles']
special['faisait'] = ['il','elle','on']
special['voulait'] = ['il','elle','on']
special['pouvait'] = ['il','elle','on']
special['devait'] = ['il','elle','on']
special['savait'] = ['il','elle','on']
special['valait'] = ['il','elle','on']
special['faisaient'] = ['ils','elles']
special['voulaient'] = ['ils','elles']
special['pouvaient'] = ['ils','elles']
special['devaient'] = ['ils','elles']
special['savaient'] = ['ils','elles']
special['valaient'] = ['ils','elles']
special['faudrait'] = ['il','elle','on']
special['voudrait'] = ['il','elle','on']
special['pourrait'] = ['il','elle','on']
special['devrait'] = ['il','elle','on']
special['saurait'] = ['il','elle','on']
special['vaudrait'] = ['il','elle','on']
special['faudraient'] = ['ils','elles']
special['voudraient'] = ['ils','elles']
special['pourraient'] = ['ils','elles']
special['devraient'] = ['ils','elles']
special['sauraient'] = ['ils','elles']
special['vaudraient'] = ['ils','elles']
# Auxiliaries in clitic groups:
special['était'] = ['il','elle','on']
special['serait'] = ['il','elle','on']
special['allait'] = ['il','elle','on']
special['irait'] = ['il','elle','on']
special['sont'] = ['ils','elles']
special['étaient'] = ['ils','elles']
special['seraient'] = ['ils','elles']
special['allaient'] = ['ils','elles']
special['iraient'] = ['ils','elles']
special['vas'] = 'y'
special['allez'] = 'y'
special['allons'] = 'y'
special['prends'] = 'en'
special['prenez'] = 'en'
special['prenons'] = 'en'

# Exceptions
# Words beginning with h-aspiré (list retrieved from wikipedia article: https://fr.wikipedia.org/wiki/H_aspiré)
h_aspire = []
with open('h_aspire.txt') as Hlist:
	for line in Hlist:
		line = line.strip()
		h_aspire.append(line)
			
exceptions_next = ['et', 'oh', 'euh', 'ah', 'ou'] + h_aspire

# TRANSCRIBE:
# Read line by line and search words in dictionary
with open('extract.txt') as input_file:
	for j, line in enumerate(input_file):
		line = line.decode('cp1252').encode('utf-8')
		newwords = []
		full_line = line.lower().split()
		info = full_line[:4]
		words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		for i, word in enumerate(words[:-1]): 
			if word in dico:
				newwords.append(dico[word]) # Transcribe the word
				nextword = words[i+1]
				lastletter = word[-1]
				if (word in plural_nouns) and (nextword in V_adjectives): #NOTE TO SELF: THIS HAS TO BE PUT INTO A FUNCTION!
					newwords[i] += liaison[lastletter] # Attach liaison consonant
					unedited = (word + ' ' + nextword).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
					unedited = unedited.decode('cp1252').encode('utf-8') # Back to unicode for printing
					edited = (newwords[i] + ' ' + dico[nextword])
					print >> f, (str(j+1).ljust(5)+unedited+ edited)
				elif word in special and nextword in special[word]:
					newwords[i] += liaison[lastletter] # Attach liaison consonant
					unedited = (word + ' ' + nextword).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
					unedited = unedited.decode('cp1252').encode('utf-8') # Back to unicode for printing
					edited = (newwords[i] + ' ' + dico[nextword])
					print >> f, (str(j+1).ljust(5)+unedited+ edited)
				elif word in liaison_words and nextword in dico:
					firstphon = dico[nextword][0] # Read first phoneme of next word
					if firstphon in vowels and \
					nextword not in exceptions_next:
						newwords[i] += liaison[lastletter] # Attach liaison consonant
						unedited = (word + ' ' + nextword).decode('utf-8').encode('cp1252').ljust(30) # Reencode in ANSI to left-justify
						unedited = unedited.decode('cp1252').encode('utf-8') # Back to unicode for printing
						edited = (newwords[i] + ' ' + dico[nextword])
						print >> f, (str(j+1).ljust(5)+unedited+ edited)
			else:
				newwords.append('#') 
		newwords.append(full_line[-1])
		print >> foutput , ' '.join(info + newwords) # Concatenate with ID and age
f.close()
foutput.close()