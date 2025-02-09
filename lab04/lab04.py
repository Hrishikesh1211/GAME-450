from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import TemplateChat

def run_console_chat(sign, **kwargs):
    chat = TemplateChat.from_file(sign=sign, **kwargs)
    chat_generator = chat.start_chat()
    print(next(chat_generator))
    while True:
        try:
            message = chat_generator.send(input('You: '))
            print('Agent:', message)
        except StopIteration as e:
            if isinstance(e.value, tuple):
                print('Agent:', e.value[0])
                ending_match = e.value[1]
                print('Ending match:', ending_match)
            break

lab04_params = {
    "template_file": "lab04/lab04_trader_chat.json",
    "sign": "Hrishikesh",
    "end_regex": ".*successfully.*"
}

if __name__ ==  '__main__':
    # run lab04.py to test your template interactively
    chat = TemplateChat.from_file(sign=lab04_params["sign"], template_file=lab04_params["template_file"])
    
    generate_chat = chat.start_chat()
    print("---------------- Trade Conversation -----------------")
    
    try:
        print(next(generate_chat))  # Display the initial system message
        while True:
            user_input = input("You (Adventurer): ")  # User provides an offer
            
            if user_input in ["exit"]:
                print("Exiting conversation...")
                break
            
            trader_response = generate_chat.send(user_input)  # Trader responds
            print("Trader:", trader_response)
    except StopIteration as e:
        print("Trader:", e.value[0])
        ending_match = e.value[1]  # Store trade result
        print("Ending match:", ending_match)