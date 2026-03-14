import os
from groq import Groq


api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def ask_llm(prompt):

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content
