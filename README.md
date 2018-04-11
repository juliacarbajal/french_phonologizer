# Liaison
These scripts read a cleaned-up orthographic transcription of corpora from CHILDES and transcribes it phonologically based on the Lexique380 French dictionary. The script called **recode.py** only uses the dictionary transcriptions, while in **recode_v2.py** I automatised the implementation of 4 phonological rules of French, as described in Ngon et al. (2013): obligatory _liaison_, liquid deletion, schwa insertion and resyllabification (_enchainement_). All scripts are written for Python 2. No special libraries are required.

## Phonological transcriptions without phonological rules
The main script is called **recode.py**.

### Input files
The following files are required to run the code
* **extract.txt**: This file contains a clean orthographic transcription of a corpus. Each line corresponds to one utterance, preceded by the name of the file and the age of the child at the moment the utterance was produced. An example is given in **test_corpus/short_extract.txt**.
* **auxiliary/french.dic**: This is a simplified version of the Lexique380 French dictionary. It contains only two columns, one with the orthographic forms, and one with the phonological forms.

### Output file
The output will contain the phonological transcription line by line, preceded by the same info that precedes the input extract file.

## Transcriptions with phonological rules
The main script is called **recode_v2.py**. This script will process all corpora included in the **corpora** folder, separated in folders by corpus_name.

### Input
The following files are required to run the code
* **corpora/corpus_name/clean/extract.txt**: This file contains a clean orthographic transcription of a corpus. Each line corresponds to one utterance, preceded by the name of the file and the age of the child at the moment the utterance was produced.
* **auxiliary/french.dic**: This is a simplified version of the Lexique380 French dictionary. It contains only two columns, one with the orthographic forms, and one with the phonological forms.
* **auxiliary/output_ADJ.txt**: List of adjectives, extracted from Lexique380.
* **auxiliary/output_NOMp.txt**: List of plural nouns, extracted from Lexique380.
* **auxiliary/output_VER.txt**: List of verbs in 3rd person plural or singular, extracted from Lexique380.
* **auxiliary/h_aspire.txt**: List of words beginning with h-aspiré, obtained from Wikipedia.

### Output
The following output files are generated when running recode_v2.py. These files will be created separately for each corpus and organised by corpus_name inside an **output** folder.

Note that all phonological rules output lists include line number, orthographic form and context to facilitate checking the output.

* **liaison_cases.txt**: List of all cases where liaison was applied.
* **rejected_liaison_cases.txt**: List of all potential liaison cases where liaison was *not* applied.
* **liquid_deletion_cases.txt**: List of all cases where liquid deletion was applied.
* **schwa_insertion_cases.txt**: List of all cases where schwa insertion was applied.
* **enchainement_cases.txt**: List of all cases where enchainement was applied. Note that the script is sequential and so enchainement cases are printed as they are applied. This means that enchainement cases involving more than one word will appear through several successive lines. To check the final output, note the line number and check the corresponding line in recoded_L_D_S_E.txt.
* **recoded_with_liaison.txt**: Phonological transcription of the corpus with only liaison applied.
* **recoded_L_D.txt**: Phonological transcription of the corpus with liaison + liquid deletion.
* **recoded_L_D_S.txt**: Phonological transcription of the corpus with liaison + liquid deletion + schwa insertion.
* **recoded_L_D_S_E.txt**: Phonological transcription of the corpus with liaison + liquid deletion + schwa insertion + enchainement.

## To Do
* Fix cases of six, dix, neuf (should transform into siz, diz, neuv before vowels).
* Fix problem with "i(l) s ont".
* Turn phonological rules into modules, merge with recode.py and give options of which modules to run.

