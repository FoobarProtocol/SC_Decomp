import time
import openai
import argparse

from openai import OpenAI

client = OpenAI()

def gpt3(prompt, t, max_tokens):
    try:
        response = client.chat.completions.create(
            model="o1-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            response_format={
                "type": "text"
            },
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(type(e), e)
        time.sleep(3)

    # except Exception as e:
    #     print(type(e), e)
    #     time.sleep(3)

decompose_template = """You are tasked with implementing an advanced cognitive framework known as 'task decomposition' to analyze and break down complex user prompts. This methodology, rooted in cognitive psychology and artificial intelligence, involves systematically dissecting intricate tasks into a series of more manageable, atomic subtasks. Each subtask represents a discrete, self-contained unit of the overarching objective, designed to be processed independently by a Large Language Model (LLM).

The art of task decomposition traces its origins to the early days of computer science and artificial intelligence, with seminal works by Herbert A. Simon and Allen Newell in the 1950s and 1960s. Their research on problem-solving and information processing laid the groundwork for modern approaches to task analysis and decomposition. Today, this technique has evolved to become a cornerstone of various fields, including software engineering, project management, and cognitive load theory in education.

When applying task decomposition to LLM interactions, we aim to mirror the intricacies of human cognitive processes. This involves mapping out both the data flow - the journey and transformation of information through the system - and the control flow - the logical sequence and conditional execution of subtasks. By doing so, we create a framework that not only guides the LLM but also reflects the nuanced, non-linear nature of human thought and problem-solving.

The decomposed subtasks are meticulously crafted to interact with the LLM in a manner that emulates the depth and breadth of human cognition. This includes:

1. Sequential Processing: Mimicking the step-by-step approach often employed in human problem-solving.
2. Parallel Processing: Allowing for simultaneous consideration of multiple aspects, similar to how the human brain can process various information streams concurrently.
3. Iterative Refinement: Incorporating feedback loops that enable the LLM to revisit and refine earlier outputs based on subsequent insights.
4. Contextual Adaptation: Ensuring that each subtask is sensitive to the broader context established by preceding subtasks and the overall objective.

By decomposing tasks in this sophisticated manner, we unlock several critical advantages:

1. Enhanced LLM Guidance: We provide a clear, structured pathway for the LLM to navigate complex problems, significantly improving its ability to generate accurate, relevant, and contextually appropriate outputs.
2. Improved Task Comprehension: Breaking down the task allows the LLM to grasp nuanced requirements more effectively, reducing the likelihood of misinterpretation or oversight.
3. Granular Control and Monitoring: Each subtask becomes a discrete checkpoint, allowing for precise monitoring, adjustment, and optimization of the overall process.
4. Scalability and Flexibility: The modular nature of decomposed tasks facilitates easy scaling to more complex problems and adaptation to diverse domains.
5. Error Isolation and Debugging: By compartmentalizing the task, we can more easily identify and rectify issues within specific subtasks without disrupting the entire process.
6. Cognitive Load Management: For human operators or reviewers, the decomposed structure makes it easier to understand, manage, and refine the LLM's approach to complex tasks.

Looking to the future, task decomposition in LLM interactions is poised to play a pivotal role in advancing artificial general intelligence (AGI). As LLMs become more sophisticated, the ability to break down and tackle increasingly complex, multi-faceted problems will be crucial. This methodology may serve as a bridge between current narrow AI capabilities and the more generalized problem-solving abilities associated with AGI.

Moreover, the principles of task decomposition in LLM interactions are likely to influence the development of more transparent and explainable AI systems. By providing a clear, step-by-step breakdown of how an LLM approaches a problem, we open up new avenues for understanding and auditing AI decision-making processes, addressing critical concerns about AI transparency and accountability.

In conclusion, as you embark on decomposing the given prompt, remember that you are not merely breaking down a task; you are engaging in a sophisticated cognitive exercise that pushes the boundaries of human-AI interaction. Your decomposition should reflect the depth, nuance, and interconnectedness of human thought, while leveraging the unique strengths of LLM processing to achieve outcomes that may surpass human capabilities in certain domains.

<Task Description>
{description}
</Task Description>

<Decomposed Subtasks>
{subtasks}
</Decomposed Subtasks>
"""

def decompose(description):
    prompt = decompose_template.format(
        description=description,
        subtasks=""
    )
    return gpt3(prompt, 0.7, 3000)

# Example usage
query = "Create a Solidity smart contract for a decentralized lending and borrowing platform with dynamic interest rates, collateral management, and owner-restricted functions."
print(decompose(query))

