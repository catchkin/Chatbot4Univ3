import sys
sys.path.append('F:\dev\Chatbot4Univ3')

from chatbot.utils.Preprocess import Preprocess
from chatbot.models.intent.intentModel import IntentModel

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.txt')

intent = IntentModel(model_name='../models/intent/intent_model.h5', preprocess=p)

query = "컴공 과사 번호 알려줘"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(f'질문: ', query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "본관 건물 위치 어디야?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(f'질문: ', query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "OOO행사 제출 마감 날짜 알려줘"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(f'질문: ', query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)
print("="*30)
