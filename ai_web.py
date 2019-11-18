import sys
import ast
from tkinter.filedialog import askopenfilename
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.cloud.automl_v1beta1 import PredictionServiceClient
from PIL import Image, ImageTk
from werkzeug import secure_filename
import werkzeug
import os
project_id = "972041640099"
model_id = "ICN8068115169550532608"
def get_prediction(content, project_id, model_id):
  prediction_client = PredictionServiceClient.from_service_account_file("AI_KEY.json")
  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned
from flask import Flask, redirect, url_for, request ,render_template
app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template("ai_web.html")
@app.route('/summit',methods = ['POST', 'GET'])
def summit():
    f = request.files['file']
    f.save(f.filename)
    try:
        with open(f.filename, 'rb') as ff:
            content = ff.read()
            #img_r=Image.open(f.filename)
            #img=img_r.load()
    except:
        re="You can only upload photo."
    try:
        response=get_prediction(content, project_id,  model_id)
        for result in response.payload:
            re=result.display_name.replace("Many_sugar","High sugar")
            break
    except:
        re="You can only upload photo."

    #get_prediction(secure_filename(f.filename),project_id,model_id)
    return render_template("summit_web.html",res=re)
