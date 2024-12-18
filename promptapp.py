from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
import json
from run_prompt import *

from exploration_view import Exploration
from clarify import generate_query_expansion
from deployproInfor import generate_deploypreInfor
from decompose import Generasteps
from Metaprompt_gpt3 import gen_for_gpt3
import subprocess
from subprocess import PIPE
import zipfile
import io
import requests
# import gevent.pywsgi
# import gevent.monkey
# from flask_sslify import SSLify


port = 5000
app = Flask(__name__)
CORS(app)
# sslify = SSLify(app)
# CORS(app, supports_credentials=True)

# 创建一个动态路由
@app.route('/project/<project>')
def project(project):
    return render_template('project.html', project = f"{project}")

@app.route('/get_project_data',methods = ['POST','GET'])
def get_json_data():
    data = request.form
    print(data)
    with open('static/project/' + data['project'] + '.json', 'r',encoding='UTF-8') as file:
        jsondata = json.load(file)
    return json.dumps(jsondata)

@app.route('/sapperIDE')
def index():
    return render_template("PromptSapper.html")

@app.route('/sapper')
def sapperuser():
    return render_template("sapper.html")

@app.route('/Deploy',methods = ['POST','GET'])
def Deploy():
    if request.method == 'POST':
        data = request.form
        with open("pychain/PromptTemplate.json", 'w', encoding='utf-8') as f1:
            json.dump(data["prompt"], f1, ensure_ascii=False)
        f1.close()
        with open("pychain/storage.json", 'w', encoding='utf-8') as f4:
            json.dump([], f4, ensure_ascii=False)
        f4.close()
        f2 = open("pychain/DeployCodeTemp.py", "r").read()
        GenCodeList = data["GenCode"].split("\n")
        GenCode = GenCodeList[0] + "\n"
        for i in range(1, len(GenCodeList)):
            GenCode += "    " + GenCodeList[i] + "\n"
        f2 = f2.replace("{{GenCode}}", GenCode).replace("\t","    ")
        f3 = open("pychain/GenCode.py", "w", encoding="utf-8")
        f3.write(f2)
        f3.close()
        code_cmd = "python pychain/app.py"
        r = subprocess.run(args=code_cmd, shell=True, encoding='utf-8', stdout=PIPE)
        print(r.stdout)
        return "http://127.0.0.1:5000/PromptSapper"

@app.route('/download',methods = ['POST'])
def download():
    data = request.get_json()
    data = data["data"]
    print(data)
    with open("pychain/PromptTemplate.json", 'w', encoding='utf-8') as f1:
        json.dump(data["prompt"], f1, ensure_ascii=False)
    f1.close()
    with open("pychain/storage.json", 'w', encoding='utf-8') as f4:
        json.dump([], f4, ensure_ascii=False)
    f4.close()
    f2 = open("pychain/DeployCodeTemp.py", "r").read()
    GenCodeList = data["GenCode"].split("\n")
    GenCode = GenCodeList[0] + "\n"
    for i in range(1, len(GenCodeList)):
        GenCode += "    " + GenCodeList[i] + "\n"
    f2 = f2.replace("{{GenCode}}", GenCode).replace("\t","    ")
    f3 = open("pychain/GenCode.py", "w", encoding="utf-8")
    f3.write(f2)
    f3.close()
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w') as myzip:
        # 向压缩包中添加文件
        myzip.write('pychain/app.py')
        myzip.write('pychain/GenCode.py')
        myzip.write('pychain/PromptTemplate.json')
        myzip.write('pychain/storage.json')
        myzip.write('pychain/sapperchain.py')
        myzip.write('pychain/LLMConfigurator.py')
    # 重置文件指针
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='compressed_files.zip', as_attachment=True)

@app.route('/DeployPreInfo',methods = ['POST','GET'])
def DeployPreInfo():
    if request.method == 'POST':
        data = request.form
        print(data)
        result = generate_deploypreInfor(data['prompt'], data['OpenAIKey'])
        return result

@app.route('/Clarify',methods = ['POST','GET'])
def Clarify():
    if request.method == 'POST':
        data = request.form
        print(data)
        question, result = generate_query_expansion(data['behaviour'] ,data['message'], data['OpenAIKey'])
        return json.dumps({"question": question, "result": result})