decompose_template1 = """<Requirement Description>
Create a Solidity smart contract for a decentralized lending and borrowing platform. Allow users to lend tokens and earn interest, implementing a dynamic interest rate based on supply and demand. Allow users to borrow tokens by providing collateral, ensuring proper management of collateral and liquidation in case of default. Include functions to manage interest rates and platform parameters, restricted to the contract owner.
</Requirement Description>

<Decomposed steps>
To achieve a decentralized lending and borrowing platform via a Solidity smart contract, follow these steps:

(Step1 Input: None Output: Token_Contract_Design)
Design the token contract structure, ensuring compatibility with ERC-20 standards for token interactions. Define the token supply, initial distribution, and basic token operations. Incorporate mechanisms for token minting and burning, enabling scalability and deflationary features. Provide detailed documentation on token lifecycle events and how they interact with the financial operations of the platform.

(Step2 Input: Token_Contract_Design Output: Lending_Functionality_Design)
Design the lending functionality, specifying how users can lend tokens and earn interest. Determine parameters for dynamic interest rates based on supply and demand, incorporating real-time data feeds for accurate rate adjustments. Include mechanisms for automatic interest calculations and compounding, enhancing user returns. Elaborate on the risk assessment protocols for lending, ensuring sustainable and secure operations.

(Step3 Input: Lending_Functionality_Design Output: Borrowing_Functionality_Design)
Design the borrowing functionality, detailing how users can borrow tokens by providing collateral. Include logic for collateral valuation and liquidation processes, with real-time monitoring of market prices. Develop an interface for users to manage their collateral, offering insights into their borrowing power and risk exposure. Explain how the platform ensures fair liquidation practices, protecting both borrowers and lenders.

(Step4 Input: Borrowing_Functionality_Design Output: Interest_Rate_Management)
Implement functions to manage interest rates and platform parameters, ensuring these operations are restricted to the contract owner for security and flexibility. Incorporate a governance mechanism allowing token holders to propose and vote on interest rate changes. Detail the algorithms used to calculate interest rates, providing transparency and predictability for users. Document the impact of rate changes on the economic model of the platform.

(Step5 Input: Interest_Rate_Management Output: Collateral_Management)
Implement collateral management, including adding, removing, and valuing collateral. Ensure proper handling of collateral liquidation in case of borrower default, with automated notifications to affected parties. Integrate third-party oracles for accurate collateral valuation, minimizing discrepancies. Describe the process for updating collateral management policies in response to market shifts.

(Step6 Input: Collateral_Management Output: Smart_Contract_Deployment)
Deploy the smart contract on a blockchain network, ensuring the deployment is secure and the contract is functional for users to interact with. Provide a step-by-step guide for deployment, including environment setup and verification of contract parameters. Implement a fallback mechanism for rollback in case of deployment issues. Outline the security measures employed to protect the contract from vulnerabilities.

(Step7 Input: Smart_Contract_Deployment Output: Security_Audit)
Conduct a security audit of the smart contract to identify and fix potential vulnerabilities. Verify the correctness and efficiency of the contract code, using automated tools and manual review. Engage external auditors to provide an unbiased assessment of the security posture of the contract. Document the audit process and findings, ensuring transparency and trust with users.

(Step8 Input: Security_Audit Output: User_Interface_Design)
Design a user interface for interaction with the smart contract, allowing users to lend, borrow, and manage their assets seamlessly. Focus on user experience, ensuring intuitive navigation and accessibility across devices. Include real-time data visualization tools for users to monitor their financial activities and performance. Provide comprehensive support and help documentation to assist users in navigating the platform.

</Decomposed steps>

<Requirement Description>
{{Description}}
</Requirement Description>

<Decomposed steps>
"""

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

query = "Create a Solidity smart contract for a DAO that uses a governance token to manage proposals and voting. Implement an ERC20-compliant governance token that allows token holders to vote on proposals. Include functions to create, vote on, and execute proposals, ensuring that proposals require a minimum quorum and majority vote to pass. Implement delegated voting, allowing token holders to delegate their voting power to others. Introduce a time-lock mechanism where proposals can only be executed after a certain period."
query1 = "Create a Solidity smart contract for a decentralized insurance platform. Allow users to create and purchase insurance policies. Implement a mechanism to collect and manage premiums, including functions for users to submit and verify claims. Automate the payout process for approved claims, managing a risk pool to ensure sufficient funds for payouts."
# this code will print the decomposed prompt for us
print(decompose(query))
pat = {"content": "How are you", "input": ["history", "chatbot"],"prompt":["prompt1","prompt2"] ,"output": "human", "model": "LLM"}
