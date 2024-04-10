"""
You can use this helper script to call your chatbot directly from python
to test and develop it without the api.
"""

import json

from chatbot import llm_stream_to_str
from chatbot_implementation import ChatbotImplementation

if __name__ == "__main__":

    chatbot = ChatbotImplementation()

    input_data = json.load(open("examples/request.json"))

    answer = chatbot.get_answer(
        input_data["messages"],
        input_data["session_id"],
        input_data["llm_parameters"],
        input_data["chatbot"],
    )

    answer = llm_stream_to_str(answer)

    print(answer)
    print(json.dumps(chatbot.last_logging_info, indent=4))
    