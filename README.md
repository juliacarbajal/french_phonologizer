# Liaison
This script reads a cleaned-up orthographic transcription of corpora from CHILDES and transcribes it phonologically based on the Lexique380 French dictionary. In the phonological transcription, I automatised the implementation of 4 phonological rules of French, as described in Ngon et al. 2013: obligatory _liaison_, liquid deletion, schwa insertion and resyllabification (_enchainement_).

## Files
The main script is called **recode_v2.py**. It is written for Python 2. No special libraries need to be installed.

### Input
The following files are required to run the code
* **extract.txt**: This file contains a clean orthographic transcription of a corpus. Each line corresponds to one utterance, preceded by the name of the file and the age of the child at the moment the utterance was produced.
* **french.dic**: This is a simplified version of the Lexique380 French dictionary. It contains only two columns, one with the orthographic forms, and one with the phonological forms.
* **output_ADJ.txt**: List of adjectives, extracted from Lexique380.
* **output_NOMp.txt**: List of plural nouns, extracted from Lexique380.
* **h_aspire.txt**: List of words beginning with h-aspiré, obtained from Wikipedia.

### Output
The following output files are produced when running recode_v2.py. Note that all phonological rules output lists include line number, orthographic form and context to facilitate checking the output.
* **liaison_cases.txt**: List of all cases where liaison was applied.
* **liquid_deletion_cases.txt**: List of all cases where liquid deletion was applied.
* **schwa_insertion_cases.txt**: List of all cases where schwa insertion was applied.
* **enchainement_cases.txt**: List of all cases where enchainement was applied. Note that the script is sequential and so enchainement cases are printed as they are applied. This means that enchainement cases involving more than one word will appear through several successive lines. To check the final output, note the line number and check the corresponding line in recoded_L_D_S_E.txt.
* **recoded_with_liaison.txt**: Phonological transcription of the corpus with only liaison applied.
* **recoded_L_D.txt**: Phonological transcription of the corpus with liaison + liquid deletion.
* **recoded_L_D_S.txt**: Phonological transcription of the corpus with liaison + liquid deletion + schwa insertion.
* **recoded_L_D_S_E.txt**: Phonological transcription of the corpus with liaison + liquid deletion + schwa insertion + enchainement.

## To Do
* Adapt code for batch processing.
