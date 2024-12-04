from sapperchain import sapperchain
import os
import json
from flask import jsonify

file_path = os.path.join(os.path.dirname(__file__), "storage.json")


def read_json():
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(data):
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


f1 = open("pychain/PromptTemplate.json", "r", encoding="UTF-8")
prompt_template = json.loads(f1.read())


def sapper(sapper_request):
    chain = sapperchain(sapper_request["OpenaiKey"])
    chain.promptbase(prompt_template)

    initrecord = {
        "id": "",
        "input": "preInfo",
        "output": [],
        "runflag": "",
        "Empty": "",
        "start": "",
        "option": "",
        "chatbot": "",
        "Scene": "",
        "Answer": "",
        "history_1": "",
        "Question": "",
        "Standard_Answer": "",
        "Evaluation": "",
        "Score": "",
        "sentence": "",
        "Career": "",
        "User_2": "",
        "history_2": "",
        "Helper": "",
        "Judge": "",
        "Advice": "",
        "First_Improvement": "",
        "preInfo": "",
    }
    sapper_query = update_request(initrecord, sapper_request)
    Empty = sapper_query["Empty"]
    start = sapper_query["start"]
    option = sapper_query["option"]
    chatbot = sapper_query["chatbot"]
    Scene = sapper_query["Scene"]
    Answer = sapper_query["Answer"]
    history_1 = sapper_query["history_1"]
    Question = sapper_query["Question"]
    Standard_Answer = sapper_query["Standard_Answer"]
    Evaluation = sapper_query["Evaluation"]
    Score = sapper_query["Score"]
    sentence = sapper_query["sentence"]
    Career = sapper_query["Career"]
    User_2 = sapper_query["User_2"]
    history_2 = sapper_query["history_2"]
    Helper = sapper_query["Helper"]
    Judge = sapper_query["Judge"]
    Advice = sapper_query["Advice"]
    First_Improvement = sapper_query["First_Improvement"]
    preInfo = sapper_query["preInfo"]
    sapper_query["output"] = []
    if sapper_query["runflag"]:
        preInfo = """Hello, welcome to the Smart Contract Assistant. I can guide you through the entire process of developing a smart contract, from basic concepts to advanced functionalities. Also, if you have a smart contract you'd like to review, I can assist in identifying potential issues, optimizing performance, and enhancing security measures."""
        sapper_query["preInfo"] = preInfo
    if sapper_query["runflag"]:
        sapper_query["output"].append(preInfo)
        stop, sapper_query, Unit = get_value("preInfo", sapper_request, sapper_query)
    stop, sapper_query, Empty = get_value("Empty", sapper_request, sapper_query)
    if stop and sapper_query["runflag"]:
        return _extracted_from_sapper_61(sapper_query, "Empty")
    start = "Welcome to Smart Contract Copilot. Please press 1 to enter into Smart Contract Development mode where you can create, test, and deploy your smart contracts seamlessly. Enter 2 to engage in Smart Contract Audit mode where you can thoroughly review and analyze your smart contracts for potential vulnerabilities and compliance issues. Our audit tools provide automated security checks, code quality assessments, and detailed reports to ensure your contracts are robust and secure. Whether you are developing or auditing, Smart Contract Copilot is here to guide you every step of the way."
    if sapper_query["runflag"]:
        sapper_query["output"].append(start)
    stop, sapper_query, option = get_value("option", sapper_request, sapper_query)
    if stop and sapper_query["runflag"]:
        return _extracted_from_sapper_61(sapper_query, "option")
    if option == "1":
        chatbot = "Welcome to Smart Contract Development mode. Here, you can create, test, and deploy your smart contracts seamlessly. I am here to help you with any questions or guidance you may need in developing your smart contracts, from basic concepts to advanced functionalities. Let\'s begin your development journey. Please enter 'Bye' at any time to end the conversation."
        if sapper_query["runflag"]:
            sapper_query["output"].append(chatbot)
        stop, sapper_query, Scene = get_value("Scene", sapper_request, sapper_query)
        if stop and sapper_query["runflag"]:
            return _extracted_from_sapper_61(sapper_query, "Scene")
        while Answer != "Bye":
            if sapper_query["runflag"]:
                Question = chain.worker(
                    "cfMm_^CqC=qE;:%QcQQ0",
                    [history_1, Scene],
                    {
                        "temperature": 0.7,
                        "max_tokens": 861,
                        "stop_strs": "",
                        "top_p": 0.8,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "engine": " gpt-4o-mini",
                    },
                )
                sapper_query["Question"] = Question
            if sapper_query["runflag"]:
                sapper_query["output"].append(Question)
            if sapper_query["runflag"]:
                history_1 = chain.worker(
                    "Q$V+u{Y]P%SZP``Uq(FN",
                    [history_1, Question],
                    {
                        "temperature": 0.7,
                        "max_tokens": 861,
                        "stop_strs": "",
                        "top_p": 1,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "engine": " gpt-4o-mini",
                    },
                )
                sapper_query["history_1"] = history_1
            stop, sapper_query, Answer = get_value(
                "Answer", sapper_request, sapper_query
            )
            if stop and sapper_query["runflag"]:
                return _extracted_from_sapper_61(sapper_query, "Answer")
            if Answer != "Bye":
                if sapper_query["runflag"]:
                    Standard_Answer = chain.worker(
                        "kRan_$l+VgL_*DGf;QKV",
                        [Question],
                        {
                            "temperature": 0.7,
                            "max_tokens": 2048,
                            "top_p": 1,
                            "frequency_penalty": 0,
                            "presence_penalty": 0,
                            "engine": " gpt-4o-mini",
                        },
                    )
                    sapper_query["Standard_Answer"] = Standard_Answer
                if sapper_query["runflag"]:
                    sapper_query["output"].append(Standard_Answer)
                if sapper_query["runflag"]:
                    Evaluation = chain.worker(
                        "@F-Q?_/`-Jh,T7E28Y3@",
                        [Scene, Question, Answer, Standard_Answer],
                        {
                            "temperature": 0.7,
                            "max_tokens": 2848,
                            "top_p": 0.8,
                            "frequency_penalty": 0,
                            "presence_penalty": 0,
                #            "model": "g",
                            "engine": " gpt-4o-mini",
                        },
                    )
                    sapper_query["Evaluation"] = Evaluation
                if sapper_query["runflag"]:
                    sapper_query["output"].append(Evaluation)
                if sapper_query["runflag"]:
                    Score = chain.worker(
                        "TB%LvOBG57D8Ngb`Q92M",
                        [Scene, Question, Answer, Standard_Answer, Evaluation],
                        {
                            "temperature": 0.7,
                            "max_tokens": 2000,
                            "top_p": 1,
                            "frequency_penalty": 0,
                            "presence_penalty": 0,
                            "engine": "gpt-4o-mini",
                        },
                    )
                    sapper_query["Score"] = Score
                if sapper_query["runflag"]:
                    sapper_query["output"].append(Score)
            else:
                chatbot = "Thank you for using Sixiaopin! Good luck in your job search!"
                if sapper_query["runflag"]:
                    sapper_query["output"].append(chatbot)

    elif option == "2":
        chatbot = "Please enter your target occupation:"
        if sapper_query["runflag"]:
            sapper_query["output"].append(chatbot)
        stop, sapper_query, sentence = get_value(
            "sentence", sapper_request, sapper_query
        )
        if stop and sapper_query["runflag"]:
            return _extracted_from_sapper_61(sapper_query, "sentence")
        if sapper_query["runflag"]:
            Career = chain.worker(
                "gIUs*4B8gOPX+_}:E^KI",
                [sentence],
                {
                    "temperature": 0.7,
                    "max_tokens": 836,
                    "stop_strs": "",
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                    "engine": "gpt-4o-mini",
                },
            )
            sapper_query["Career"] = Career
        chatbot = "Please enter your requirements:"
        if sapper_query["runflag"]:
            sapper_query["output"].append(chatbot)
        while User_2 != "Bye":
            stop, sapper_query, User_2 = get_value(
                "User_2", sapper_request, sapper_query
            )
            if stop and sapper_query["runflag"]:
                return _extracted_from_sapper_61(sapper_query, "User_2")
            if sapper_query["runflag"]:
                Helper = chain.worker(
                    "Ck=LJ%.v]r?JvqCbn?if",
                    [history_2, Career, User_2],
                    {
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "top_p": 1,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "engine": "gpt-4o-mini",
                    },
                )
                sapper_query["Helper"] = Helper
            if sapper_query["runflag"]:
                sapper_query["output"].append(Helper)
            if sapper_query["runflag"]:
                history_2 = chain.worker(
                    "ZE4yeBc$rYAJoV]$:D,g",
                    [User_2, history_2, Helper],
                    {
                        "temperature": 0.7,
                        "max_tokens": 1959,
                        "stop_strs": "",
                        "top_p": 1,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "engine": "gpt-4o-mini",
                    },
                )
                sapper_query["history_2"] = history_2
            if User_2 != "Bye":
                chatbot = "Could you please let me know if you are satisfied with this result? (A. Dissatisfied; B. Satisfied.)"
                if sapper_query["runflag"]:
                    sapper_query["output"].append(chatbot)
                stop, sapper_query, Judge = get_value(
                    "Judge", sapper_request, sapper_query
                )
                if stop and sapper_query["runflag"]:
                    return _extracted_from_sapper_61(sapper_query, "Judge")
                if Judge == "A":
                    chatbot = "I'm sorry you're not satisfied with my output. Please provide me with an improvement suggestion, and I will try my best to improve my reply to better meet your needs."
                    if sapper_query["runflag"]:
                        sapper_query["output"].append(chatbot)
                    stop, sapper_query, Advice = get_value(
                        "Advice", sapper_request, sapper_query
                    )
                    if stop and sapper_query["runflag"]:
                        return _extracted_from_sapper_61(sapper_query, "Advice")
                    if sapper_query["runflag"]:
                        First_Improvement = chain.worker(
                            "49]~`,N]7.q$F[TL49HU",
                            [Helper, Advice],
                            {
                                "temperature": 0.7,
                                "max_tokens": 2048,
                                "top_p": 1,
                                "frequency_penalty": 0,
                                "presence_penalty": 0,
                                "engine": "gpt-4o-mini",
                            },
                        )
                        sapper_query["First_Improvement"] = First_Improvement
                    if sapper_query["runflag"]:
                        sapper_query["output"].append(First_Improvement)
                    chatbot = "Could you please let me know if you are satisfied with this result? (A. Dissatisfied; B. Satisfied.)"
                    if sapper_query["runflag"]:
                        sapper_query["output"].append(chatbot)
                    stop, sapper_query, Judge = get_value(
                        "Judge", sapper_request, sapper_query
                    )
                    if stop and sapper_query["runflag"]:
                        return _extracted_from_sapper_61(sapper_query, "Judge")
                    while Judge == "A":
                        if User_2 != "Bye":
                            chatbot = "I'm sorry you're not satisfied with my output. Please provide me with an improvement suggestion, and I will try my best to improve my reply to better meet your needs."
                            if sapper_query["runflag"]:
                                sapper_query["output"].append(chatbot)
                            stop, sapper_query, Advice = get_value(
                                "Advice", sapper_request, sapper_query
                            )
                            if stop and sapper_query["runflag"]:
                                return _extracted_from_sapper_61(sapper_query, "Advice")
                            if sapper_query["runflag"]:
                                First_Improvement = chain.worker(
                                    "PO596X1|.Q_4uocH#ko*",
                                    [First_Improvement, Advice],
                                    {
                                        "temperature": 0.7,
                                        "max_tokens": 2048,
                                        "top_p": 1,
                                        "frequency_penalty": 0,
                                        "presence_penalty": 0,
                                        "engine": "gpt-4o-mini",
                                    },
                                )
                                sapper_query["First_Improvement"] = First_Improvement
                            if sapper_query["runflag"]:
                                sapper_query["output"].append(First_Improvement)
                            chatbot = "Could you please let me know if you are satisfied with this result? (A. Dissatisfied; B. Satisfied.)"
                            if sapper_query["runflag"]:
                                sapper_query["output"].append(chatbot)
                            stop, sapper_query, Judge = get_value(
                                "Judge", sapper_request, sapper_query
                            )
                            if stop and sapper_query["runflag"]:
                                return _extracted_from_sapper_61(sapper_query, "Judge")
                    if Judge == "B":
                        chatbot = "Thank you very much for your feedback. I am happy to help you. Please let me know if you need anything else"
                        if sapper_query["runflag"]:
                            sapper_query["output"].append(chatbot)

                elif Judge == "B":
                    chatbot = "Thank you very much for your feedback. I am happy to help you. Please let me know if you need anything else"
                    if sapper_query["runflag"]:
                        sapper_query["output"].append(chatbot)

    resetquery(sapper_query, initrecord)
    return {"Answer": sapper_query["output"]}


# TODO Rename this here and in `sapper`
def _extracted_from_sapper_61(sapper_query, arg1):
    sapper_query["runflag"] = False
    sapper_query["input"] = arg1
    savequery(sapper_query)
    return {"Answer": sapper_query["output"]}
