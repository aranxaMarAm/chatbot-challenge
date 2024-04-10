#!/bin/bash
cd "$(dirname "$0")"

bot=$1
cd $1/python-backend
docker build -t $bot-python-backend-amd64 --platform linux/amd64 .
img="vm014.qu.tu-berlin.de:6000/$bot-python-backend-amd64"
docker tag $bot-amd64 $img
docker push $img

echo ""
echo "#################"
echo "pushed new docker image"
echo $img
echo "#################"
