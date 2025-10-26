import time
from ml.predict_difficulty import predict_next_level
import random  # for generating fake answers for now
import pandas as pd

def handle_conversation():
    context = ""
    current_difficulty = 2
    user_data = []

    print("Welcome to the AI Math Tutor! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        start_time = time.time()

        # TEMP: Generate a dummy AI response
        result = f"AI thinks about: {user_input} 🤖"

        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        print(f"Bot: {result}")
        print(f"(Response time: {response_time}s)")

        # TEMP: Ask user for performance metrics manually
        accuracy = float(input("Enter accuracy (1=correct, 0=wrong): "))
        hints_used = int(input("Enter number of hints used: "))

        # Predict next difficulty using ML model
        next_diff = predict_next_level(response_time, accuracy, hints_used, current_difficulty)
        print(f"📊 Next recommended difficulty: {next_diff}\n")

        # Feedback
        if accuracy < 0.5:
            print("Feedback: Revise this topic again. 🔁")
        elif hints_used > 2:
            print("Feedback: Try using fewer hints next time. 💡")
        elif next_diff > current_difficulty:
            print("Feedback: Great! Let’s try a slightly harder question. 💪")
        else:
            print("Feedback: Keep practicing! 📈")

        # Save user session data
        user_data.append({
            "response_time": response_time,
            "accuracy": accuracy,
            "hints_used": hints_used,
            "current_difficulty": current_difficulty,
            "next_difficulty": next_diff
        })

        current_difficulty = next_diff
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save session data to CSV
    if user_data:
        df = pd.DataFrame(user_data)
        df.to_csv("data/user_learning_data.csv", mode='a', index=False, header=False)
        print("✅ Your session data has been saved.")

if __name__ == "__main__":
    handle_conversation()
