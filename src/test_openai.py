# src/test_openai.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_connection():
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Try a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'The elves are working!'"}
            ]
        )
        
        # Print the response
        print("OpenAI Response:", response.choices[0].message.content)
        print("\nConnection test successful! Your API key is working.")
        
    except Exception as e:
        print("Error testing OpenAI connection:")
        print(e)

if __name__ == "__main__":
    test_openai_connection()