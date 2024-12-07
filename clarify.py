import openai
import os

OpenaiKey = os.getenv("OPENAI_API_KEY")


def program_Generate(prompt, num_candidates=1, max_tokens=3630, temperature=1):
    #    import openai

    # Set the API key once, assuming `OpenaiKey` is defined globally or passed securely.
    #    openai.api_key = OpenaiKey
    openai.api_key = OpenaiKey

    # Validate the max_tokens to avoid exceeding model limits.
    if max_tokens > 4096:  # Example limit for some GPT models; adjust as needed.
        raise ValueError("max_tokens exceeds model limit. Please adjust.")

    results = []
    try:
        # Make the ChatCompletion API call.
        response = openai.ChatCompletion.create(
            model="o1-preview",  # Ensure the model name is correct.
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            n=num_candidates,
        )
        # Parse responses.
        for choice in response.get("choices", []):
            text = choice.get("message", {}).get("content", "").strip()
            if text:
                print(text)  # Debug/console log
                results.append(text)  # Full response instead of truncation
        return results

    except openai.BadRequestError as e:
        print(f"Bad request error: {e}")
        return []
    except openai.APIError as e:
        print(f"API error: {e}")
        return []
    except openai.RateLimitError as e:
        print(f"Rate limit error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


question_prompt = """
Context: A user is interacting with a large language model designed to assist with smart contract development. This model provides comprehensive information on Solidity programming concepts, best practices, and tools. It offers step-by-step guidance on writing smart contracts, testing and debugging them, and deploying them on the Ethereum blockchain. The instructions and resources are tailored to the individual needs and goals of the user, ensuring a smooth transition into smart contract development.
Instruction: In order for a large language model to better complete tasks or generate outputs, the quality and accuracy of the outputs are profoundly influenced by the depth of understanding that the model achieves regarding the task. To ensure comprehensive understanding and to leave no stone unturned, it is imperative that the model engages in a continuous process of asking follow-up questions. This iterative approach is essential for capturing every single facet of the project, thereby enhancing the precision and relevance of the generated outputs.
The questions asked can be combined with the previously obtained (a) Key Requirements, (b)User Preference, and (c) Implementing Consideration to make users more clear about their needs.
{{User_Behaviour}}
The questions asked need to lead users to clarification of requirements and conform to strategies for interacting with LLM.

Functional requirement: I want to develop a smart contract for a decentralized marketplace.
Requirement guidance: You need to consider what goes into the contract design. For example, what functions are needed, what data structures to use, and what security measures to implement.
Answer: Implement functions for listing items, purchasing, and managing escrow with appropriate data structures.
Requirement guidance: You need to specify some conditions. For example, what happens in case of disputes or failed transactions.
Answer: Include dispute resolution mechanism with a 3-day waiting period and automated refund system for failed transactions.
Please give requirement guidance for the following functional requirement based on the above form.
"""

question_prompt2 = """
Context: A user is interacting with a large language model designed to assist with smart contract development. This model provides comprehensive information on Solidity programming concepts, best practices, and tools. It offers step-by-step guidance on writing smart contracts, testing and debugging them, and deploying them on the Ethereum blockchain. The instructions and resources are tailored to the individual needs and goals of the user, ensuring a smooth transition into smart contract development.
Instruction: In order for a large language model to better complete tasks or generate outputs, the quality and accuracy of the outputs are profoundly influenced by the depth of understanding that the model achieves regarding the task. To ensure comprehensive understanding and to leave no stone unturned, it is imperative that the model engages in a continuous process of asking follow-up questions. This iterative approach is essential for capturing every single facet of the project, thereby enhancing the precision and relevance of the generated outputs.
The questions asked can be combined with the previously obtained (a) Key Requirements, (b)User Preference, and (c) Implementing Consideration to make users more clear about their needs.
{{User_Behaviour}}
The questions asked need to lead users to clarification of requirements and conform to strategies for interacting with LLM.

Functional requirement: I want to develop a smart contract for an NFT minting platform.
Requirement guidance: You need to consider what goes into the contract design. For example, what token standard to use, how minting will work, and what royalty structure to implement.
Answer: Use ERC-721 standard with customizable metadata and configurable royalty settings.
Requirement guidance: You need to specify some conditions. For example, how to handle minting limits and pricing strategies.
Answer: Implement tiered minting with different price points, maximum supply cap of 10,000, and whitelist functionality for early access.
Please give requirement guidance for the following functional requirement based on the above form.
"""


def generate_query_expansion(
    behaviour, query, openai_key, question_prompt_template=None
):
    import openai
    from typing import Optional

    def validate_openai_key(key: str) -> bool:
        return bool(key and isinstance(key, str) and len(key.strip()) > 0)

    def safe_extract(response: Optional[list]) -> Optional[str]:
        if response and isinstance(response, list) and len(response) > 0:
            return response[0]
        return None

    if not validate_openai_key(openai_key):
        raise ValueError("Invalid OpenAI API key provided.")

    #    openai.api_key = openai_key
    openai.api_key = OpenaiKey

    question_prompt = (
        question_prompt_template
        or "Expand the following query based on user behavior and provide requirement guidance:\n"
    )

    question_prompt1 = f"{question_prompt}{query}\nRequirement guidance:"
    question_prompt1 = question_prompt1.replace("{{User_Behaviour}}", behaviour)

    try:
        expansion = program_Generate(
            prompt=question_prompt1, temperature=0.3, max_tokens=3800, num_candidates=1
        )
        expansion = safe_extract(expansion)
        if not expansion:
            return "No expansion generated.", ""

        if "Requirement guidance:" in query:
            functional_req_prompt = (
                f"{query}\nWrite the Functional requirement in detail according to the Requirement guidance and Answer above.\n"
                "Functional Requirement:"
            )
            expansion1 = program_Generate(
                prompt=functional_req_prompt,
                num_candidates=1,
                max_tokens=2500,
                temperature=0.3,
            )
            expansion1 = safe_extract(expansion1)
            if not expansion1:
                return expansion, ""
        else:
            expansion1 = query.replace("Functional requirement:", "").strip()

        return expansion, expansion1

    except openai.BadRequestError as e:
        print(f"Bad request error: {e}")
        return f"Error in query expansion: {e}", ""
    except openai.AuthenticationError as e:
        print(f"Authentication error: {e}")
        return "OpenAI API authentication failed.", ""
    except openai.APIConnectionError as e:
        print(f"API connection error: {e}")
        return "Could not connect to OpenAI API.", ""
    except openai.RateLimitError as e:
        print(f"Rate limit error: {e}")
        return "OpenAI API rate limit exceeded.", ""
    except openai.APIError as e:
        print(f"API error: {e}")
        return f"OpenAI API error: {e}", ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}", ""
