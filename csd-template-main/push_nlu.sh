#!/bin/bash
cd "$(dirname "$0")"

bot=$1
cd $1/rasa-nlu
docker build -t $bot-rasa-nlu-amd64 --platform linux/amd64 .
img="vm014.qu.tu-berlin.de:6000/$bot-rasa-nlu-amd64"
docker tag $bot-amd64 $img
docker push $img

echo ""
echo "#################"
echo "pushed new docker image"
echo $img
echo "#################"
