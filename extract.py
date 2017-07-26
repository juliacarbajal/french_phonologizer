import re
import os

location = os.getcwd()
f = open('extract.txt','w')

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

# Load participants and child's info:
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

def clean_text(current_line):
	# This function cleans the CHAT annotations based on the
	# CHILDES transcription guidelines: http://talkbank.org/manuals/CHAT.pdf
	new_line = current_line.replace('www','*') # Untranscribed material
	new_line = new_line.replace('0','*')       # Untranscribed material
	new_line = new_line.replace('xxx','*')     # Unintelligible words
	new_line = new_line.replace('yyy','*')
	new_line = new_line.replace('xx','*')
	new_line = new_line.replace('yy','*')
	new_line = new_line.replace('["]','')
	new_line = new_line.replace('[*]','')
	new_line = new_line.replace('(.)',',')     # Pauses, replaced by commas
	new_line = new_line.replace('(..)',',')
	new_line = new_line.replace('(...)',',')
	new_line = new_line.replace(':eng','')           # This marks english words
	new_line = re.sub('\[:\s[^\]]*\]', '', new_line) # [: smth] This notes the intended word
	new_line = re.sub('\[=\s[^\]]*\]', '', new_line) # [= smth] This notes the meaning of a referent
	new_line = re.sub('\[%\s[^\]]*\]', '', new_line) # [% smth] This is an annotation.
	new_line = re.sub('\[[^\]]*\]', '', new_line)    # Delete the rest of the brackets.
	new_line = re.sub('&=[^ ]*', '', new_line)       # Delete &=event annotations.
	new_line = new_line.replace('+<', '')    # Overlaps (we ignore them)
	new_line = new_line.replace('+"/.', '.') # Quotation follows (included as normal speech)
	new_line = new_line.replace('+"', '')    # Quotation (included as normal speech)
	new_line = new_line.replace('+,', '')    # Completion of utterance after interruption
	new_line = new_line.replace('++', '')    # Other completion
	new_line = new_line.replace('+...', '.') # Incomplete utterance (trailing off).
	new_line = new_line.replace('+..?', '?') # Incomplete question (trailing off).
	new_line = new_line.replace('+.', '.')   # Transcription break
	new_line = new_line.replace('+!?',  '?') # Question with great amazement.
	new_line = new_line.replace('+/.',  '.') # Utterance interrupted.
	new_line = new_line.replace('+/?',  '?') # Question interrupted.
	new_line = new_line.replace('+//.', '.') # Self interruption.
	new_line = new_line.replace('+//?', '?') # Self interruption.
	new_line = new_line.replace('+/', '.')   # If any +/ left, replace by stop.
	new_line = new_line.replace('+', ' ')    # Separate words joined by +
	new_line = new_line.replace('_', '-')    # Composed words transcribed with _ replaced by -
	new_line = new_line.replace(',', ' ,')   # Add space before comma
	new_line = new_line.replace(';', ' ;')   # Add space before semicolon
	new_line = new_line.replace('..', '.')   # Correct double stops
	new_line = new_line.replace('. .', '.')  # Correct double stops
	new_line = new_line.replace('.', ' .')   # Add space before stops
	new_line = new_line.replace('<', '')     # < This marks repetitions, we delete the symbol but keep the citation
	new_line = new_line.replace('>', '')     # > This marks repetitions, we delete the symbol but keep the citation
	new_line = re.sub('.+',' ', new_line) # This is some code for audio files, to discard.
	new_line = re.sub('@.','',new_line)   # Special annotations about certain words, we erase the annotation but keep the word.
	new_line = new_line.replace(':','')   # Except for :eng, the colon just indicates a stretch in the sound, so we erase it.
	new_line = new_line.replace("'","' ") # Add a space after apostrophe (we break down words like c'est, l'a, etc)
	new_line = new_line.replace("aujourd' hui","aujourd'hui") # We correct aujourd'hui (broken in previous line)
	new_line = new_line.replace("quelqu'  un","quelqu'un")    # We correct quelqu'un/e
	return new_line

def print_line(current_line, filename):
	if (current_line[-1] not in ['.','?','!']):
		continue_line = 1 # If line is unfinished (continues in next line) keep printing on same line
		print >> f, current_line,
	else:
		print >> f, current_line
		continue_line = 0
	return continue_line

# Read and clean files:
for file in chafiles:
	print "Analysing file: ", file
	child_age = age[file]
	child_age = re.sub('[;\.]',' ',child_age) # Replace age written as "y;m.d" by "y m d"
	continue_line = 0
	with open(file) as corpus:	
		for j, line in enumerate(corpus):
			line = line.strip()
			is_adult_speaking = ((line[0] == '*') and (line[1:4] in participants)) or (continue_line == 1)
			if is_adult_speaking:
				if (line[0] == '*'):
					start_text = 6
				else:
					start_text = 0
				thisline = line[start_text:]
				newline  = clean_text(thisline)
				# Final corrections (white space, punctuation marks):
				newline = newline.split()
				if (continue_line == 0) and (newline[0]==','): # Note: only do this in first line of a dialog
					newline = newline[1:] # Get rid of any comma left at the beginning of the line
				newline = ' '.join(newline)
				newline = newline.replace(', .','.')
				newline = newline.replace(', ,',',')
				newline = newline.replace('. .','.')
				
				# Print:
				if (continue_line == 1):
					continue_line = print_line(newline, f)
				elif (continue_line == 0) and (newline != '.') and (newline != '* .'):
					print >> f, file+' '+child_age+' ',
					continue_line = print_line(newline, f)

f.close()
