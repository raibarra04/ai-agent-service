import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import call_function, available_functions

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    args = []
    agent_response = ''
    
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):
        try:
            response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=available_functions, system_instruction=system_prompt),
                    )

            if (len(response.candidates) > 0):      
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            
            if response.function_calls:
                function_responses = []
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                
                    if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                        raise Exception("empty function call result")
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                
                    function_responses.append(function_call_result.parts[0])

                if not function_responses:
                    raise Exception("no function responses generated, exiting.")
                messages.append(types.Content(role="user", parts=function_responses))

            else:
                if response.text:
                    print(response.text)
                    break
                
        except Exception as e:
            print(f"Error: something happened: {e}")


if __name__ == "__main__":
    main()
