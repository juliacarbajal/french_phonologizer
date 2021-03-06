# This Python file uses the following encoding: utf-8

######################################################################################
#
#    CORPUS CLEANING SCRIPT FOR CHILDES TRANSCRIPTIONS (2018)
#
#    Authors: Julia Carbajal, Camillia Bouchon, Emmanuel Dupoux & Sharon Peperkamp
#    Contact: carbajal.mjulia@gmail.com   or   sharon.peperkamp@ens.fr
#
######################################################################################

# NOTE: Please verify that all corpora to be processed are located in corpora/corpus_name/raw/
# (one folder per corpus, containing .cha files) before running this script.

import re
import os

root='corpora'
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

######################################################################################
#### FUNCTIONS ####

def clean_text(current_line):
	# This function cleans the CHAT annotations based on the
	# CHILDES transcription guidelines: http://talkbank.org/manuals/CHAT.pdf
	new_line = current_line.replace('www','#') # Untranscribed material
	new_line = new_line.replace('xxx','#')     # Unintelligible words
	new_line = new_line.replace('yyy','#')
	new_line = new_line.replace('xx','#')
	new_line = new_line.replace('yy','#')
	new_line = new_line.replace('0','')        # Note: In CHAT manual they say 0 means omitted word, but in York they use it a lot even in words that are not likely to be omitted, so I will ignore it for the moment.
	new_line = new_line.replace('["]',',')     # I decided to introduce a comma after a quote as there usually are prosodic boundaries.
	new_line = new_line.replace('[*]','')	   # This is a replacement marker (ignore)
	new_line = new_line.replace('[/]',',')	   # This marks a repetition after a pause, we introduce a comma
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
	new_line = new_line.replace('peut+être', 'peut-être') # Correct spelling of peut-être
	new_line = new_line.replace('+', ' ')    # Separate words joined by +
	new_line = new_line.replace('_', '-')    # Composed words transcribed with _ replaced by -
	new_line = new_line.replace(',', ' ,')   # Add space before comma
	new_line = new_line.replace(';', ' ;')   # Add space before semicolon
	new_line = new_line.replace('..', '.')   # Correct double stops
	new_line = new_line.replace('. .', '.')  # Correct double stops
	new_line = new_line.replace('.', ' .')   # Add space before stops
	new_line = new_line.replace('?', ' ?')   # Add space before question mark
	new_line = new_line.replace('!', ' !')   # Add space before exclamation mark
	new_line = new_line.replace('<', '')     # < This marks repetitions, we delete the symbol but keep the citation
	new_line = new_line.replace('>', '')     # > This marks repetitions, we delete the symbol but keep the citation
	new_line = re.sub('.+',' ', new_line) # This is some code for audio files, to discard.
	new_line = re.sub('@.','',new_line)   # Special annotations about certain words, we erase the annotation but keep the word.
	new_line = new_line.replace(':','')   # Except for :eng, the colon just indicates a stretch in the sound, so we erase it.
	new_line = new_line.replace("'","' ") # Add a space after apostrophe (we break down words like c'est, l'a, etc)
	new_line = new_line.replace("j' sais", "j'sais") # We correct j'sais (assimilates, it is included in the dictionary)
	new_line = new_line.replace("j(e) sais", "j'sais") # We correct j(e) sais -> j'sais (same as previous line)
	new_line = new_line.replace("j' suis", "j'suis") # We correct j'suis (assimilates, it is included in the dictionary)
	new_line = new_line.replace("j(e) suis", "j'suis") # We correct j(e) suis -> j'suis (same as previous line)
	new_line = new_line.replace("aujourd' hui","aujourd'hui") # We correct aujourd'hui
	new_line = new_line.replace("quelqu'  un","quelqu'un")    # We correct quelqu'un/e
	new_line = re.sub('(ʁ|ʃ|ʌ)', '*', new_line) # Replace problematic character appearing in Lyon (mar09a.cha)
	return new_line

def print_line(current_line, processed_lines, filename):
	if (current_line[-1] not in ['.','?','!']):
		continue_line = 1 # If line is unfinished (continues in next line) combined processed lines
		processed_lines = processed_lines + current_line.strip() + ' '
	else:
		processed_lines = processed_lines + current_line
		# Final details (potentially multi-line problems):
		processed_lines = processed_lines.replace(', ,',',')
		processed_lines = processed_lines.replace('. .','.')
		processed_lines = processed_lines.replace(', .','.')
		processed_lines = processed_lines.replace(', ?','?')
		processed_lines = processed_lines.replace(', !','!')
		processed_lines = processed_lines.replace("est ce qu", "est-ce qu")         # Add a dash to est-ce (usually transcribed without the dash in CHILDES)
		processed_lines = processed_lines.replace("est c(e) qu", "est-ce qu")       # Add a dash to est-c(e) and remove parenthesis (est-ce will later be transcribed as /Es/)
		processed_lines = processed_lines.replace("n' est ce pas", "n' est-ce pas") # Expression
		processed_lines = processed_lines.replace("qui est ce ?", "qui est-ce ?")   # Expression
		processed_lines = processed_lines.replace("c' est-ce", "c' est ce")         # Remove the dash if it was added to c'est ce
		print >> f, processed_lines
		processed_lines = ''
		continue_line = 0
	return continue_line, processed_lines

