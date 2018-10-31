# This script searches Lexique380 to retrieve nouns.
# It only saves the nouns for which this gram. categ. is the most frequent for the word

fp = open('output_NOMp.txt', 'w')
fs = open('output_NOMs.txt', 'w')

freqNOMp = {}
freqNOMs = {}
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[3] == 'NOM') and (aux[5] == 'p'):
			freqNOMp[aux[0]] = aux[8] # Retrieve frequency of all plural nouns in films
		elif (aux[3] == 'NOM') and (aux[5] == 's'):
			freqNOMs[aux[0]] = aux[8] # Retrieve frequency of all singular nouns in films

# Keep only those words for which 'noun' is the most frequent category
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[0] in freqNOMp) and (aux[3] != 'NOM') and (float(aux[8]) > float(freqNOMp[aux[0]])):
			del freqNOMp[aux[0]]
		if (aux[0] in freqNOMs) and (aux[3] != 'NOM') and (float(aux[8]) > float(freqNOMs[aux[0]])):
			del freqNOMs[aux[0]]
	
for noun, v in sorted(freqNOMp.items()):
	print >> fp, noun		
for noun, v in sorted(freqNOMs.items()):
	print >> fs, noun	
	
fp.close()
fs.close()