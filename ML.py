import nltk
from nltk import word_tokenize
#from nltk.corpus import stopwords

#stop  = stopwords.words('english')


text = word_tokenize('Add now for something completely different')
print(str(nltk.pos_tag(text)))
