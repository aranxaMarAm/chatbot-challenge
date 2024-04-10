Example request to the chat api.

curl -X POST -H "Content-Type: application/json" -d @request.json http://localhost:5000/api/chat



Example request to RASA NLU

curl localhost:5005/model/parse -d '{"text":"hello"}'