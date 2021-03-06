import os, re, json, shutil
from flask import Flask, redirect , url_for, render_template , request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from prediction import alarm_pred
import zipfile

app=Flask(__name__)

    
@app.route('/')
def index():
    return render_template('flask.html')

@app.route('/uploads', methods=['POST'])
def upload():
    UPLOAD_FOLDER  = os.getcwd()+'/'+'output'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if os.path.exists(UPLOAD_FOLDER) and os.path.isdir(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER)

    upload_data = request.files['myFile']
    
    # calling function for predicting image
    result = alarm_pred(upload_data)
    # print(os.getcwd())
    shutil.move('false_alarm_report.csv', UPLOAD_FOLDER)
    shutil.move('alarm_action_report.csv', UPLOAD_FOLDER)
    shutil.move('duplication_alarm_report.csv', UPLOAD_FOLDER)

    shutil.make_archive('result', 'zip', 'output')
    
    return render_template('link.html')



@app.route('/download', methods =['GET'])
def download_all():
#     zipf = zipfile.ZipFile('result_file.zip','w', zipfile.ZIP_DEFLATED)
#     for root,dirs, files in os.walk(UPLOAD_FOLDER):
#         for file in files:
#             zipf.write('result_file/'+file)
# #     zipf.close()
    return send_file('result.zip', as_attachment=True, cache_timeout=-1)
if __name__ == '__main__':
    app.run(debug=True)