def correct_names_lyon_corpus(current_line, file):
	# Correction of name spellings which were shortened in Lyon corpus
	current_line = re.sub('( ana | Ana )', ' Anaïs ', current_line)
	current_line = re.sub('Ana ', 'Anaïs ', current_line)
	current_line = re.sub('( chl | Chl )', ' Chloé ', current_line)
	current_line = re.sub('Chl ', 'Chloé ', current_line)
	current_line = re.sub('( nat | Nat )', ' Nathan ', current_line)
	current_line = re.sub('Nat ', 'Nathan ', current_line)
	current_line = re.sub('( jea | Jea )', ' Jean ', current_line)
	current_line = re.sub('Jea ', 'Jean ', current_line)
	current_line = re.sub('( tim | Tim )', ' Théotime ', current_line)
	current_line = re.sub('Tim ', 'Théotime ', current_line)
	current_line = re.sub('( ger | Ger )', ' Géraldine ', current_line)
	current_line = re.sub('Ger ', 'Géraldine ', current_line)
	if   file[:3] == 'ana':
		current_line = current_line.replace('Chi ', 'Anaïs ').replace('Mar ','Marc ').replace('Fle ','Fleur ')
	elif file[:3] == 'mar':
		current_line = current_line.replace('Chi ', 'Marie ').replace('Mar ', 'Marie ')
	elif file[:3] == 'nat':
		current_line = current_line.replace('Chi ', 'Nathan ').replace('Bro ','Jean ').replace('Mar ', 'Marie ')
	elif file[:3] == 'tim':
		current_line = current_line.replace('Chi ', 'Théotime ').replace('Mar ', 'Marie ')
	return current_line

def utterance_not_empty(current_line):
	not_empty = False
	for k in current_line:
		if k not in [',', '.', ':', ';', '?', '!', ' ', '#', '*', '@']:
			not_empty = True
	return not_empty

def get_participants(chafiles):
	participants = []
	age = {}
	children = ['child','target_child','brother','sister','playmate','girl','boy','cousin']
	for chafile in chafiles:
		with open(input_location +'\\'+ chafile, mode = 'rU') as file:
			for line in file:
				aux = re.split(r'\t+', line.strip())
				if aux[0] == '@ID:':
					participant_info = aux[1].split('|')
					participant_tag  = participant_info[2]
					participant_type = participant_info[7]
					participant_age  = participant_info[3]
					if (participant_type.lower() not in children) and (participant_tag not in participants):
						participants.append(participant_tag)
					elif (participant_type.lower() == 'target_child') or (participant_tag == 'CHI') and (chafile not in age):
						age[chafile] = participant_age
	return participants, age

######################################################################################
#### CLEANING ####

for corpusdir in dirlist:
	print 'Processing corpus:', corpusdir
	input_location = root + '\\' + corpusdir + '\\raw'
	output_location = root + '\\' + corpusdir + '\\clean'
	if not os.path.exists(output_location):
		os.makedirs(output_location)
	
	output_file = output_location + '\\extract.txt'
	f = open(output_file,'w')

	# Get filenames to analyse:
	chafiles = []
	counter = 0
	for file in os.listdir(input_location):
		try:
			if file.endswith(".cha"):
				chafiles.append(str(file))
				counter = counter + 1
		except Exception as e:
			raise e
			print "No cha files found."

	print "Total files found:\t", counter

	# Load participants and child's age:
	participants, age = get_participants(chafiles)

	# Read and clean files:
	for file in chafiles:
		print "Analysing file: ", file
		child_age = age[file]
		if child_age[-1] == '.':
			child_age = child_age + '00' # Add 00 days if days missing from age, e.g. age = "2;8."
		elif child_age[-1] == ';':
			child_age = child_age + '0.00' # Add 0 months and 00 days if info missing from age, e.g. age = "2;"
		child_age = re.sub('[;\.]',' ',child_age) # Replace age written as "y;m.d" by "y m d"
		continue_line = 0
		processed_lines = ''
		with open(input_location +'\\'+ file, mode = 'rU') as corpus:	
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
					# Final corrections (punctuation marks, correction of names):
					newline = newline.split()
					if (len(newline) > 0):
						if (continue_line == 0) and (newline[0]==','): # Note: only do this in first line of a dialogue
							newline = newline[1:] # Get rid of any comma left at the beginning of the line
						newline = ' '.join(newline)
						if corpusdir == 'lyon':
							newline = correct_names_lyon_corpus(newline, file)
						
						# Print:
						if (continue_line == 1):
							continue_line, processed_lines = print_line(newline, processed_lines, f)
						elif (continue_line == 0) and (utterance_not_empty(newline)): #(newline != '.') and (newline != '# .') and (newline != '?') and (newline != '!'):
							print >> f, file + ' ' + child_age + ' ',
							continue_line, processed_lines = print_line(newline, processed_lines, f)

	f.close()
	print 'Corpus', corpusdir, 'done!\n'
