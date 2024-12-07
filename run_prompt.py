import openai
import LLMConfigurator
import re
import os
from io import StringIO
import sys
from typing import Optional, Dict


def run_python_code(
    command: str, _globals: Optional[Dict] = None, _locals: Optional[Dict] = None
) -> str:
    _globals = _globals if _globals is not None else {}
    _locals = _locals if _locals is not None else {}

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        exec(command, _globals, _locals)
        sys.stdout = old_stdout
        output = mystdout.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        output = str(e)

    return output


def getPromptParams(prompt_template):
    paraNames = []
    if re.search(r"{{\w+}}", prompt_template):
        paraNames = re.findall(r"{{.*}}", prompt_template)
        for i in range(len(paraNames)):
            paraNames[i] = paraNames[i][2:-2]
    return paraNames


def run_Function(promptvalue, prenunits, model, OpenAIKey, debugvalue):
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OpenAIKey)

    # ready_prompt = open("../PromptTemplate/"+prompt_name+"_Prompt.txt", "r").read()
    ready_prompt = promptvalue
    para_name = getPromptParams(promptvalue)
    for index, key in enumerate(para_name):
        try:
            ready_prompt = ready_prompt.replace("{{%s}}" % key, prenunits[index])
        except Exception as e:
            e = "The number of preworkers is different from the number of parameters in the prompt."
            return {"error": e, "type": "text"}
    Config = LLMConfigurator.Config()
    if debugvalue != "":
        ready_prompt = debugvalue
    Config.add_to_config("prompt", ready_prompt)
    print(ready_prompt)
    try:
        if Config.engine.replace(" ", "") == "dall-e":
            response = client.images.generate(prompt=ready_prompt, n=1, size="512x512")
            image_url = response.data[0].url
            return {"message": image_url, "type": "image"}

        for key in model:
            Config.add_to_config(key, model[key])

        if model["engine"].replace(" ", "") == "gpt-4o":
            response = client.chat.completions.create(
                model="o1-preview",  # Using the correct model name
                messages=[{"role": "user", "content": ready_prompt}],
                temperature=float(Config.temperature),
                max_tokens=int(Config.max_tokens),
                top_p=float(Config.top_p),
                frequency_penalty=float(Config.frequency_penalty),
                presence_penalty=float(Config.presence_penalty),
            )
            output = response.choices[0].message.content
            return {"message": output, "type": "text"}

        response = client.completions.create(
            model=Config.engine.replace(" ", ""),
            prompt=Config.prompt,
            temperature=float(Config.temperature),
            max_tokens=int(Config.max_tokens),
            top_p=float(Config.top_p),
            frequency_penalty=float(Config.frequency_penalty),
            presence_penalty=float(Config.presence_penalty),
        )
        output = response.choices[0].text
        # 只选取第一个生成的内容
        output = output.split("===================")[0]
        # 删除空值之后的内容
        output = output.split("\n")
        # delete the empty string in the list
        output = [i for i in output if i != ""]
        output = "\n".join(output)
        return {"message": output, "type": "text"}
    except Exception as e:
        return {"error": str(e), "type": "text"}


def run_PythonREPL(promptvalue, prenunits, model, debugvalue):
    ready_prompt = promptvalue
    para_name = getPromptParams(promptvalue)
    for index, key in enumerate(para_name):
        ready_prompt = ready_prompt.replace("{{%s}}" % key, prenunits[index])
    if debugvalue != "":
        ready_prompt = debugvalue
    print(ready_prompt)
    try:
        output = run_python_code(ready_prompt)
        return {"message": output, "type": "text"}
    except Exception as e:
        return {"error": str(e), "type": "text"}
