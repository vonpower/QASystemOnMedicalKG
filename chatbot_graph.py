#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *
import web
import json
'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，抱歉没能回答上来，祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)
urls = (
        '/', 'medical'
    )
chatbot = ChatBotGraph()
class medical:
    def __init__(self):
        self.handler = chatbot
    def POST(self):
        data = json.loads(web.data())
# '''   bearychat outgoing json example    
#  {
#   "token" : "995c98c6d79e22cc4200233e8def6f9c",
#   "ts" : 1355517523,
#   "text" : "!baike 中国",
#   "trigger_word" : "!baike",
#   "subdomain" : "your_domain",
#   "channel_name" : "your_channel",
#   "user_name" : "your_name"
# }
# '''
        question = data["text"].replace(data["trigger_word"],"")
        answer = self.handler.chat_main(question)
        return f'{{"text" : "{answer}"\}}'

if __name__ == '__main__':
        app = web.application(urls, globals())
        app.run()


