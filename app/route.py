from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import app
from app.utils.nlp import analyze_text  # 假设这个函数执行NLP分析并返回摘要和实体
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}  # 根据需要调整

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件在POST请求中
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            summary, entities = analyze_text(filepath)  # 对上传的文件进行NLP分析
            return render_template('analysis.html', summary=summary, entities=entities)

    return render_template('upload.html')
