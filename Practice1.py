from textblob import TextBlob
from textblob.taggers import NLTKTagger

zen = TextBlob("Beautiful is better than ugly. "
               "Explicit is better than implicit. "
               "Simple is better than complex.")

print(str(zen.words))
print(str(zen.sentences))

for sentence in zen.sentences:
    print(sentence.sentiment)
    print(sentence.noun_phrases.count())

nltk_tagger = NLTKTagger()
blob = TextBlob("Tag! You're It!", pos_tagger=nltk_tagger)
print(str(blob.pos_tags))
