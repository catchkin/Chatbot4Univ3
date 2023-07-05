import sys
sys.path.append('F:\dev\Chatbot4Univ2')

# 단어 사전 파일 생성 코드입니다.
# 챗봇에 사용하는 사전 파일

from chatbot.utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle
import pandas as pd

# 말뭉치 데이터 읽어오기
movie_review = pd.read_csv('../../../chatbot/변형데이터/영화리뷰.csv')
purpose = pd.read_csv('../../../chatbot/변형데이터/용도별목적대화데이터.csv')
topic = pd.read_csv('../../../chatbot/변형데이터/주제별일상대화데이터.csv')
common_sense = pd.read_csv('../../../chatbot/변형데이터/일반상식.csv')
#print(movie_review.head())

movie_review.dropna(inplace=True)
purpose.dropna(inplace=True)
topic.dropna(inplace=True)
common_sense.dropna(inplace=True)
#print(movie_review)

text1 = list(movie_review['document'])
text2 = list(purpose['text'])
text3 = list(topic['text'])
text4 = list(common_sense['query']) + list(common_sense['answer'])
#for row in text1:
#    print(row)

corpus_data = text1 + text2 + text3 + text4
#print(*corpus_data)

# 말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c)
    #print(pos, end='\n')
    for k in pos:
        dict.append(k[0])
        #print(k[0], end='\n')

#print(dict, end='\n')
# 사전에 사용될 word2index 생성
# 사전의 첫 번째 인덱스에는 OOV 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV', num_words=100000)
tokenizer.fit_on_texts(dict)
#print(tokenizer.word_index, end='\n')
word_index = tokenizer.word_index
print(word_index)

# 사전 파일 생성
f = open("chatbot_dict.bin", "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()
