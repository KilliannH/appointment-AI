from nltk.tag import StanfordPOSTagger
import os
import sys

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = TOP_DIR + '/resources/standford_tagger/models/french.tagger'
JAR_FILE = TOP_DIR + '/resources/standford_tagger/stanford-postagger.jar'

st = StanfordPOSTagger(MODEL, JAR_FILE)

test_sentance = sys.argv[1]

output = st.tag(test_sentance.split())

print(output)
