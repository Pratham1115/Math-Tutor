from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from ml.predict_difficulty import predict_next_level  # ML function
import time
import pandas as pd  # For logging user performance

# Chat prompt template
template = """ 
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Initialize chatbot model
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    current_difficulty = 2  # start with medium difficulty
    user_data = []           # Temporary list to store session data

    print("Welcome to the AI Math Tutor! Type 'exit' to quit.\n")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Start timer for response time
        start_time = time.time()
        result = chain.invoke({"context": context, "question": user_input})
        end_time = time.time()

        response_time = round(end_time - start_time, 2)
        print(f"Bot: {result}")
        print(f"(Response time: {response_time}s)")

        # Ask user for performance metrics (later can be automated)
        accuracy = float(input("Enter accuracy (1 = correct, 0 = wrong): "))
        hints_used = int(input("Enter number of hints used: "))

        # Predict next difficulty using ML model
        next_diff = predict_next_level(response_time, accuracy, hints_used, current_difficulty)
        print(f"📊 Next recommended difficulty: {next_diff}\n")

        # Give personalized feedback
        if accuracy < 0.5:
            print("Feedback: Try revising this topic again. 🔁")
        elif hints_used > 2:
            print("Feedback: Try using fewer hints next time. 💡")
        elif next_diff > current_difficulty:
            print("Feedback: Great! Let’s try a slightly harder question. 💪")
        else:
            print("Feedback: Keep practicing! You’re doing well. 📈")

        # Update current difficulty for next question
        current_difficulty = next_diff

        # Append this question’s data to session log
        user_data.append({
            "response_time": response_time,
            "accuracy": accuracy,
            "hints_used": hints_used,
            "current_difficulty": current_difficulty,
            "next_difficulty": next_diff
        })

        # Update conversation history
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save session data when user exits
    if user_data:
        df = pd.DataFrame(user_data)
        df.to_csv("data/user_learning_data.csv", mode='a', index=False, header=False)
        print("✅ Your session data has been saved.")

if __name__ == "__main__":
    handle_conversation()
