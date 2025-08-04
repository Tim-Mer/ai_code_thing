import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import *
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *

# Setting verbosity
verbose = False
if "--verbose" in sys.argv:
    verbose = True
# Checking if prompt given   
if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
else:
    print("Error: No input given")
    exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# Creating a list of messages that will be sent to the AI, initially it is just the users input message
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

model_name='gemini-2.0-flash-001'

# List of functions available to the model to use and execute
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
i = 0
text = ""
while i < 20:
    # Get a response from the AI, the system_prompt is a string that describes how the AI should act
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )
    except Exception as e:
        print(f"Error: Failed with error message: {e}")
        exit(1)

    if not response.function_calls:
        i += 20
        text = response.text
    
    try:
        for candidate in response.candidates:
            messages.append(candidate.content)
    except:
        print(f"Error: Failed during candidate response adding")

    try: 
    # If the AI decides it wants to run one of the available functions
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if function_call_result.parts[0].function_response.response:
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("Error missing response")
                #print(f"\nCalling function: {function_call_part.name}({function_call_part.args})")
                messages.append(
                    types.Content(role="tool", parts=[types.Part(function_response=function_call_result.parts[0].function_response)])
                )
    except Exception as e:
        print(f"Error: Failed during function calling with error: {e}")
        
    i += 1

print(text)



if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")