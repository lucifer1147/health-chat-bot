# **MedBot**: 
>***A Chatbot for medical assistance***



Medbot is an AI Powered ChatBot that can:
+ Provide you information on a specifiic Disease
+ Predict a disease based on the patient's symptom

It was created as a Project for a School Science Fest.


## About the Model:
The chatbot itself is an <abbr title='Artificial Neural Network'>ANN</abbr> based on the [BagOfWords Model](https://www.geeksforgeeks.org/bag-of-words-bow-model-in-nlp/).
The chatbot also implements a LogisticRegression Model which actually predicts the dieasease from the symptom. The chat bot mainly identifies 4 types of inputs:
- Illegible Inputs.
- Inputs asking about the chatbot itself or general messages.
- Inputs asking info about the specific disease.[^1]
- Inputs asking to predict a disease.

The chatbot then performs a specific action which is pretty self-explanatory.

### How to run it:
- Running it in a **Virtual Enviroment** is recommended.[^2]

- Make sure the modules in the `requirements.txt` are present on your machine. Run `pip install -r requirements.txt` just to be sure.

- To run the django server, run the command `python MedBot/manage.py runserver`[^3]

- To test the backend models, a main.py file has also be created in the MedBot directory which allows accesse to the AI Models from the command line.
 
  - USAGE:
        `python main.py [<COMMAND>=<BOT-NAME>] [<OPTIONS>=<VALUE>]`

  - COMMANDS:
      -r, --run      Run the specified bot
      -t, --train    Train the specified bot[^5]

  - BOT-NAME:
      cb, chatbot    The ChatBot model based on BOW deep learning Model.
      pb, predbot    The PredBot model based on a Voting Classifier.
    
  - OPTIONS:
      --time         If set to 1, outputs the time taken to load each file in a model.
      --data-dir     Used to specify the data directory for training the predbot model.[^5]

  
### Implementations:
The model can further be implemented as a chatbot on relevant medical sites. It can be of help to those who are not sure if they suffer from a specific disease or not and do not have the time/resources to contact a professional in case it's nothing. This chatbot can provide them with basic guidance and if they need to further consult an expert.

[^1]: The data for the diseases such as their symptoms, precautions, treatments etc. is taken from [Wikipedia](wikipedia.org)
[^2]: Python Virtual Environment is an isolated python installation made to be used specifically for select project(s). See [Python Venv](https://docs.python.org/3/library/venv.html) for further info.
[^3]: You can also specify the local-host address and port in the format of **address:port** in the run command to specify the host to run the local-server on. Ex `python MedBot/manage.py runserver 127.0.0.1:8000`
[^4]: Incase, you wish to train the chatbot */MedBot/ChatBot/jsons/intents.json* is the file you need to edit in order to customise responses. Keep the format as 'tag', 'patterns', 'respones'.
[^5]: This only needs to be specified when training the predbot. Note that the directory path should be absolute. If not specified, the default training file used is */MedBot/PredBot/datasets/Training.csv*
