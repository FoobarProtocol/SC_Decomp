from sapperchain import sapperchain
import os
import json
from flask import jsonify

# Define paths relative to this module's location
STORAGE_PATH = os.path.join(os.path.dirname(__file__), "storage.json")
PROMPT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "pychain/PromptTemplate.json"
)


def read_json(file_path=STORAGE_PATH):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(data, file_path=STORAGE_PATH):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def update_request(initrecord, query):
    initrecord["id"] = query["id"]
    initrecord["runflag"] = True
    data = read_json()
    has_id = False
    for record in data:
        if record["id"] == query["id"]:
            has_id = True
            return record
    if not has_id:
        new_record = initrecord
        data.append(new_record)
        write_json(data)
        return new_record


def get_value(vary, request, query):
    if vary == query["input"]:
        query["runflag"] = True
        query["input"] = ""
        query[vary] = request["query"]
        return False, query, request["query"]
    else:
        return True, query, query[vary]


def resetquery(query, initrecord):
    initrecord["id"] = query["id"]
    initrecord["runflag"] = True
    query = initrecord
    data = read_json()
    for i in range(len(data)):
        record = data[i]
        if record["id"] == query["id"]:
            data[i] = query
    write_json(data)


def savequery(query):
    data = read_json()
    for i in range(len(data)):
        record = data[i]
        if record["id"] == query["id"]:
            data[i] = query
    write_json(data)


prompt_template = read_json(PROMPT_TEMPLATE_PATH)


def sapper(sapper_request):
    chain = sapperchain(sapper_request["OpenaiKey"])
    chain.promptbase(prompt_template)

    # Execute GenCode functionality
    from .GenCode import sapper

    sapper_result = sapper(sapper_request)
    sapper_query = sapper_result["query"]
    initrecord = sapper_result["initrecord"]

    resetquery(sapper_query, initrecord)
    return {"Answer": sapper_query["output"]}
