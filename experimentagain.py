import tempfile
import subprocess
import os
import logging
from datetime import datetime
from mirascope.core import openai, prompt_template
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    filename="smart_contract_qa.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@openai.call("gpt-4o-mini")
# The `@prompt_template` decorator in the provided Python code snippet is used to define a template
# for generating prompts that will be used by the OpenAI GPT-4o-mini model. This specific prompt
# template is designed to extract all development-related requirements from the user's input prompt.
@prompt_template(
    """
    Extract all development-related requirements from the user's prompt.
    Include:
    - Specific coding tasks or features for the smart contract.
    - Required programming languages, tools, libraries, or frameworks.
    - Technical constraints or assumptions.
    - Any potential clarifications needed for implementation.

    User Prompt: {query}

    Comprehensive Smart Contract Development Requirements:
    """
)

# This function is designed to extract comprehensive requirements based on a given query.
# :param query: The `query` parameter in the `extract_comprehensive_requirements` function is a string
# that likely contains some kind of search query or input that will be used to extract comprehensive
# requirements
# :type query: str
def extract_comprehensive_requirements(query: str): ...

@openai.call("gpt-4o-mini")
@prompt_template(
    """
    Generate specific, practical questions about smart contract design choices based on the requirements.
    Each question should:
    - Target a single, concrete design decision
    - Request a specific format for the answer
    - Avoid open-ended or general programming questions
    - Focus on quantifiable parameters and explicit choices

    Examples of good questions:
    - "Specify the maximum number of concurrent lending positions per user (e.g., '5 positions')."
    - "State the liquidation threshold as a percentage of collateral value (e.g., '75%')."
    - "Define the exact cooldown period between withdrawals in blocks (e.g., '100 blocks')."

    Bad question examples to avoid:
    - "How do you want the withdrawal process to work?"
    - "What security features should we implement?"
    - "Describe the user journey for deposits."

    For ERC4626 vaults specifically, ensure to ask about:
    - Specific numerical parameters (min/max values, thresholds, limits)
    - Exact timing parameters (blocks, timestamps)
    - Discrete choices (yes/no, enumerated options)
    - Explicit event triggers
    - Precise asset configurations

    Separate questions with '---'.

    Smart Contract Requirements: {requirements}

    Design Parameters:
    """
)
def generate_comprehensive_questions(requirements: str): ...


@openai.call("gpt-4o-mini")
@prompt_template(
    """
    Based on the user's response to the smart contract development question,
    analyze the response type and provide appropriate guidance:

    1. If it's a direct answer: Evaluate its completeness for implementation
    2. If it's a clarification request: Provide detailed information about the topic
    3. If it's a counter-question: Give a comprehensive answer before repeating the original question

    Question: {question}
    User's Response: {response}

    Format:
    RESPONSE_TYPE: [DIRECT_ANSWER|CLARIFICATION_REQUEST|COUNTER_QUESTION]
    SUFFICIENT: [true/false] (only for DIRECT_ANSWER)
    EVALUATION: [detailed evaluation] (only for DIRECT_ANSWER)
    CLARIFICATION: [detailed explanation] (only for CLARIFICATION_REQUEST or COUNTER_QUESTION)
    REFINED_QUESTION: [refined version of question] (optional)
    """
)
def evaluate_comprehensive_response(question: str, response: str): ...


@openai.call("gpt-4o-mini")
@prompt_template(
    """
    Given a user's request for clarification about a smart contract feature or concept,
    provide a comprehensive explanation with examples and best practices.
    Include:
    - Common implementations and their tradeoffs
    - Industry standard approaches
    - Security considerations
    - Integration patterns
    - Relevant examples from popular protocols

    Topic: {topic}
    Specific Query: {query}

    Detailed Explanation:
    """
)
def generate_clarification_response(topic: str, query: str): ...


