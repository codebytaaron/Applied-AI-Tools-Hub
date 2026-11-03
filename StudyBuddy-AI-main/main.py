import openai

openai.api_key = "YOUR_API_KEY_HERE"

SYSTEM_PROMPT = """
You are a helpful study buddy.
Explain topics simply.
Use clear language.
Help students memorize information.
"""

def ask_study_buddy(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message["content"]

def main():
    print("📚 StudyBuddy AI")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        answer = ask_study_buddy(question)
        print("\nStudyBuddy:", answer, "\n")

if __name__ == "__main__":
    main()
