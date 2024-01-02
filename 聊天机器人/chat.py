import jieba
from gensim.models import word2vec
import math
#精确模式
result = jieba.lcut("下雨天留客天留我不留",cut_all=False)
print("精确模式分词结果:",result)
#全模式
result =jieba.lcut("下雨天留客天留我不留",cut_all=True)
print("全模式分词结果:",result)
#搜索引擎模式
result = jieba.lcut_for_search("下雨天留客天留我不留")
print("搜索引擎模式分词结果:",result)
#定义词向量转换方法
"""def get_word_vector_result(word):
    word_vector_result =[]
    for i in word_vector_list:
        if i==word:
            word_vector_result.append(1)
        else:
            word_vector_result.append(0)
    return word_vector_result"""
"""word_vector_list=["Python","在","人工智能","领城","应用","广泛"]
#输人要转成词向量的词
inword=input()
#调用词向量转换函数
word_vector=get_word_vector_result(inword)
#输出词向量
print(word_vector)"""
# 导人中文分词库
#对语料库进行分词，分词结果存入 fenci result.txt 文件
fl=open('D:\腾讯实验班\人工智能实践\[2]王子宸+202013230005\聊天机器人\corpus.txt',encoding="utf8")
f2= open('D:\腾讯实验班\人工智能实践\[2]王子宸+202013230005\聊天机器人\\fenci result.txt','a',encoding="utf8")
lines = fl.readlines()
for line in lines:
    line.replace('\t','').replace('\n','').replace(' ','')
    seg_list = jieba.cut(line)
    #将词汇以空格隔开
    f2.write(' '.join(seg_list))
fl.close()
f2.close()
# 获取计算文本向量及其相似度模型
sentences = word2vec.Text8Corpus('D:\腾讯实验班\人工智能实践\[2]王子宸+202013230005\聊天机器人\\fenci result.txt')
model= word2vec.Word2Vec(sentences)
model.save("D:\腾讯实验班\人工智能实践\[2]王子宸+202013230005\聊天机器人\\word2Vec.model")
import json
#加载和解祈模板文件
f3=open('D:\腾讯实验班\人工智能实践\[2]王子宸+202013230005\聊天机器人\\templet.json',encoding="utf8")
str_=f3.read()
content = json.loads(str_)
f3.close()
if not content:  # 如果content为空，说明文件可能没有内容或者读取有误  
    print("Error: File is empty or cannot be read.")
#print(content)
import jieba
import random
#寻我最大相似度的回答
def answer(input):
#存储最大相似度
    similarityMax = 0
    #存储最大相似度问句的下标
    similarityIndex = -1
    #对用户输人做分词处理
    input_word_arr= list(jieba.cut(input))
    #print(input_word_arr)
    #遍历规则库
    for i in range(len(content)):
        title_word_arr = list(jieba.cut(content[i]['question'].replace(' ','')))
        #print(title_word_arr)
        #使用 try...except 语法来做余弦相似度计算，避免因词向量小而引发报错
        #similarity越大越相似
        try:
            similarity = model.wv.n_similarity(input_word_arr,title_word_arr)
            #print(similarity)
        except Exception:
            similarity=0
#存储当前最大相似度及其下标
        if similarityMax<similarity:
            similarityMax= similarity
            similarityIndex = i
            # 随机取一个回复，如果 similarityIndex 为-1,则说明未匹配到相似语句
    if similarityIndex != -1:
        reply_index = math.floor(random.random() * len(content[similarityIndex]['answer']))
        if reply_index >= 0:
            return {"question":content[similarityIndex]['question'],"answer":content[similarityIndex]['answer']}
    return {"question":"无","answer":"抱歉，我不太明白您的意思"}
while True:
    #接受用户输入
    input_str= input("用户:")
    #寻找匹配的答复
    result =answer(input_str)
    #输出结果
    print("匹配到问题:%s 回答:%s"%(result['question'],result['answer']))