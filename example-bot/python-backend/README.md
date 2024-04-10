# Dynamic Prompting - Python Backend

This repository contains the dynamic prompting backend. The important files and directories are:

* examples: Contains example CURL requests how to interact with the API
* logs: Contains detailed logs about the conversation. What did the users say, what did the NLU detect, ...
* chat_server.py: This is the entry point of the application. It starts a Flask HTTP server
* chatbot_implementation: This is the file in which you will implement your bot.
* chatbot.py: This implements the dynamic prompting backend. It creates an abstract class "Chatbot" from which you derive the chatbot_implementation.

Run it:

```
python chat_server.py
```