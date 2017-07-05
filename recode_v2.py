# This Python file uses the following encoding: utf-8
import sys # This is not necessary anymore (but I'll keep it as a reminder that I might use it)

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

# Load the dictionary:
with open('french.dic') as dic:
	for line in dic:
		line = line.decode('cp1252').encode('utf-8')
		aux = line.split()
		if len(aux) == 2:
			dico[aux[0]] = aux[1]

# Liaison
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
adjectives = []
with open('output_ADJ.txt') as ADJlist:
	for line in ADJlist:
		line = line.strip()
		if line[-1] in liaison: # Only adjectives finishing in a liaison consonant
			adjectives.append(line)
	
liaison_words = ['un', 'des', 'les', 'ces',\
                 'mon', 'ton', 'son', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs',\
				 'aux', 'aucun', 'tout', 'quels', 'quelles', 'quelques',\
				 'on', 'nous', 'vous', 'ils', 'elles',\
				 'est', 'ont', 'chez', 'dans', 'en', 'sans',\
				 'plus','très','bien','quand','comment','trop','beaucoup']

liaison_words = liaison_words + adjectives
exceptions_next = ['et','oh','euh','hein', 'ah', 'ou']

# Read line by line and search words in dictionary:
#count_liaison = 0
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
				if word in liaison_words and nextword in dico:
					firstphon = dico[nextword][0] # Read first phoneme of next word
					if firstphon in vowels and \
					nextword not in exceptions_next:
						newwords[i] += liaison[lastletter] # Attach liaison consonant
						#count_liaison += 1
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