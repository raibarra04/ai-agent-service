import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function

def main():
    load_dotenv()
    args = sys.argv[1:]
    verbose = False
    agent_response = ''

    if not args:
        print("Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
            )

    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            current_fn_call = call_function(function_call, verbose)
        
            if not current_fn_call.parts[0].function_response.response:
                raise ValueError('Error: retrieving response from called function')
        
            if verbose:
                print(f"-> {current_fn_call.parts[0].function_response.response}")

            agent_response += current_fn_call.parts[0].function_response.response["result"]
    else:
        agent_response += response.text

    print(agent_response)
    return 0



if __name__ == "__main__":
    main()
