import sys
sys.path.append('F:\dev\Chatbot4Univ2')

import threading
import json
import pandas as pd
import tensorflow as tf
import torch

from utils.Preprocess import Preprocess
from models.intent.intentModel import IntentModel
from train_tools.qna.create_embedding_data import create_embedding_data
from utils.FindAnswer import FindAnswer

from flask import Flask, render_template
from flask_cors import CORS

# Flask 애플리케이션
app = Flask(__name__)
CORS(app)

# tensorflow gpu 메모리 할당
# tf는 시작시 메모리를 최대로 할당하기 때문에, 0번 GPU를 2GB 메모리만 사용하도록 설정함
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        tf.config.experimental.set_virtual_device_configuration(gpus[0],
                        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    except RuntimeError as e:
        print(e)


# 로그 기능 구현
from logging import handlers
import logging

#log settings
LogFormatter = logging.Formatter('%(asctime)s,%(message)s')

#handler settings
LogHandler = handlers.TimedRotatingFileHandler(filename='logs/chatbot.log', when='midnight', interval=1, encoding='utf-8')
LogHandler.setFormatter(LogFormatter)
LogHandler.suffix = "%Y%m%d"

#logger set
Logger = logging.getLogger()
Logger.setLevel(logging.ERROR)
Logger.addHandler(LogHandler)

# 전처리 객체 생성
try:
    p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin', userdic='./utils/user_dic.txt')
    #print(p.word_index)
    print("텍스트 전처리기 로드 완료..")
except: print("텍스트 전처리기 로드 실패..")

# 의도 파악 모델
try:
    intent = IntentModel(model_name='./models/intent/intent_model.h5', preprocess=p)
    print("의도 파악 모델 로드 완료..")
except: print("의도 파악 모델 로드 실패..")

# 엑셀 파일 로드
try:
    df = pd.read_excel('train_tools/qna/train_data.xlsx')
    print(df.head())
    print("엑셀 파일 로드 완료..")
except: print("엑셀 파일 로드 실패..")

# pt 파일 갱신 및 불러오기
try:
    create_embedding_data = create_embedding_data(df=df, preprocess=p)
    create_embedding_data.create_pt_file()
    embedding_data = torch.load('train_tools/qna/embedding_data.pt')
    #print(embedding_data)
    print("임베딩 pt 파일 갱신 및 로드 완료..")
except: print("임베딩 pt 파일 갱신 및 로드 실패..")




@app.route('/request_chat/<text>', methods=['GET'])
def request_chat(text: str) -> dict:
    """
    문자열을 입력하면 intent, state, answer 등을 포함한 딕셔너리를 json 형태로 반환합니다.

    :return: json 딕셔너리
    """
    query = text

    # 의도 파악
    #query = "컴공 과사 번호 알려줘"
    # 의도 파악
    intent_pred = intent.predict_class(query)
    intent_name = intent.labels[intent_pred]

    # 답변 검색
    f = FindAnswer(df=df, embedding_data=embedding_data, preprocess=p)
    selected_qes, score, answer, imageUrl, query_intent = f.search(query, intent_name)

    if score < 0.6:
        answer = "부정확한 질문이거나 답변할 수 없습니다.\n 빠른 시간 안에 답변을 업데이트 하겠습니다. :("
        imageUrl = "없음"
        # 사용자 질문, 예측 의도, 선택된 질문, 선택된 질문 의도, 유사도 점수
        Logger.error(f"{query},{intent_name},{selected_qes},{query_intent},{score}")

    result = {
        'state': 'SUCCESS',
        "query": selected_qes,
        "answer": answer,
        "intent": query_intent,
    }

    return result



@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


