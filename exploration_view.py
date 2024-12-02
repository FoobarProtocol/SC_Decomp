import openai
import json


class Exploration():
    """
    This class serves as an AI-driven Project Manager, designed to distill complex dialogues into
    actionable project requirements. It leverages OpenAI's GPT-4 API to perform its tasks.
    The class is initialized with an OpenAI API key and employs a predefined conversation template
    to elicit essential project details. The conversation will involve a system-user-assistant dialog.
    Following the conversation, the AI Project Manager analyzes the discourse to formulate a
    comprehensive summary. This summary is structured under three critical aspects:
    1. Key Requirements: Pinpointing the fundamental needs and goals as articulated by the user.
    2. User Preferences: Deciphering likes, dislikes, and nuanced preferences that must be adhered
       to for successful project execution.
    3. Implementation Considerations: Enumerating vital points that must be considered during
       the project's technical implementation.
    Each aspect is presented as a bullet-point list to facilitate quick comprehension and future reference.
    """

    def __init__(self, OpenaiKey):
        # Initialize the AI Project Manager with the given OpenAI API key.
        # The initial conversation template is set up to prompt the assistant to readiness and
        # to set the context for its role as a project manager.
        openai.api_key = OpenaiKey
        self.prompt = [
            {"role": "system", "content": "Are you ready?"},
            {"role": "assistant", "content": "Yes, I am always ready to assist you to the best of my abilities. Just let me know how I can help you."},
        ]
        self.context = """
        I would like you to act as a project manager. I have given you the conversation between user and assistant.
        According to the conversation above, please summarize the key information.
        You can only refer to the given conversation but not add extra information.
        Do not pay too much attention to what the user is trying the system, but have high level abstraction for system design.
        You should summarize it from three aspects:
        1. Illustrate the key requirements of the user?
        2. Desctibe the user's preference? For example, what the user like and what the user dislike. What should you have to do to satisfy the user's requirement and what you have not to do.
        3. List the points that you have to pay attention to when implementing the system exlicitly.
        You have to output the three aspects in the form of 1. Key Requirements:, 2. User Preference:, 3. Implementing Consideration:.You are expected to bullet list the key points for each aspects.
        """

    def chatbot(self):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.prompt
        )
        return response["choices"][0]["message"]

    def pre_design_view(self):
        self.prompt = self.prompt + [
            {"role": "system", "content": self.context},
        ]
        # Summarize conversation and extract user requirements
        return self.chatbot()["content"]
