# **MedBot**: 
>***A Chatbot for medical assistance***


\
Medbot is an AI Powered ChatBot that can:
+ Provide you information on a specifiic Disease
+ Predict a disease based on the patient's symptom

It was created as a Project for a School Science Fest.

### How to run it:
- Running it in a virtual environment is recommended.[^1]
- Make sure the modules in the `requirements.txt` are present on your machine. Run `pip install -r requirements.txt` just to be sure.


- To run the chatbot, run the command `python main.py -r --no-time` or `python main.py --run --no-time`
  - `-r` or `--run` run the actual chat loop
  - `--no-time` doesn't allow the module load time to be outputted
  

- To re-train the chatbot with custom intents, edit the intents.json[^2], and run the command `python main.py -t` or `python main.py --train`
  - `-t` runs the `train()` function in `chatbotTrain.py` which train the chatbot
  


[^1]: Python Virtual Environment is an isolated python installation made to be used specifically for select project(s). See [Python Venv](https://docs.python.org/3/library/venv.html) for further info.
[^2]: /AI_Model_Files/jsons/intents.json is the file you need to edit in order to customise responses. Keep the format as 'tag', 'patterns', 'respones'.
