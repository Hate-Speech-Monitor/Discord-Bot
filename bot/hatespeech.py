from dotenv import load_dotenv
import json
from expertai.nlapi.cloud.client import ExpertAiClient

load_dotenv('.env.local')
detector = 'hate-speech'
language = 'en'
client = ExpertAiClient()


def evaluate(content):
    output = client.detection(body={"document": {"text": content}}, params={
                              'detector': detector, 'language': language})
    return len(output.categories)
