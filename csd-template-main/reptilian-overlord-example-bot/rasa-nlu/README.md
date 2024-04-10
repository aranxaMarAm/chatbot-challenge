# RASA NLU Server

Official documentation: https://rasa.com/docs/rasa/nlu-only-server/

Run it (replace the path to the model):

```
rasa run --enable-api -m models/20240328-132336-express-director.tar.gz
```

Example CURL request: 

```
curl localhost:5005/model/parse -d '{"text":"hello"}'
```
