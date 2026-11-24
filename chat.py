from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client()

print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=question,
        )
        print("Bot:", response.text, "\n")
    except errors.ServerError:
        print("Bot: The model is busy right now. Please try again in a moment.\n")