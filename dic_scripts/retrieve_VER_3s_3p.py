f3s = open('output_VER3s.txt', 'w')
f3p = open('output_VER3p.txt', 'w')

#consonants = ['s','t','p','n','r']
freqVER3s = {}
freqVER3p = {}

with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[3][:3] == 'VER') and (':3s;' in aux[10]) and (aux[0][-1] == 't'):
			freqVER3s[aux[0]] = aux[8] # Retrieve frequency of all 3rd person singular verbs in films
		elif (aux[3][:3] == 'VER') and (':3p;' in aux[10]) and (aux[0][-1] == 't'):
			freqVER3p[aux[0]] = aux[8] # Retrieve frequency of all 3rd person plural verbs in films

with open('Lexique380.txt') as dic:
	for line in dic:
		aux = line.split('\t')
		if (aux[0] in freqVER3s) and (aux[3] != 'VER') and (float(aux[8]) > float(freqVER3s[aux[0]])):
			del freqVER3s[aux[0]]
		if (aux[0] in freqVER3p) and (aux[3] != 'VER') and (float(aux[8]) > float(freqVER3p[aux[0]])):
			del freqVER3p[aux[0]]
	
for verb, v in sorted(freqVER3s.items()):
	print >> f3s, verb

for verb, v in sorted(freqVER3p.items()):
	print >> f3p, verb
	
f3s.close()
f3p.close()