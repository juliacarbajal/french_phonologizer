# A toolbox for phonologizing French infant-directed speech corpora
These scripts allow to clean orthographic transcriptions of corpora from CHILDES and transform them into an approximate phonological transcription based on the Lexique380 French dictionary with the addition of several French phonological rules: obligatory _liaison_, liquid deletion, schwa insertion (optional), resyllabification (_enchaînement_) and _je_-devoicing. All scripts are written in Python 2.

## Input files
This phonologizer works with CHILDES orthographic transcriptions of speech written in CHAT format. In order to process a corpus, you must download the collection of *.cha files for the given corpus from CHILDES, and store them in the directory **corpora/corpus_name/** under a new subdirectory called **raw/**. We do not provide the *.cha files for the corpora we have processed here, but they can be downloaded from https://childes.talkbank.org/.

## Main scripts
The phonologizer is separated into three scripts: **clean_corpus.py**, **phonologize.py** and **compile.py**, to be used in that order.

### Cleaning
The cleaning script **clean_corpus.py** takes the orthographic transcriptions located under each directory **corpora/corpus_name/raw/** and cleans them up, returning a simplified transcription with no annotations. This transcription is a concatenation of all the *.cha files found in the directory. During this step, utterances from children are filtered out.

The output of this script is a single file called **extract.txt**, located under **corpora/corpus_name/clean/**.

### Phonologizing
The script **phonologize.py** takes the cleaned-up files **extract.txt** from each corpus in the directory **corpora/** and produces an approximate phonological transcription based on the Lexique380 French dictionary, with the addition of the following French phonological rules: obligatory _liaison_, liquid deletion, schwa insertion (optional), resyllabification (_enchaînement_) and _je_-devoicing. For more information on these rules please read the accompanying paper **Carbajal et al (2018).pdf**.

As the rules are applied in a chain, an output file is produced after each rule, indicating the rules that have been applied so far with a letter: _L for _liaison_, _D for liquid deletion, _S for schwa insertion and _E for _enchaînement_ + _je_-devoicing. For instance, the output file with all rules except schwa insertion applied is called **phonologized_L_D_E.txt**. These files will be saved in the directory **output/corpus_name/**. Additionally, lists of applied cases (and, for _liaison_ only, also rejected cases) will be printed after each rule for debugging. These can be found in the same directory as the phonologized output.

Auxiliary files containing lists of words and dictionaries necessary for processing the phonological rules are contained in the directory **auxiliary/**.

### Compiling corpora
To obtain one final compiled corpus composed of multiple corpora, you should use the **compile.py** script. This script will gather all output files of a specified kind (e.g., orthographic or phonological transcriptions) located in the directory **output/** and concatenate them to obtain one single corpus. This script allows you to define several parameters, such as the age range of the children at the moment of the recording, the inclusion of file info at the beginning of each utterance, as well as some final modifications to the phonological transcription, namely the merging of the rounded and unrounded front nasals vowels (not contrastive in many varieties of French) and the removal of geminates across word boundaries.

The resulting compilation will be saved in the directory **compiled_corpus/**.

## Phonologized corpus of French infant-directed speech
Using these scripts, we built a phonologized corpus of infant-directed speech based on CHILDES corpora, called **corpus_phono_L_D_E_0y0m_2y0m.txt**, which can be found in the directory **compiled_corpus/**. In this corpus we applied liaison, liquid deletion, enchaînement, and “je”-devoicing, but not schwa insertion. Furthermore, we merged the nasal vowels mentioned before, but we did not remove geminates. For further details regarding the included corpora and the processing steps, please read the documentation file **Carbajal et al (2018).pdf**.

## Citing this work
If you use the toolbox and/or the sample phonologized corpus, please cite the following paper:

Carbajal, M.J., Bouchon, C., Dupoux, E. \& Peperkamp, S. (2018) *A toolbox for phonologizing French infant-directed speech corpora.* Retrieved from: https://github.com/juliacarbajal/french_phonologizer
