import os
import openai
import datetime
import json

# set up OpenAI API key
openai.api_key = "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"

# set up prompt for GPT-3
prompt = "Synthetic dataset: Here is an example of a synthetic dataset for a machine learning model that predicts whether a customer will churn or not.\n\n"
prompt += "Dataset:\n"
prompt += "Customer ID | Age | Gender | Tenure | Balance | Num. Products | Credit Score | Churn\n"
prompt += "-----------------------------------------------------------------------------------------\n"
prompt += "001        | 35  | M      | 2      | 5000   | 3          | 700       | 0\n"
prompt += "002        | 42  | F      | 4      | 8000   | 4          | 650       | 1\n"
prompt += "003        | 28  | M      | 1      | 2000   | 2          | 750       | 0\n"
prompt += "004        | 39  | F      | 3      | 6000   | 3          | 800       | 1\n"
prompt += "005        | 52  | M      | 5      | 10000  | 4          | 625       | 0\n"
prompt += "006        | 23  | F      | 2      | 3500   | 2          | 675       | 1\n"
prompt += "007        | 31  | M      | 3      | 4500   | 2          | 600       | 0\n"
prompt += "008        | 47  | F      | 6      | 9000   | 3          | 750       | 1\n"
prompt += "009        | 26  | M      | 4      | 5000   | 3          | 725       | 0\n"
prompt += "010        | 38  | F      | 5      | 7000   | 2          | 650       | 1\n\n"
prompt += "Can you generate a similar dataset for me with a different set of features and outcomes? If so then generate a dataset for smart contracts that features an instruction or a problem, an input and then the proper output when the instructions are properly followed. The data produced by this dataset will be used to fine-tune a large language model to develop expert abilities in solidity programming.\n"

# Artificially generate creation epoch time
created = int(datetime.datetime.now().timestamp())

# Define the GPT-3 model name
model_name = "gpt-4-0613"

# Call OpenAI API
response = openai.ChatCompletion.create(
  model=model_name,
  messages=[
        {"role": "system", "content": prompt},
  ]
)

# Create the 'chatcmpl_object' following the structure of an OpenAI Chat Models API response
chatcmpl_object =  {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": created,
    "model": model_name,
    "choices": response['choices'],
    "usage": response['usage']
}

json_output = json.dumps(chatcmpl_object)
print(json_output)
# print(chatcmpl_object)
