import sys

if len(sys.argv) >= 2:
    if sys.argv[1] in ['--run', '-r']:
        from AI_Model_Files.chatbotMain import get_output

        while True:
            inp = input("Input: ")

            if inp.lower() not in ['q', 'quit']:
                res = get_output(inp)
                print("Output:", res)
            else:
                print("Bye!")
                break

    elif sys.argv[1] in ['--train', '-t']:
        from AI_Model_Files.chatbotTrain import train
        import AI_Model_Files.modelFunction
        train()

else:
    print("This is an AI Powered Chatbot made in python. To chat with it, run 'python main.py -r' or run 'python main.py -t' to train it.")