@openai.call("gpt-4o-mini")
@prompt_template(
    """
    Given a sufficient response about smart contract development, provide helpful
    context and insights that expand upon the user's answer. Include relevant
    examples, best practices, or implementation considerations.

    User's Response: {response}

    Additional Context:
    """
)
def generate_response_context(response: str): ...


def get_query_from_editor() -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
    try:
        subprocess.run(["nano", temp_file_path])
        with open(temp_file_path, "r") as file:
            query = file.read().strip()
    finally:
        os.remove(temp_file_path)
    return query


def ask_comprehensive_questions(questions_text, original_query):
    questions = [q.strip() for q in questions_text.split("---") if q.strip()]
    total_questions = len(questions)
    augmented_query = original_query

    for idx, question in enumerate(
        tqdm(questions, desc="Progress", unit="question"), start=1
    ):
        while True:
            # Log the current question
            logging.info(f"Question {idx}/{total_questions}: {question}")

            # Display the question clearly
            print(f"\nQuestion {idx}/{total_questions}:")
            print(question)
            print(f"\nYour response ({total_questions - idx} questions remaining):")

            response = input()
            logging.info(f"User response: {response}")

            # Evaluate the response in the background
            evaluation = evaluate_comprehensive_response(question, response)
            logging.info(f"Evaluation: {evaluation.content}")

            # Parse evaluation response
            eval_lines = evaluation.content.split("\n")
            response_type = next(
                (
                    line.replace("RESPONSE_TYPE:", "").strip()
                    for line in eval_lines
                    if line.startswith("RESPONSE_TYPE:")
                ),
                "DIRECT_ANSWER",
            )

            if (
                response_type == "CLARIFICATION_REQUEST"
                or response_type == "COUNTER_QUESTION"
            ):
                # Extract the clarification content
                clarification = next(
                    (
                        line.replace("CLARIFICATION:", "").strip()
                        for line in eval_lines
                        if line.startswith("CLARIFICATION:")
                    ),
                    "",
                )

                # Generate detailed explanation
                explanation = generate_clarification_response(
                    topic=question, query=response
                )

                # Display the clarification and explanation
                print("\nLet me help clarify that:")
                print(explanation.content)
                print(
                    "\nNow, with this context, could you please address the original question:"
                )
                print(question)
                logging.info(f"Provided clarification: {explanation.content}")
                continue

            # Handle direct answers
            is_sufficient = any(
                line.startswith("SUFFICIENT: true") for line in eval_lines
            )

            if is_sufficient:
                # Generate and display helpful context
                context = generate_response_context(response)
                print("\nHelpful Context:")
                print(context.content)

                augmented_query += (
                    f"\n\nComprehensive information for Question {idx}:\n{response}"
                )
                logging.info("Response accepted with additional context provided")
                break
            else:
                # Extract and display the refined question
                refined_question = next(
                    (
                        line.replace("REFINED_QUESTION:", "").strip()
                        for line in eval_lines
                        if line.startswith("REFINED_QUESTION:")
                    ),
                    None,
                )

                print(
                    "\nTo help you provide a more complete response, let me rephrase:"
                )
                print(refined_question if refined_question else question)
                logging.info(
                    f"Asked for clarification with refined question: {refined_question}"
                )

    return augmented_query


def main():
    original_query = get_query_from_editor()
    logging.info(f"Original query: {original_query}")

    response_requirements = extract_comprehensive_requirements(query=original_query)
    requirements = response_requirements.content
    logging.info(f"Extracted requirements: {requirements}")

    print("\nComprehensive Smart Contract Development Requirements:\n")
    print(requirements)

    response_questions = generate_comprehensive_questions(requirements=requirements)
    questions = response_questions.content
    logging.info(f"Generated questions: {questions}")

    final_query = ask_comprehensive_questions(questions, original_query)
    logging.info(f"Final augmented query: {final_query}")

    print("\nFinal comprehensive augmented prompt:\n")
    print(final_query)


if __name__ == "__main__":
    main()
