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


# TODO: Define a function to add two numerical inputs and return the result.
# Keep the print statement within the function.
def add(x, y):
    print("Calling add function")
    return x + y


# TODO: Define a function to multiply two numerical inputs and return the result.
# Keep the print statement within the function.
def multiply(x, y):
    print("Calling multiply function")
    return x * y


def minus(x, y):
    print("Calling minus function")
    return x - y


# TODO: Create FunctionDeclarations for your functions
add_func = FunctionDeclaration(
    name="add",
    description="add two numerical inputs",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "x": {"type": "number", "description": "input numerical"},
            "y": {"type": "number", "description": "input numerical"}
        },
    },
)

multiply_func = FunctionDeclaration(
    name="multiply",
    description="multiply two numerical inputs",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "x": {"type": "number", "description": "input numerical"},
            "y": {"type": "number", "description": "input numerical"}
        },
    },
)

minus_func = FunctionDeclaration(
    name="minus",
    description="minus two numerical inputs",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "x": {"type": "number", "description": "input numerical"},
            "y": {"type": "number", "description": "input numerical"}
        },
    },
)

tool = Tool(
    function_declarations=[add_func, multiply_func],
)

system_instructions = """
    - Fulfill the user's instructions.
    - If asked to add or multiply numbers, call the provided functions.
    - You may call one function after the other if needed.
    - Repeat the result to the user.
"""


model = GenerativeModel(model_name="gemini-1.5-pro-001", system_instruction=system_instructions, tools=[tool])

chat = model.start_chat()


def handle_response(response):
    # If there is a function call then invoke it
    # Otherwise print the response.
    if response.candidates[0].function_calls:
        function_call = response.candidates[0].function_calls[0]
    else:
        print(response.text)
        return

    # TODO: Complete the following sections
    if function_call.name == "add":
        # the function_call requests your add function
        # Extract the arguments to use in your function
        # Call your function
        # Send the result back to the chat session with the model
        # Make a recursive call of this handler function

        result = add(function_call.args["x"], function_call.args["y"])
        new_response = chat.send_message(
            Part.from_function_response(
                name="add",
                response={
                    "content": {"result": result},
                },
            ),
        )
        handle_response(new_response)



    elif function_call.name == "multiply":
        result = multiply(function_call.args["x"], function_call.args["y"])
        new_response = chat.send_message(
            Part.from_function_response(
                name="multiply",
                response={
                    "content": {"result": result},
                },
            ),
        )
        handle_response(new_response)


    # the function_call requests your multiply function
    # Extract the arguments to use in your function
    # Call your function
    # Send the result back to the chat session with the model
    # Make a recursive call of this handler function
    # elif function_call.name == "minus":
    #     result = minus(function_call.args["x"], function_call.args["y"])
    #     new_response = chat.send_message(
    #         Part.from_function_response(
    #             name="minus",
    #             response={
    #                 "content": {"result": result},
    #             },
    #         ),
    #     )
    #     handle_response(new_response)
    else:
        # You shouldn't end up here
        print(function_call)
        print(response.text)


response = chat.send_message("Tell me a joke.")
handle_response(response)


response = chat.send_message("I have 7 pizzas each with 16 slices. How many slices do I have?")
handle_response(response)

response = chat.send_message("Doug brought 3 pizzas. Andrew brought 4 pizzas. How many pizzas did they bring together?")
handle_response(response)

response = chat.send_message("Doug brought 3 pizzas. Andrew brought 4 pizzas. There are 16 slices per pizza. How many slices are there?")
handle_response(response)

response = chat.send_message("Doug brought 4 pizzas, but Andrew dropped 2 on the ground. How many pizzas are left?")
handle_response(response)