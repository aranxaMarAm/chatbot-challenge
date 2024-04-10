from flask import Flask, request
import requests
import json
import logging
from flask_cors import CORS, cross_origin
from abc import ABC, abstractmethod
import os
from typing import Dict, List
from datetime import datetime

class Chatbot(ABC):

    def __init__(self):

        self.rasa_nlu_url = "http://localhost:5005/model/parse"
        if os.getenv("RASA_NLU_URL") is not None:
            self.rasa_nlu_url = os.getenv("RASA_NLU_URL")

        self.logdir = "logs"
        if os.getenv("LOG_DIR") is not None:
            self.logdir = os.getenv("LOG_DIR")
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

        self.logfile = None
        self.last_logging_info = None

    # call rasa nlu
    def nlu(self, user_message : str):
        try:
            data = {"text": user_message}
            response = requests.post(self.rasa_nlu_url, json = data)
            nlu_response = response.json()
            intent = nlu_response["intent"]
            return intent, nlu_response
        except Exception as e:
            logging.error("There was a problem connecting to RASA NLU server")
            logging.exception(e)

    # call nlu, generate prompt and call the llm
    def get_answer(self, messages : List[Dict], session_id : str, llm_parameter : Dict, chatbot_id : str):
        intent, nlu_response = self.nlu(messages[-1]["message"])
        prompt = self.get_prompt(messages, intent, session_id)
        logging_info = {
            "messages": messages,
            "session_id": session_id,
            "llm_parameters": llm_parameter,
            "nlu_response": nlu_response,
            "prompt": prompt,
            "time": datetime.now().isoformat()
        }
        return self.call_llm(prompt, llm_parameter, logging_info, chatbot_id)

    # construct a theater script dialog from the list of messages
    def build_dialog(self, messages : List[Dict]) -> str:
        dlg = []
        for message in messages:
            msg = message["sender"] + ": " + message["message"]
            msg = msg.strip()
            dlg.append(msg)
        dlg.append(messages[0]["sender"] + ": ")
        return "\n".join(dlg)
    
    @abstractmethod
    def get_prompt(self, messages, intent, session_id):
        pass

    def write_to_logfile(self, log_str : str, chatbot_id : str):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        if self.logfile is None:
            self.logfile = open(f"{self.logdir}/chat_log.text", "a")
        self.logfile.write(log_str)
        self.logfile.flush()

    def call_llm(self, prompt : str, llm_parameter : Dict, logging_info : Dict, chatbot_id : str):
        url = f"https://dfki-3108.dfki.de/mistral-api/generate_stream"
        data = {
            "inputs": prompt,
            "parameters": llm_parameter
        }

        # connect to the llm api
        # read response stream
        # parse the llm answer from the stream for logging
        # also pass the stream to the frontend
        # the function stops the output stream at the first \n.
        def generate():
            try:
                http_user = "mistral"
                http_password = "aaRePuumL6JL"
                session = requests.Session()
                session.auth = (http_user, http_password)
                response = session.post(url, stream = True, json=data)
            except Exception as e:
                logging.error("There was a problem connecting to the LLM server.")
                logging.exception(e)

            running_text = []
            
            stop = False
            for chunk in response.iter_content(chunk_size = None):
                if stop:
                    break
                chunk_utf8 = chunk.decode("utf-8")[5:]
                for line in chunk_utf8.split("\n"):
                    if len(line.strip()) == 0:
                        continue
                    try:
                        jsono = json.loads(line)
                        next_str = jsono["token"]["text"]
                        if next_str == "\n" and len(running_text) > 0:
                            stop = True
                        running_text.append(next_str)
                    except Exception as e:
                        logging.exception(e)
                        pass
                yield chunk

            # write chatlog
            running_text = "".join(running_text)
            logging_info["llm_response"] = running_text
            logging_info_str = json.dumps(logging_info) + "\n"
            self.write_to_logfile(logging_info_str, chatbot_id)
            self.last_logging_info = logging_info

        return generate()

# helper function that reads the streaming response from the llm and converts it to a single string.
def llm_stream_to_str(generator):
    response = []
    for o in generator:
        s = o.decode("utf-8")[5:]
        try:
            jsono = json.loads(s)
            response.append(jsono["token"]["text"])
        except Exception as e:
            pass
    return "".join(response)

