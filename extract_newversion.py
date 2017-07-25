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

# Load participants:
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

# Read and clean files:
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
				continue_next = 0
				if (line[0] == '*'):
					start_text = 6
				else:
					start_text = 0
				newline = line[start_text:]
				# Annotations:
				newline = newline.replace('www','*') # Untranscribed material
				newline = newline.replace('xxx','*') # Unintelligible words
				newline = newline.replace('yyy','*')
				newline = newline.replace('xx','*')
				newline = newline.replace('yy','*')
				newline = newline.replace('["]','')
				newline = newline.replace('[*]','')
				newline = newline.replace('(.)',',') # Pauses replaced by commas
				newline = newline.replace('(..)',',')
				newline = newline.replace('(...)',',')
				newline = re.sub('\[:\s[^\]]*\]', '', newline) # [: smth] This notes the intended word
				newline = re.sub('\[=\s[^\]]*\]', '', newline) # [= smth] This notes the meaning of a referent
				newline = re.sub('\[%\s[^\]]*\]', '', newline) # [% smth] This is an annotation.
				newline = re.sub('\[[^\]]*\]', '', newline) # Delete the rest of the brackets.
				newline = re.sub('&=[^ ]*', '', newline) # Delete &=word annotations.
				newline = newline.replace(':eng','') # This marks english words
				# Punctuation marks:
				newline = newline.replace('+<','') # +<
				newline = newline.replace('+,','') # +,
				newline = newline.replace('+"/','') # +"/
				newline = newline.replace('+"','') # +"
				newline = newline.replace('++','') # ++
				newline = newline.replace('+...','.') # +...
				newline = newline.replace('+//','.') # +//
				newline = newline.replace('+/','.') # +/
				newline = newline.replace('+',' ') # Separate words joined by +
				newline = newline.replace('_','-') # Composed words transcribed with _ replaced by -
				newline = newline.replace(',',' ,') # Add space before comma
				newline = newline.replace(';',' ;') # Add space before semicolon
				newline = newline.replace('..','.') # Correct double stops
				newline = newline.replace('.',' .') # Add space before stops
				newline = newline.replace('<','') # < This marks citations, we delete the symbol but keep the citation
				newline = newline.replace('>','') # > This marks citations, we delete the symbol but keep the citation
				newline = re.sub('.+',' ', newline) # This is some code for audio files, to discard.
				newline = re.sub('@.','',newline)
				newline = newline.replace(':','') # Except for :eng, the colon just indicates a stretch in the sound, so we erase it.
				newline = newline.replace("'","' ") # Add a space after apostrophe (we break down words like c'est, l'a, etc)
				newline = newline.replace("aujourd' hui","aujourd'hui") # We correct aujourd'hui (broken in previous line)
				# White spaces:
				newline = ' '.join(newline.split()) # Correct any double or triple spaces
				newline = newline.replace('\t ','\t') # Correct extra spaces at the beginning
				newline = newline.replace('\t','') # Erase initial tab
				
				if (newline != '.') and (newline != '* .'):
					if (print_filename == 1):
						print >> f, file+' '+child_age+' ',
					if (newline[-1] not in ['.',',','?','!',';',':']):
						continue_next = 1
						print_filename = 0
						print >> f, newline, # If line is unfinished (continues in next line) keep printing on same line
					else:
						print >> f, newline
						print_filename = 1

f.close()
