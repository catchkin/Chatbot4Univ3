import os
import platform

# 단어 시퀀스 벡터 크기
MAX_SEQ_LEN = 25

def GlobalParams():
    global MAX_SEQ_LEN


root_dir = os.path.abspath(os.curdir)

_ = "\\" if platform.system() == "Windows" else "/"
if root_dir[len(root_dir) - 1] != _:
    root_dir += _

BASE = {
    "root_dir": root_dir.format(_=_),  # 백엔드 루트경로
}


API = {
    "request_chat_url_pattern": "request_chat",  # request_chat 기능 url pattern
}


