import sys

options =\
"""

USAGE:
    python main.py [<COMMAND>=<BOT-NAME>] [<OPTIONS>=<VALUE>]

COMMANDS:
    -r, --run      Run the specified bot
    -t, --train    Train the specified bot

BOT-NAME:
    cb, chatbot    The ChatBot model based on BOW deep learning Model.
    pb, predbot    The PredBot model based on a Voting Classifier.
    
OPTIONS:
    --time         If set to 1, outputs the time taken to load each file in a model.
    --data-dir     Used to specify the data directory for training the predbot model 

"""



if len(sys.argv) > 1:
    if list(sys.argv[1].split("="))[0] in ['-r', '--run']:
        try:
            file = list(sys.argv[1].split("="))[1]
        except IndexError:
            print(f"Enter the file option you want to run.\nEx: {sys.argv[1]}=cb or {sys.argv[1]}=pb")


        if file.lower() in ['cb', 'chatbot']:
            from ChatBot.chatbotMain import get_output

            print("How May I help you?")
            while True:
                inp = input("Input: ")
                if inp not in ['q', 'quit']:
                    outp = get_output(inp)
                    print('Output:', outp)

                else:
                    print("Quiting...")


        elif file.lower() in ['pb', 'predbot']:
            from PredBot.symptomInput import get_feature_input, get_features, related_symptoms
            from PredBot.modelFunction import pred_with_model, load_model

            model, labelEnc, diseases = load_model('main_py')

            print("Please enter the corresponding numbers for the symptoms that apply to you in the following 16 categories as asked (Ex: 1, 2, 5 if they apply to you or just Enter None if nothing applies to you)")
            while True:
                message = input("Input: ")
                bot_response, i = get_feature_input(message)

                if i >= len(related_symptoms) + 1:
                    features = get_features()
                    predictions = pred_with_model(features, model, labelEnc, diseases)

                    if len(predictions) == 1:
                        bot_response = f"\nYou most likely suffer from {predictions[0]}"
                    elif len(predictions) == 2:
                        bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
                    else:
                        bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {', '.join(predictions[1:-1])} or {predictions[-1]}"

                    print(bot_response)


                print(bot_response)

    elif list(sys.argv[1].split("="))[0] in ['-t', '--train']:
        try:
            file = list(sys.argv[1].split("="))[1]
        except IndexError:
            print(f"Enter the file option you want to run.\nEx: {sys.argv[1]}=cb or {sys.argv[1]}=pb")

        if file.lower() in ['cb', 'chatbot']:
            from ChatBot.chatbotTrain import train

            print("Training the chatbot...")
            train()
            

        elif file.lower() in ['pb', 'predbot']:
            from PredBot.finalModel import fitModel, modelDump

            print("Fitting the Model...")
            final_pipeline, labelEnc = fitModel()
            modelDump('main_py', final_pipeline, labelEnc)
            

else:
    print("This is the command line utility for MedBot."+options)
