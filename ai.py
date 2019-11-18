import sys
import ast
from tkinter.filedialog import askopenfilename
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.cloud.automl_v1beta1 import PredictionServiceClient
from PIL import Image
def chose_file():
    result_l.pack()
    result_l["text"]="loading image"
    file_path = askopenfilename()
    with open(file_path, 'rb') as ff:
        content = ff.read()
        img_r=Image.open(file_path)
        img=img_r.load()
        img_tk=ImageTk.PhotoImage(img_r)
        #w,h=img.getpixel(("x","y"))
    label = tk.Label(window, image=img_tk)
    label.image=img_tk
    label.pack()
    with open(file_path, 'rb') as ff:
        content = ff.read()
        img_r=Image.open(file_path)
        img=img_r.load()
    response=get_prediction(content, project_id,  model_id)
    result_l["text"]="no result"
    for result in response.payload:
        result_l["text"]=result.display_name
        break
def get_prediction(content, project_id, model_id):
  prediction_client = PredictionServiceClient.from_service_account_file("")#your json file
  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned
window=tk.Tk()
window.title("AI")
result_l=tk.Label(window)
summit_b=tk.Button(window,text="choose and summit",command=chose_file).pack()
project_id = ""#your project id
model_id = ""#your model id
window.mainloop()
