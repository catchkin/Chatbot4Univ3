import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from konlpy.tag import Komoran

# 1. 데이터 불러오기
movie = pd.read_csv("../../변형데이터/영화리뷰.csv")
purpose = pd.read_csv("../../변형데이터/용도별목적대화데이터.csv")
topic = pd.read_csv("../../변형데이터/주제별일상대화데이터.csv")
common_sense = pd.read_csv("../../변형데이터/일반상식.csv")
#add = pd.read_csv("../../변형데이터/추가데이터.csv")
#print(movie.head())

movie.dropna(inplace=True)
purpose.dropna(inplace=True)
topic.dropna(inplace=True)
common_sense.dropna(inplace=True)
#add.dropna(inplace=True)
#print(f"movie shape => {movie.shape}")

#print(movie.columns)

all_data = list(movie['document']) + list(purpose['text']) + list(topic['text']) + list(common_sense['query']) + list(common_sense['answer'])

#print(all_data)
#len(all_data)

# 통합본 생성하고 저장하기
total = pd.DataFrame({'text': all_data})
total.to_csv("../../변형데이터/통합본데이터.csv", index=False)

# 2. 의도 분류 데이터 생성하기
# 0 -> 번호, 1 -> 장소, 2 -> 시간, 3 -> 기타

number = []
place = []
time = []
etc = []

for i in all_data:
    if ('어디' or '장소' or '위치' or '주소') in i: place.append(i)
    elif ('번호' or '전화') in i: number.append(i)
    elif ('시작' or '마감' or '언제' or '기간' or '시간') in i: time.append(i)
    else: etc.append(i)

#print(place)
#print(number)
#print(time)
#print(etc)

#print(len(number))

number_label = []
for _ in range(len(number)):
    number_label.append(0)
#print(f'number: ', len(number_label))


place_label = []
for _ in range(len(place)):
    place_label.append(1)
#print(f'place: ', len(place_label))

time_label = []
for _ in range(len(time)):
    time_label.append(2)
#print(f'time: ', len(time_label))

train_df = pd.DataFrame({'text':number+place+time,
                         'label':number_label+place_label+time_label})
#print(train_df)

train_df.reset_index(drop=True, inplace=True)
print(train_df.tail())

train_df.to_csv("train_data.csv", index=False)

# 적절한 패딩 길이 구하기
data = pd.read_csv('train_data.csv')
#print(data.shape)

tokenizer = Komoran()
data_tokenized = [[token+"/"+POS for token, POS in tokenizer.pos(text_)] for text_ in data['text']]

#print(data_tokenized)

exclusion_tags = [
    'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
]

f = lambda x: x in exclusion_tags
#print(f)

data_list = []
for i in range(len(data_tokenized)):
    temp = []
    for j in range(len(data_tokenized[i])):
        if f(data_tokenized[i][j].split('/')[1]) is False:
            temp.append(data_tokenized[i][j].split('/')[0])
    data_list.append(temp)

#print(f'data_list: ', data_list)
num_tokens = [len(tokens) for tokens in data_list]
#print(f'token: ', num_tokens)
num_tokens = np.array(num_tokens)
#print(f'token: ', num_tokens)

# 평균값, 최댓값, 표준편차
print(f"토큰 길이 평균: {np.mean(num_tokens)}")
print(f"토큰 길이 최대: {np.max(num_tokens)}")
print(f"토큰 길이 표준편차: {np.std(num_tokens)}")

plt.title('all text length')
plt.hist(num_tokens, bins=100)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

select_length = 25
def below_threshold_len(max_len, nested_list):
    cnt = 0
    for s in nested_list:
        if (len(s) <= max_len):
            cnt = cnt + 1

    print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s' % (max_len, (cnt / len(nested_list))))


below_threshold_len(select_length, data_list)

