import openai
import os


def program_Classifier(prompt, max_tokens=1024, stop=None, temperature=0):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = None
    while response is None:
        try:
            response = client.completions.create(
                model="got-4o-mini",
                prompt=prompt,
                max_tokens=max_tokens,
                stop=stop,
                temperature=temperature,
            )
        except Exception as e:
            print(type(e), e)
            if isinstance(e, openai.BadRequestError):
                response = "null"
    results = []
    for choice in response.choices:
        text = choice.text.strip()
        results.append(text)

    return results


# def gen_for_gpt3(input, query, OpenAIKey):
#     client = openai.OpenAI(api_key=OpenAIKey)
#     input_m = []
#     for put in input:
#         input_m.append(put[0])
#     input_mes = ", ".join(input_m)
#     prompt = (
#         "A user is interacting with a large language model. They are crafting prompts and giving them to the LLM in order to get the model to complete a task or generate output.\n\n"
#         + "Figure out what the intent of the following prompt is that the user submitted and suggest a better prompt for what they are trying to do. Use triangle brackets {{}} for templating parts of the prompt that could be substituted. The new prompt should be specific and detailed.\n\n"
#         + "PROMPT: Write a short feature description for a website Input: Website_Name\n"
#         + "NEW PROMPT: Write a short description of {{Website_Name}} to be used on its homepage. Focus on features such as pricing, user experience, customer suport, etc. Include a call-to-action linking to a signup page.\n\n"
#         + "PROMPT:"
#         + query.strip()
#         + " Input: "
#         + input_mes
#         + "\n"
#         + "NEW PROMPT:"
#     )
#     first = program_Classifier(prompt=prompt, max_tokens=2056, temperature=0.5)

#     second = program_Classifier(prompt=prompt, max_tokens=2056, temperature=0.7)

#     third = program_Classifier(prompt=prompt, max_tokens=2056, temperature=1)
#     result = [first[0], second[0], third[0]]
#     print("First: ", first[0])
#     print("Second: ", second[0])
#     print("Third: ", third[0])


#     return result
def gen_for_gpt3(input, query, OpenAIKey, max_tokens=512):
    """
    Generates three variations of a refined prompt using the LLM API.

    Parameters:
    - input: List of input variables for the prompt.
    - query: The original user-provided prompt.
    - OpenAIKey: API key for OpenAI.
    - max_tokens: Maximum token length for the output.

    Returns:
    - List of three generated prompts.
    """
    client = openai.OpenAI(api_key=OpenAIKey)
    input_m = [put[0] for put in input]
    input_mes = ", ".join(input_m)

    # Instructions for this function
    prompt = (
        "Users interact with a large language model (LLM) by creating specific prompts to receive better responses. "
        "Clear and precise wording is crucial, as it can significantly influence the quality of the model's replies. "
        "A well-defined prompt with context or examples typically yields better results, while vague prompts do not. "
        "This process is collaborative; users adjust their prompts based on the model's outputs to enhance its effectiveness for various tasks, "
        "emphasizing the link between human intent and machine-generated language. "
        "Figure out what the intent of the following prompt is that the user submitted and suggest a better prompt for what they are trying to do. "
        "Use triangle brackets {{}} for templating parts of the prompt that could be substituted. "
        "The new prompt should be specific and detailed.\n\n"
        f"PROMPT: {query.strip()} Input: {input_mes}\n\nNEW PROMPT:"
    )

    # Parameter configurations for diversity
    configs = [
        {"temperature": 0.5, "top_p": 0.8, "frequency_penalty": 0.1, "top_k": 40},
        {"temperature": 0.7, "top_p": 0.9, "frequency_penalty": 0.2, "top_k": 60},
        {"temperature": 1.0, "top_p": 1.0, "frequency_penalty": 0.3, "top_k": 80},
    ]

    results = []

    for config in configs:
        response = None
        while response is None:
            try:
                response = client.completions.create(
                    model="got-4o-mini",
                    prompt=prompt,
                    max_tokens=max_tokens,
                    stop=None,
                    temperature=config["temperature"],
                    top_p=config["top_p"],
                    frequency_penalty=config["frequency_penalty"],
                    presence_penalty=config["top_k"] / 100.0,  # Normalize top_k
                )
            except Exception as e:
                print(type(e), e)
                if isinstance(e, openai.BadRequestError):
                    response = "null"

        for choice in response.choices:
            results.append(choice.text.strip())

    return results


def amalgamate_prompts(prompts, original_prompt, OpenAIKey, max_tokens=512):
    """
    Combines three prompts into a fourth, improved prompt using the LLM API.

    Parameters:
    - prompts: List of three generated prompts.
    - original_prompt: The user's original input prompt.
    - OpenAIKey: API key for OpenAI.
    - max_tokens: Maximum token length for the output.

    Returns:
    - str: The synthesized fourth prompt.
    """
    client = openai.OpenAI(api_key=OpenAIKey)

    # Instructions for this function
    meta_prompt = (
        "You are a highly advanced AI tasked with synthesizing a better prompt by combining the strengths of multiple inputs. "
        "You should prioritize clarity and creativity, merging the strengths of each version without losing focus on the user's original intent. "
        "As an expert in prompt crafting, you are able to craft prompts that are both comprehensive and engaging, "
        "capturing the essence of the task at hand in the most effective way possible. "
        "Below are three prompts. You are tasked with creating a final, refined prompt by evaluating three separate prompts "
        "that have been generated based on an original user input. Your job is to synthesize the best elements of all three prompts "
        "into a cohesive and optimized version. This involves extracting the most relevant, insightful, and impactful details "
        "from each prompt, while ensuring the final result is clear, actionable, and well-balanced. "
        "The final prompt should feel like the best possible synthesis, combining the key insights and ideas from all three, "
        "while maintaining a high level of coherence and relevance.\n\n"
        f"ORIGINAL USER PROMPT: {original_prompt}\n\n"
        f"PROMPT 1: {prompts[0]}\n\n"
        f"PROMPT 2: {prompts[1]}\n\n"
        f"PROMPT 3: {prompts[2]}\n\n"
        "SYNTHESIZED PROMPT:"
    )

    try:
        response = client.completions.create(
            model="o1-preview",  # Use a distinct model for synthesis
            prompt=meta_prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
        )
        synthesized_prompt = response.choices[0].text.strip()

        return synthesized_prompt

    except Exception as e:
        print(f"Error during amalgamation: {e}")
        return None


# query = "According to the number of questions entered, generate math homework based on the math problem. "
# first, second, thrid = gen_for_gpt3(["Number"], query)
