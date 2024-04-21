import os
from pathlib import Path
from flask import Flask, flash, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
from waitress import serve
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

load_dotenv()

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
app.config['UPLOAD_FOLDER'] = Path(UPLOAD_FOLDER).absolute()
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/i/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST', "GET"])
def upload_file():
    if request.args.get('api_key') != os.environ.get('API_KEY'):
        return "Unauthorized", 401

    if len(request.files) == 0:
        flash('No file part')
        return "No file part"

    for _, file in request.files.items():
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(path):
                return "File already exists", 409
            file.save(path)
            local_url = url_for('uploaded_file', filename=filename) 

            return urljoin(request.url_root, local_url)
    return "Invalid file", 400

if __name__ == '__main__':
    print("Starting server, listening on port 6500")
    serve(app, host='0.0.0.0', port=6500)
    # app.run(debug=True, host='0.0.0.0', port=6500)