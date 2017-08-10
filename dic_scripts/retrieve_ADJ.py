f = open('output_ADJ.txt', 'w')
#f2 = open('duplicates.txt','w')

freqADJ = {}
with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if aux[3][:3] == 'ADJ':
			freqADJ[aux[0]] = aux[8] # Retrieve frequency of all adjectives in films

with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[0] in freqADJ) and (aux[3] != 'ADJ') and (float(aux[8]) > float(freqADJ[aux[0]])):
			del freqADJ[aux[0]]
	
for adj, v in sorted(freqADJ.items()):
	print >> f, adj		
	
f.close()
#f2.close()