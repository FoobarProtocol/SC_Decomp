import openai
import json


class Exploration():
    """
    This class serves as an AI-driven project manager, designed to distill complex dialogues into actionable project requirements. It utilizes the OpenAI GPT-4 API to perform its functions.
    The class is set up with an OpenAI API key and uses a predefined conversation template to gather the necessary project details. The dialogue will take the form of a system-user-assistant interaction.
    Once the conversation has concluded, the AI Project Manager will analyse the discourse in order to produce a comprehensive summary. The summary is structured around three critical aspects:
    1. Key Requirements: Identifying the essential needs and objectives as defined by the user.
    2. User Preferences: Understanding the user's preferences, including likes, dislikes, and subtle preferences that must be considered for successful project completion.
    3. Implementation Considerations: Listing the critical points that must be addressed during the project's technical implementation.
    Each aspect is presented as a bullet-point list to facilitate quick comprehension and future reference.
    """

    def __init__(self, OpenaiKey):
        # Initialize the AI Project Manager with the given OpenAI API key.
        # The initial conversation template is set up to prompt the assistant to readiness and
        # to set the context for its role as a project manager.
        self.client = openai.OpenAI(api_key=OpenaiKey)
        self.prompt = [
            {"role": "user", "content": "Are you ready?"},
            {"role": "assistant", "content": "Yes, I am always ready to assist you to the best of my abilities. Just let me know how I can help you."},
        ]
        self.context = """
        This class serves as an AI-powered assistant specializing in smart contract development, designed to extract and structure complex discussions into actionable project components. Built upon the OpenAI GPT-4 API, the system is tailored to provide in-depth guidance on Solidity programming concepts, best practices, and tools. It offers step-by-step instructions on writing, testing, debugging, and deploying smart contracts on the Ethereum blockchain, all while adapting to the unique requirements and objectives of the user.The system facilitates a dynamic interaction between the user and assistant to comprehensively analyze the discourse and generate a project summary. This summary is organized into three critical dimensions:
        1.	Key Requirements: Pinpointing the fundamental needs and objectives of the smart contract project.
        2.	User Preferences: Capturing the user's preferences, including specific technical approaches, stylistic choices, and developmental priorities.
        3.	Implementation Considerations: Highlighting vital aspects to address during the technical execution of the project, such as security, scalability, and optimization strategies.
        """

    def chatbot(self):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.prompt,
            temperature=0.7,
            max_tokens=6000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message

    def pre_design_view(self):
        self.prompt.append({
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": self.context
                }
            ]
        })
        return self.chatbot().content

    def add_user_message(self, message):
        """Add a user message to the conversation."""
        self.prompt.append({"role": "user", "content": message})
        return self.chatbot().content


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description='AI-powered Smart Contract Project Manager')
    parser.add_argument('--api_key', type=str, help='OpenAI API key', default=os.getenv('OPENAI_API_KEY'))
    parser.add_argument('--conversation_file', type=str, help='Path to conversation JSON file (optional)')
    parser.add_argument('--interactive', action='store_true', help='Enable interactive mode for direct input')
    parser.add_argument('--input', type=str, help='Direct input message to the model')
    args = parser.parse_args()

    if not args.api_key:
        print("Error: OpenAI API key is required. Either provide it with --api_key or set OPENAI_API_KEY environment variable.")
        exit(1)

    # Initialize the Exploration class
    explorer = Exploration(args.api_key)

    # If conversation file is provided, load it
    if args.conversation_file and os.path.exists(args.conversation_file):
        with open(args.conversation_file, 'r') as f:
            conversation = json.load(f)
            explorer.prompt.extend(conversation)

    if args.interactive:
        print("\nEntering interactive mode. Type 'exit' to quit.")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
            response = explorer.add_user_message(user_input)
            print("\nAssistant:", response)
    elif args.input:
        response = explorer.add_user_message(args.input)
        print("\nAssistant:", response)
    else:
        # Get the standard analysis
        result = explorer.pre_design_view()
        print("\nProject Analysis:")
        print("----------------")
        print(result)
