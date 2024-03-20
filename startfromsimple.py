from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import spacy
from textblob import TextBlob

# 初始化 Flask 应用和 API
app = Flask(__name__)
api = Api(app)

# 加载 NLP 模型
nlp = spacy.load("en_core_web_sm")

# 文档分析类
class DocumentAnalyze(Resource):
    def analyze(self):
        # 假定文本文件名是 'document.txt'，并且它位于与此代码相同的目录中
        file_path = 'document.txt'
        # 从文件中读取文本
        with open(file_path, 'r') as file:
            text = file.read()
        # 调用文档分析逻辑
        return analyze_document(text)
    
    def post(self):
        # 直接调用analyze函数处理文档并返回分析结果
        analysis_result = self.analyze()
        return jsonify(analysis_result)

    def get(self):
        # 对GET请求也使用相同的分析逻辑并返回结果
        analysis_result = self.analyze()
        return jsonify(analysis_result)

# 文档分析逻辑
def analyze_document(text):
    doc = nlp(text)
    # 命名实体识别
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    # 关键词提取
    keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'ADJ')]
    # 情感分析，使用TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment
    # 摘要生成
    summary = '. '.join(text.split('. ')[:3]) + '.'
    # 返回分析结果
    return {
        "entities": entities,
        "keywords": keywords,
        "sentiment": sentiment.polarity,
        "summary": summary
    }

# 将资源添加到API
api.add_resource(DocumentAnalyze, '/')

if __name__ == '__main__':
    app.run(debug=True)
