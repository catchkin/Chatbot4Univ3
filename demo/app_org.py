import sys
sys.path.append('F:\dev\Chatbot4Univ2')

from api import ChatbotApi



# tensorflow gpu 메모리 할당
# tf는 시작시 메모리를 최대로 할당하기 때문에, 0번 GPU를 2GB 메모리만 사용하도록 설정함


chatbot = ChatbotApi(host='127.0.0.1', port=5000)
chatbot.start()

#@chatbot.api.route('/')
#def index():
#    return render_template("index.html")


#if __name__ == '__main__':
    #chatbot.api.template_folder = chatbot.root_dir + 'templates'
    #chatbot.api.static_folder = chatbot.root_dir + 'static'
    #chatbot.run(host='127.0.0.1', port=5000)
#    chatbot.start()



