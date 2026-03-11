import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("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"))


def ask_llm(prompt):

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )


    return completion.choices[0].message.content
