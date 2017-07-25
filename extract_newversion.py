import re
import os

location = os.getcwd()
f = open('prueba1.txt','w')

# Get filenames to analyse:
chafiles = []
counter = 0
for file in os.listdir(location):
	try:
		if file.endswith(".cha"):
			print "cha file found:\t", file
			chafiles.append(str(file))
			counter = counter + 1
	except Exception as e:
		raise e
		print "No cha files found."

print "Total files found:\t", counter

# Load participants
participants = []
age = {}
with open('participants.txt') as Plist:
	for line in Plist:
		aux = line.split()
		if (aux[0] == '0') and (aux[2] not in participants):
			participants.append(aux[2])
		if ('Target_Child' in aux[5]):
			child_info = aux[5].split('|')
			age[aux[1]] = child_info[3]

for file in chafiles:
	with open(file) as corpus:
		child_age = age[file]
		child_age = re.sub('[;\.]',' ',child_age)
		continue_next = 0
		print_filename = 1
		for j, line in enumerate(corpus):
			newline = []
			line = line.strip()
			if ((line[0] == '*') and (line[1:4] in participants)) or (continue_next == 1):
				if print_filename == 1:
					print >> f, file+' '+child_age+' ',
				continue_next = 0
				newline = line.replace('["]','')
				newline = newline.replace('[*]','')
				newline = newline.replace('(.)','.')
				newline = newline.replace('(..)','.')
				newline = newline.replace('(...)','.')
				newline = re.sub('\[: .*\]', '', newline) # [: word]
				newline = re.sub('^\+\<$',' ', newline) # +<
				newline = re.sub('^\+,$',' ', newline) # +,
				newline = re.sub('^\+\"$',' ', newline) # +"
				newline = re.sub('\+{2}$',' ', newline) # ++
				newline = re.sub('\+\.\.\.','.', newline) # +...
				newline = re.sub('\+\/\/\.*','.', newline) # +//
				newline = re.sub('\+\/\.*','.', newline) # +/
				newline = newline.replace('  ',' ') # Correct any double spaces
				newline = newline.replace('\t ','\t') # Correct extra spaces at the beginning
				newline = newline.replace('\t','') # Erase initial tab
				if (line[0] == '*'):
					start_text = 5
				else:
					start_text = 0
				if (line[-1] not in ['.',',','?','!',';',':']):
					continue_next = 1
					print_filename = 0
					print >> f, newline[start_text:], # If line is unfinished (continues in next line) keep printing on same line
				else:
					print >> f, newline[start_text:]
					print_filename = 1

f.close()