@app.route('/Explore',methods = ['POST','GET'])
def Explore():
    if request.method == 'POST':
        data = request.form
        data = json.loads(data['senddata'])
        print(data['message'])
        explore = Exploration(data['OpenAIKey'])
        explore.prompt = data['message']
        # Call chatbot
        response = explore.chatbot()
        explore.prompt.append({"role": response.role, "content": response.content})
        pre_design = explore.pre_design_view()
        return json.dumps({'Answer':{"role": response.role, "content": response.content}, 'Design': pre_design})

@app.route('/Decompose',methods = ['POST','GET'])
def Decompose():
    if request.method == 'POST':
        data = request.form
        print(data)
        steps = Generasteps(data['message'], data['OpenAIKey'])
        print(steps)
        return json.dumps(steps)

@app.route('/Regetprompt',methods = ['POST','GET'])
def Regetprompt():
    if request.method == 'POST':
        data = request.form
        print(data)
        textinfo = json.loads(data["data"])
        steps = gen_for_gpt3(textinfo["input"],textinfo['message'], data['OpenAIKey'])[0]
        return steps

@app.route('/Classifier',methods = ['POST','GET'])
def Classifier():
    if request.method == 'POST':
        data = request.form
        print(data)
        textinfo = json.loads(data["data"])
        steps = gen_for_gpt3(textinfo["input"],textinfo['message'], data['OpenAIKey'])[0]
        return steps

# @app.route('/Regetprompt',methods = ['POST','GET'])
# def get_wiki_data(title, first_paragraph_only):
#     url = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext=1&titles={title}"
#     if first_paragraph_only:
#         url += "&exintro=1"
#     data = requests.get(url).json()
#     text = list(data["query"]["pages"].values())[0]
#     if "missing" in text:
#         return "not found"
#     return text["extract"]

@app.route('/Getprompt',methods = ['POST','GET'])
def Getprompt():
    if request.method == 'POST':
        data = request.form
        requery = json.loads(data['message'])
        res = {}
        for step in requery.keys():
            prompts = gen_for_gpt3(requery[step]['input'],requery[step]['content'], data['OpenAIKey'])
            res[step] = []
            for pro in prompts:
                res[step].append({'context': pro})
        # return generate_query_expansion(data['function'], data['message'])
        return json.dumps(res)

@app.route('/SapperUnit',methods = ['POST','GET'])
def SapperUnit():
    if request.method == 'POST':
        data = request.form
        data = json.loads(data["senddata"])
        print(data["action"])
        try:
            debugvalue = ""
            if "debugvalue" in data.keys():
                debugvalue = data["debugvalue"]
            if data["action"] == "run_Function":
                print("on_run")
                preunits = data["preunits"].split("#*#*")
                preunits.reverse()
                preunits.pop()
                preunits.reverse()
                model = json.loads(data["model"])
                prompt = data["prompt_name"]
                OpenAIKey = data["OpenAIKey"]
                print(OpenAIKey)
                print(model)
                output = run_Function(prompt, preunits, model,OpenAIKey,debugvalue)
                return json.dumps(output)
            if data["action"] == "run_SerpAPIWrapper":
                print("on_run")
                preunits = data["preunits"].split("#*#*")
                preunits.reverse()
                preunits.pop()
                preunits.reverse()
                model = json.loads(data["model"])
                prompt = data["prompt_name"]
                output = run_SerpAPIWrapper(prompt, preunits, model,debugvalue)
                return json.dumps(output)
            if data["action"] == "run_PythonREPL":
                print("on_run")
                preunits = data["preunits"].split("#*#*")
                preunits.reverse()
                preunits.pop()
                preunits.reverse()
                model = json.loads(data["model"])
                prompt = data["prompt_name"]
                output = run_PythonREPL(prompt, preunits, model,debugvalue)
                # output = "python"
                return json.dumps(output)
        except Exception as e:
            print(e)
            return str(e)

# Modern interface route
@app.route('/modern')
def modern_interface():
    return render_template('modern.html')

# Chat API endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')

    # Here you can integrate with your existing backend logic
    # For now, we'll just echo back a response
    response = {
        'response': f"You said: {message}"
    }

    return jsonify(response)

if __name__ == '__main__':
    # app.run(processes=True,debug=False,port=5000,ssl_context=('fullchain.pem', 'privkey.key'),host='0.0.0.0')
    # gevent_server = gevent.pywsgi.WSGIServer(('0.0.0.0', 5000),app)
    # gevent_server.serve_forever()
    app.run(debug=False)
