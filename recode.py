# This Python file uses the following encoding: utf-8
import sys

foutput = open('test_simplerecode.txt','w')

dico = {}

# Load the dictionary:
with open('auxiliary/french.dic') as dic:
	for line in dic:
		line = line.decode('cp1252').encode('utf-8')
		aux = line.split()
		if len(aux) == 2:
			dico[aux[0]] = aux[1]

# Special symbols to be added to dictionary:
dico["\*"]="#"  
dico["l'"]="l'" 
dico["d'"]="d'" 
dico["m'"]="m'" 
dico["n'"]="n'" 
dico["c'"]="s'" 
dico["t'"]="t'" 
dico["s'"]="s'" 
dico["j'"]="Z'"
dico[","]=","
dico["?"]="?"
dico["!"]="!"
dico["."]="."
dico[";"]=";"
dico[":"]=":"

# Read line by line and search words in dictionary:
with open('corpus/short_extract.txt') as input_file:
	for j, line in enumerate(input_file):
		line = line.decode('cp1252').encode('utf-8')
		newwords = []
		full_line = line.lower().split()
		info = full_line[:4]
		words = full_line[4:] # Start reading in 5th column, first 4 are ID and age
		for i, word in enumerate(words[:-1]): 
			if word in dico:
				newwords.append(dico[word]) # Transcribe the word
			else:
				newwords.append('#') 
		newwords.append(full_line[-1])
		newsentence = ' '.join(info + newwords) # Concatenate sentence with ID and age
		newsentence = newsentence.replace("' ",'') # Attach consonants with apostrophe to next word
		print >> foutput , newsentence

foutput.close()