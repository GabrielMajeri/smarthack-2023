import logging

from dotenv import dotenv_values
from fastapi import FastAPI
import openai


app = FastAPI()
env = dotenv_values()
logger = logging.getLogger('smarthack-api')


ft_model = env['OPENAI_FT_MODEL']

client = openai.OpenAI(api_key=env['OPENAI_API_KEY'])


@app.get('/')
async def root():
    return {'message': 'Hello world!'}

@app.get('/test/')
async def test():
    response = client.chat.completions.create(
        model=ft_model,
        messages=[
            {'role': 'system', 'content':'Esti un asistent folositor.'},
            {'role': 'user', 'content': 'Salut!'}
        ]
    )

    return {'message': response.choices[0].message.content}


@app.post('/extract-product/')
async def test(prompt: str):
    response = client.chat.completions.create(
        model=ft_model,
        messages=[
            {
                'role': 'system',
                'content':
                    "You are an assistant trying extract what items someone wants to buy. Write the answer in plain text format. Write only the items separated by a comma without the quantity. Write each item to singular, not to plural."},
            {
                'role': 'user',
                'content':
                    f'''What does the following person try to buy:
                    {prompt}    
                    '''
            }
        ]
    )

    try:
        formatted = response.choices[0].message.content.lower().split(", ")
    except Exception:
        return {'items': []}

    return {'items': formatted}


@app.post('/synonym/')
async def test(prompt: str, n: int):
    response = client.chat.completions.create(
        model=ft_model,
        messages=[
            {
                'role': 'system',
                'content':
                    "You are an assistant trying give synonyms for a word given by the user. Write the answer in plain text format. Write the items separated by a comma without any other punctuation."},
            {
                'role': 'user',
                'content':
                    f'Give {n} synonyms for: {prompt}'
            }
        ]
    )

    try:
        formatted = response.choices[0].message.content.lower().split(", ")
    except Exception:
        return {'items': []}

    return {'items': formatted}


@app.post('/justification-notice/')
async def test(prompt: str):
    response = client.chat.completions.create(
        model=ft_model,
        messages=[
            {
                'role': 'system',
                'content':
                    "You are an assistant trying to help a public institution which has to fill out a form justifying why they want to make some acquisitions. These acquisitions will be used to develop the community and improve many aspects of both the institution and the community. Consider describing the utility of the item, its contribution, its necessity, key factors for success and other relevant factors. The response should not have headings and should be formal, but not too formal. Keep it short and return only the main content without headers and footers."},
            {
                'role': 'user',
                'content':
                    f'Write such a text for acquiring a {prompt}'
            }
        ]
    )

    try:
        formatted = response.choices[0].message.content
    except Exception:
        return {'content': ''}

    return {'content': formatted}
