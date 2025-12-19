# Overview
This repo aims to showcase the basic functionality of a RAG (resource augmented generation) application, utilizing a soccer training PDF markdown, to provide the User precise instructions on how to improve their technical and tactical awareness.
# Libraries
```
pip3 install -r requirements.txt
```
# API Usage
This RAG demo used OpenAI's API, for which you must generate a key, and add it to an environmental variable, for safely loading it in the embedding script.
# Functionality
Clone the repo into your local system, run the libararies installation, and then generate OpenAI embedings with
```
python3 openai_embeddings.py
```
Then, view the answer to your training queries by running:
```
python3 rag.py
```
# Results
## Queries:
```
print(ask("How do young players learn speed of play?"))
print(ask("What is a quick and effective drill to practice offensive shooting?"))
print(ask("How many players make up a basketball team?"))
```
## Answers:
Young players learn speed of play through the process of being in game situations that present various challenges. This involves recognizing and adapting to what the game presents, which requires experimentation and problem-solving rather than mere repetition in controlled environments. Coaches should create environments that encourage players to discover for themselves where spaces exist and how to exploit them, rather than directing their actions. Additionally, players develop different aspects of speed, such as visual speed, anticipatory speed, and decision-making speed, through experiences in game-like scenarios where they can solve problems and make decisions based on the cues from the game itself.

A quick and effective drill to practice offensive shooting is the "1v1 Recovery Game." In this drill, one player (A1) dribbles as close to the opponent's goal as they want and takes a shot. Immediately after shooting, A1 retreats to play in goal while the next player (B1) dribbles and shoots at A1. This drill allows for continuous shooting opportunities with minimal downtime, as players alternate between shooting and goalkeeping.

I could not find an answer.
