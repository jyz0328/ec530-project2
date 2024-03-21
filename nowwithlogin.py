#python3 ./nowwithlogin.py
from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import spacy
from textblob import TextBlob
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于加密会话
#app.secret_key = secrets.token_hex(16)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

# 加载 NLP 模型
nlp = spacy.load("en_core_web_sm")

# 假设的用户存储
users = {"admin": {"password": "admin"}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)

class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"}), 401

class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return jsonify({"message": "Logged out"})

class FileUpload(Resource):
    @login_required
    def post(self):
        if 'document' not in request.files:
            return jsonify({"error": "No file part"})
        file = request.files['document']
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        if file:
            text = file.read().decode("utf-8")
            analysis_result = analyze_document(text)
            return jsonify(analysis_result)

def analyze_document(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'ADJ')]
    blob = TextBlob(text)
    sentiment = blob.sentiment
    summary = '. '.join(text.split('. ')[:3]) + '.'
    return {
        "entities": entities,
        "keywords": keywords,
        "sentiment": sentiment.polarity,
        "summary": summary
    }

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(FileUpload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
