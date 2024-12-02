import time
import openai
import argparse

openai.api_key = "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"
def gpt3(prompt, t, max_tokens):
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            temperature=t,
            max_tokens=16384,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=""
        )
        return response["choices"][0]["text"]

    except Exception as e:
        print(type(e), e)
        time.sleep(3)

decompose_template = """You are provided a prompt from a user which you will breakdown using a technique called 'task decomposition'. Task decomposition involves breaking down a complex task into a series of smaller subtasks. Each subtask represents a specific part of the overall task and can be processed independently by the LLM. You are going to do with this with the prompt you are given.

The decomposed subtasks are designed to interact with the LLM in a manner similar to human thought process, reflecting both data flow (the movement and transformation of data) and control flow (the order in which the subtasks are executed).

By decomposing tasks in this way, we can guide the LLM more effectively, making it easier for the model to understand the task requirements and generate more accurate and relevant outputs. This approach also makes it easier to manage and troubleshoot the task execution process, as each subtask can be monitored and adjusted independently.

<Task Description>
I want to build a music recommendation system for a music streaming platform that suggests songs to users based on their listening history and ratings they've given to songs.
</Task Description>

<Decomposed Subtasks>

(Subtask1 Input: User_ID Output: Listening_History Model: Database)
Retrieve the listening history of the user from the database.

(Subtask2 Input: User_ID Output: User_Ratings Model: Database)
Retrieve the ratings given by the user from the database.

<Control If Listening_History and User_Ratings are not empty>

(Subtask3 Input: Listening_History, User_Ratings Output: User_Profile Model: User_Profiling_Algorithm)
Generate a user profile based on the listening history and ratings.

(Subtask4 Input: User_Profile Output: Song_Suggestions Model: Recommendation_Algorithm)
Generate song suggestions based on the user profile.

</Control>

<Control If Listening_History or User_Ratings are empty>

(Subtask5 Input: None Output: Song_Suggestions Model: Popular_Songs)
Suggest popular songs when there's not enough data to generate a user profile.

</Control>

(Subtask6 Input: Song_Suggestions Output: Display_Suggestions Model: User_Interface)
Display the song suggestions to the user on the platform.

</Decomposed Subtasks>


<Task Description>
I need to develop a function to obtain the weather conditions of the day according to the weather API and automatically draw 500x500 pixel RGB color paintings that meet the weather conditions, draw abstract paintings when the weather is rainy, and draw natural landscape paintings when the weather is sunny, so as to improve the user experience and entertainment.
</Task Description>

<Decomposed Subtasks >

(Subtask1 Input: None Output: Weather_Data Model OpenWeatherMap)
obtain weather conditions for the day

<Control If Weather equal to rainy>

(Subtask2 Input: Weather_Data Output: Painting_Description Model LLM)
generate descriptions of abstract paintings through weather information.

</Control>

<Control If Weather equal to sunny>

(Subtask3 Input: Weather_Data Output: Painting_Description Model LLM)
generate natural landscape descriptions of abstract paintings through weather information.

</Control>

(Subtask4 Input: Painting_Description Output: Painting; Model Image-generation-model)
Generate 500x500 pixel paintings according to Painting_Description.

</Decomposed Subtasks>


<Task Description>
{{Description}}
</Task Description>
Note: Output cannot have the same name
"""

decompose_template1 = """<Requirement Description>
I need to develop a function to obtain the weather conditions of the day according to the weather API and automatically draw 500x500 pixel RGB color paintings that meet the weather conditions, draw abstract paintings when the weather is rainy, and draw natural landscape paintings when the weather is sunny, so as to improve the user experience and entertainment.
</Requirement Description>

<Decomposed steps>
To achieve this function, you can follow the following steps to analyze and design the process:

(Step1 Input: None Output: API_Interface_Selection)
First, you need to choose an API interface used to obtain weather information. You can select some open weather APIs, such as OpenWeatherMap, AccuWeather, etc.

(Step2 Input: API_Interface_Selection Output: API_Key)
After selecting the API interface, you need to configure the API key to access the API. Generally, the API provider will provide a key, which can be found in the API documentation.

(Step3 Input: API_Key Output: Weather_Data)
Use the API key to access the API to get the weather data of the day. The data format is usually JSON or XML.

(Step4 Input: Weather_Data Output: Parsed_Data_Structure)
Parse the obtained JSON or XML format data into easy-to-handle data structures, such as dictionaries or objects.

(Step5 Input: Parsed_Data_Structure Output: Weather_Type)
Judge the weather type of the day according to the description information in the weather data. It can be classified according to weather conditions, such as sunny, cloudy and rainy days.

(Step6 Input: Weather_Type Output: RGB_Color_Value)
In order to generate paintings that meet weather conditions, you need to map the weather type to the corresponding RGB color value. You can map sunny days to blue tones, rainy days to gray tones, and snowy days to white tones.

(Step7 Input: Weather_Type&RGB_Color_Value Output: Painting)
Generate 500x500 pixel paintings according to weather type and corresponding RGB color values. For rainy days, you can generate abstract paintings, and for sunny days, you can generate natural landscape paintings.

(Step8 Input: Painting Output: Display_Painting)
Display the generated paintings to users to improve user experience and entertainment.
</Decomposed steps>

<Requirement Description>
{{Description}}
</Requirement Description>

<Decomposed steps>
"""

def decompose(query):
    decomposed_steps = gpt3(decompose_template.replace("{{Description}}", query), 0, 16384)
    return decomposed_steps

def Generasteps(query , OpenAIKey):
    openai.api_key = OpenAIKey
    # query = "I need to develop a function that allows users to search for nearby restaurants and hotels according to their current location and display the search results on the map."
    steps = decompose(query).split("\n\n")[1:]
    stepsJson = {}
    for j,step in enumerate(steps):
        if '(Subtask' in step:
            temp = step.split("\n")
            inp = temp[0].split(" ")[2].split("&")
            newinp = [[i, 'no'] for i in inp if i != 'None']
            # for i in inp:
            #     newinp.append([i,'no'])
            oup = temp[0].split(" ")[4]

            mod = temp[0].split(" ")[6][:-1]
            content = temp[1]
            js = {"content": content, "input": newinp, "output": [oup, 'no'], "model": mod}
            name = 'step' + str(j)
            stepsJson[name] = js

    return stepsJson

query = "I need to develop a function that allows users to search for nearby restaurants and hotels according to their current location and display the search results on the map."
query1 = "I need an automatic problem maker that can generate multiple choice math questions based on the difficulty and number of questions entered by the user."
# this code will print the decomposed prompt for us
print(decompose(query))
pat = {"content": "How are you", "input": ["history", "chatbot"],"prompt":["prompt1","prompt2"] ,"output": "human", "model": "LLM"}
