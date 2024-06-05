
import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


def get_ai_response(user_message, content):
    print(os.getenv("gpt_token"))
    client = OpenAI(api_key=os.getenv("gpt_token"))
   
    completion = client.chat.completions.create(
        
        model= "gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": content},
                {"role": "user", "content": user_message}
        ]
    )
    
    
    ai_response = completion.choices[0].message
    
    return ai_response.content
