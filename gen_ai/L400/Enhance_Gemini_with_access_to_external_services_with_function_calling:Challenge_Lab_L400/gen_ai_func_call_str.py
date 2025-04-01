import vertexai

PROJECT_ID = "data-sandbox-344301"
LOCATION = "us-central1" # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)

import requests
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)



# TODO: Define a function to reverse the order
# of a string and return the result.
# Keep the print statement within the function.

def reverse(s):
    result = s[::-1]
    print("Calling reverse function")
    return result


# TODO: Define a function to remove white space
# characters from a string and return the result.
# Keep the print statement within the function.

def remove_white_spaces(s):
    r = []
    for c in s:
        if c != " ":
            r.append(c)

    print("Calling remove_white_spaces function")
    return "".join(r)


# TODO: Create FunctionDeclarations for your functions

reverse_func = FunctionDeclaration(
    name="reverse",
    description="reverse the order of a string",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "s": {"type": "string", "description": "input string"}
        },
    },
)

remove_white_spaces_func = FunctionDeclaration(
    name="remove_white_spaces",
    description="remove white space characters from a string",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "s": {"type": "string", "description": "input string"}
        },
    },
)


tool = Tool(
    function_declarations=[reverse_func, remove_white_spaces_func],
)


system_instructions = """
    - Fulfill the user's instructions.
    - If asked to reverse a string or remove whitespace, call the provided functions.
    - You may call one function after the other if needed.
    - Repeat the result to the user.
"""


model = GenerativeModel(model_name="gemini-1.5-pro-001", system_instruction=system_instructions, tools=[tool])

chat = model.start_chat()


def handle_response(response):
    # If there is a function call then invoke it
    # Otherwise print the response.
    # print(response.candidates[0].function_calls)
    if response.candidates[0].function_calls:
        function_call = response.candidates[0].function_calls[0]
    else:
        print(response.text)
        return
    # print(function_call)
    if function_call.name == "reverse":
        result = reverse(function_call.args["s"])
        new_response = chat.send_message(
            Part.from_function_response(
                name="reverse",
                response={
                    "content": {"result": result},
                },
            ),
        )
        handle_response(new_response)


    # the function_call requests your reverse function
    # Extract the arguments to use in your function
    # Call your function
    # Send the result back to the chat session with the model
    # Recursive call

    elif function_call.name == "remove_white_spaces":
        result = remove_white_spaces(function_call.args["s"])

        new_response = chat.send_message(
            Part.from_function_response(
                name="remove_white_spaces",
                response={
                    "content": {"result": result},
                },
            ),
        )
        handle_response(new_response)
    # the function_call requests your remove_white_spaces function
    # Extract the arguments to use in your function
    # Call your function
    # Send the result back to the chat session with the model
    # Make a recursive call of this handler function

    else:
        # You shouldn't end up here
        print(function_call)
        print(function_call.name)
        print(response.text)