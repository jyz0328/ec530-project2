import spacy

# 加载spaCy英语模型
nlp = spacy.load("en_core_web_sm")

# 文档分析逻辑
def analyze_document(filepath):
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
  #need to modify in route.py
