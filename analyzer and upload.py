
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import nltk
from textblob import TextBlob
import requests
import pandas as pd
from docx import Document
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.summarization import summarize
import spacy

# 定义文档分析类
class SmartDocumentAnalyzer:
    def __init__(self):
        # 初始化任何需要的变量
        pass

    # 上传文档并转换为文本

 #I want to upload different types of files (CSV, DOC,pdf,image, etc.)

    def upload_and_convert_document(self, filepath):
        """
        根据文件扩展名，处理PDF或图片文件，并将其内容转换为文本。
        :param filepath: 文件路径
        :return: 文档的文本内容
        """
        # 确定文件类型并相应处理
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == '.pdf':
            return self._convert_pdf_to_text(filepath)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self._convert_image_to_text(filepath)
        elif ext == '.csv':
            return self._convert_csv_to_text(filepath)
        elif ext in ['.docx', '.doc']:  # 假设.doc也以同样方式处理
            return self._convert_docx_to_text(filepath)
        else:
            raise ValueError("不支持的文件类型")
        
 #The application should translate my documents to text
    # PDF转文本
    def _convert_pdf_to_text(self, filepath):
        """
        将PDF文件转换为文本。
        :param filepath: PDF文件路径
        :return: 转换后的文本内容
        """
        # 示例代码，实际应用中可能需要使用更高级的库来处理复杂布局的PDF
        images = convert_from_path(filepath)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)
        return text

    # 图片转文本
    def _convert_image_to_text(self, filepath):
        """
        将图片文件转换为文本。
        :param filepath: 图片文件路径
        :return: 转换后的文本内容
        """
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text

    # 更新上传和转换文档的方法以支持CSV和DOCX
    def upload_and_convert_document(self, filepath):
        """
        根据文件扩展名，处理PDF、图片、CSV、和DOCX文件，并将其内容转换为文本。
        :param filepath: 文件路径
        :return: 文档的文本内容
        """
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == '.pdf':
            return self._convert_pdf_to_text(filepath)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self._convert_image_to_text(filepath)
        elif ext == '.csv':
            return self._convert_csv_to_text(filepath)
        elif ext in ['.docx', '.doc']:  # 假设.doc也以同样方式处理
            return self._convert_docx_to_text(filepath)
        else:
            raise ValueError("不支持的文件类型")

    def _convert_csv_to_text(self, filepath):
        """
        将CSV文件转换为文本。
        :param filepath: CSV文件路径
        :return: 转换后的文本内容
        """
        df = pd.read_csv(filepath)
        text = df.to_string(index=False)  # 转换DataFrame为字符串，不包含索引
        return text

    def _convert_docx_to_text(self, filepath):
        """
        将DOCX文件转换为文本。
        :param filepath: DOCX文件路径
        :return: 转换后的文本内容
        """
        doc = Document(filepath)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
 #I should be able to to find all positive, neutral and negative paragraphs and sentences
    # 关键词提取与情感分析
    def analyze_document_content_emotion(self, text):
        """
        对给定的文本进行关键词提取和情感分析。
        :param text: 文本内容
        :return: 关键词列表和情感分析结果
        """
        # 使用nltk或TextBlob等库来提取关键词和进行情感分析
        # 示例代码，实际应用中需要根据需求调整
        blob = TextBlob(text)
        keywords = nltk.FreqDist(blob.words).most_common(10)  # 提取前10个最常见的词
        sentiment = blob.sentiment
        return keywords, sentiment

    # 更多功能（如外部数据搜索、文档摘要等）可以在这里添加


 # want the service to tag all my documents and paragraphs within every document with the keywords and know the topics each document cover

    def tag_documents_and_paragraphs(self, text):
        """
        标记文档和段落中的关键词，并识别每个文档的主题。
        :param text: 文本内容
        :return: 标记的关键词和主题
        """
        # 使用NLP库来识别关键词和主题，这里是个简化示例
        keywords, _ = self.analyze_document_content_emotion(text)
        # 假设主题分析是基于关键词的进一步分析
        topics = "示例主题"  # 实际应用中需要实现主题分析逻辑
        return keywords, topics
 #I should be able to access different paragraphs of different documents based on keywords
    def find_paragraphs_by_keywords(self, text, keyword):
        """
        根据关键词查找相关的段落。
        :param text: 文本内容
        :param keyword: 要搜索的关键词
        :return: 包含关键词的段落列表
        """
        paragraphs = text.split('\n')  # 假设每个段落由换行符分隔
        relevant_paragraphs = [p for p in paragraphs if keyword in p]
        return relevant_paragraphs

 #I should be able to get summaries of each document
    def generate_document_summary(self, text):
        """
        生成文档的摘要。
        :param text: 文本内容
        :return: 文档的摘要
        """
        # 使用gensim或其他库生成摘要
        summary = summarize(text, word_count=100)  # 限制摘要的词数
        return summary
  #I want to know all names, locations, institutions and address in my documents
    def extract_named_entities(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entities = {
        "persons": [],
        "locations": [],
        "institutions": [],
        "addresses": []  # 地址可能较难直接识别，需要特定逻辑或进一步处理
         }
        for ent in doc.ents:
           if ent.label_ == "PERSON":
            entities["persons"].append(ent.text)
           elif ent.label_ in ["GPE", "LOC"]:  # GPE: 国家、城市等; LOC: 山脉、水体等
            entities["locations"].append(ent.text)
           elif ent.label_ == "ORG":
            entities["institutions"].append(ent.text)
        # 地址识别可能需要特定的逻辑，这里仅为示例
        # 实际应用中可能需要利用正则表达式或专门的地址识别库
        return entities
    

# 示例使用
analyzer = SmartDocumentAnalyzer()
text = analyzer.upload_and_convert_document('example.pdf')
keywords, topics = analyzer.tag_documents_and_paragraphs(text)
print(keywords, topics)

keyword = "示例关键词"
relevant_paragraphs = analyzer.find_paragraphs_by_keywords(text, keyword)
print(relevant_paragraphs)

summary = analyzer.generate_document_summary(text)
print(summary)
