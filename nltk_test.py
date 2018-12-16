from nltk.tag import StanfordPOSTagger
import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = TOP_DIR + '/resources/standford_tagger/models/french.tagger'
JAR_FILE = TOP_DIR + '/resources/standford_tagger/stanford-postagger.jar'

st = StanfordPOSTagger(MODEL, JAR_FILE)

output = st.tag('Salut, comment ça va ?'.split())

print(output)
