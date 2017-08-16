# This Python file uses the following encoding: utf-8
import os

root='output'
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

# Age limits:
age_min_input = '0y0m' # Eventually make this input user-defined
age_max_input = '2y0m'

f = open('corpus'+age_min_input + '-' + age_max_input+'.txt', 'w')

def parse_age(age_string):
	age = age_string.replace('y','-').replace('m','')
	age = age.split('-')
	age = [int(x) for x in age]
	return age

age_min_y, age_min_m = parse_age(age_min_input)
age_max_y, age_max_m = parse_age(age_max_input)


def check_age(current_age):
	years  = current_age[0]
	months = current_age[1]
	include = False
	if (years < age_max_y and years > age_min_y):
		include = True
	elif (years == age_max_y and years == age_min_y):
		if (months <= age_max_m or months >= age_min_m):
			include = True
	elif (years == age_max_y and years != age_min_y):
		if (months <= age_max_m):
			include = True
	elif (years == age_min_y and years != age_max_y):
		if (months >= age_min_m):
			include = True
	return include


for corpusdir in dirlist:
	location = 'output/' + corpusdir
	with open(location + '/recoded_L_D_S_E.txt') as recoded_file:
		for line_ID, line_text in enumerate(recoded_file):
			line = line_text.split()
			age = [int(x) for x in line[1:4]]
			if check_age(age):
				print >> f, line_text.strip()

f.close()