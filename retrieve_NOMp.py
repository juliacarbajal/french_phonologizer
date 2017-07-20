# This script searches Lexique380 to retrieve plural nouns.
# It only saves the nouns for which this gram. categ. is the most frequent for the word

f = open('output_NOMp.txt', 'w')
#f2 = open('duplicates.txt','w')

freqNOM = {}
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[3] == 'NOM') and (aux[5] == 'p'):
			freqNOM[aux[0]] = aux[8] # Retrieve frequency of all plural nouns in films

# Keep only those words for which 'noun' is the most frequent category
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[0] in freqNOM) and (aux[3] != 'NOM') and (float(aux[8]) > float(freqNOM[aux[0]])):
			del freqNOM[aux[0]]
	
for noun, v in sorted(freqNOM.items()):
	print >> f, noun		
	
f.close()
#f2.close()