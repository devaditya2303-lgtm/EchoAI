import random

def load_knowledge():
    try:
        with open("src/data/knowledge.txt", "r") as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        return ["AstroAI is thinking silently in the stars 🌌"]

def astroai_response(user_input, knowledge):
    responses = [
        "Interesting… tell me more 🌙",
        "That sounds meaningful ⭐",
        "Hmm… the universe agrees 🌌",
        "I see wisdom in your words 🧠",
        "Old souls speak like this 😌"
    ]

    for line in knowledge:
        if user_input.lower() in line.lower():
            return line

    return random.choice(responses)

def main():
    print("🤖 AstroAI is awake.")
    print("Type 'exit' to close the universe.\n")

    knowledge = load_knowledge()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("AstroAI: Until we meet again among the stars ✨")
            break

        reply = astroai_response(user_input, knowledge)
        print("AstroAI:", reply)

if __name__ == "__main__":
    main()
