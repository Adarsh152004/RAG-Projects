from chatbot import chat
from prompts import PROMPTS
from chatbot import start_chat

print("=" * 40)
print("🚀 Welcome to My Python Application!")
print("=" * 40)

print("\nChoose a Prompt\n")

print(
    """
    0
    1. Assistant
    2. Python
    3. Story
    4. Translator
    5. Java
    6. Marketing
    7. Agent
    8. Q&A
    9. Summarizer
    10. Chatbot
    11. Tutor
    12. Lawyer
    13. Doctor
    14. Engineer
    15. Scientist
    16. Artist
    17. Musician
    18. Writer
    """
)

choice = input("\nChoice: ")

system_prompt = PROMPTS.get(choice, PROMPTS["Assistant"])

start_chat(system_prompt)

while True:
    print('\n')
    user_input = input('You: ')
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: GoodBye!😶❤️")
        break

    print('\n')
    print('Bot: ', end='')
    chat(user_input)
