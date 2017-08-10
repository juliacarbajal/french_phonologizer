f = open('output_VER.txt', 'w')

consonants = ['s','t','p','n','r']
freqVER = {}
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[3][:3] == 'VER') and ('3' in aux[10]) and (aux[0][-1] in consonants):
			freqVER[aux[0]] = aux[8] # Retrieve frequency of all verbs in films

with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[0] in freqVER) and (aux[3] != 'VER') and (float(aux[8]) > float(freqVER[aux[0]])):
			del freqVER[aux[0]]
	
for verb, v in sorted(freqVER.items()):
	print >> f, verb
	
f.close()