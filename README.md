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


- To run the chatbot, run the command `python main.py -r --no-time` or `python main.py --run --no-time`
  - `-r` or `--run` run the actual chat loop
  - `--no-time` doesn't allow the module load time to be outputted
  

- To re-train the chatbot with custom intents, edit the intents.json[^3], and run the command `python main.py -t` or `python main.py --train`
  - `-t` runs the `train()` function in `chatbotTrain.py` which train the chatbot
  
### Implementations:
The model can further be implemented as a chatbot on relevant medical sites. It can be of help to those who are not sure if they suffer from a specific disease or not and do not have the time/resources to contact a professional in case it's nothing. This chatbot can provide them with basic guidance and if they need to further consult an expert.

[^1]: The data for the diseases such as their symptoms, precautions, treatments etc. is taken from [Wikipedia](wikipedia.org)
[^2]: Python Virtual Environment is an isolated python installation made to be used specifically for select project(s). See [Python Venv](https://docs.python.org/3/library/venv.html) for further info.
[^3]: /AI_Model_Files/jsons/intents.json is the file you need to edit in order to customise responses. Keep the format as 'tag', 'patterns', 'respones'.
