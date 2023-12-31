import logging
import openai
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

import helper

load_dotenv()

app = FastAPI()

origins = [
    "http://172.16.23.239/",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger('smarthack-api')


ft_model = os.environ['OPENAI_FT_MODEL'].strip()
client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'].strip())

engine = create_engine(
        URL.create(
            drivername=os.environ['POSTGRES_DRIVER'],
            username=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            database=os.environ['POSTGRES_DB']
    )
)

Session = sessionmaker(bind=engine)


@app.get('/')
async def root():
    return {'message': 'Hello world!'}


@app.post('/extract-product/')
async def extract_product(prompt: str):
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
async def synonym(prompt: str, n: int):
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
async def justification(prompt: str):
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


@app.post('/conversation/')
async def conversation(conv_id: int, msg: str):
    session = Session()

    conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-3.5-turbo"}]

    current_messages = session.execute(select(helper.Message).where(helper.Message.conversation_id == conv_id).order_by(helper.Message.id)).all()
    conversation += [{'role': m.Message.role, 'content': m.Message.content} for m in current_messages]

    message = {'role': 'user', 'content': msg}
    conversation.append(message)

    session.add(helper.Message(conversation_id=1, content=message['content'], role="user"))
    session.commit()

    response = client.chat.completions.create(
        model=ft_model,
        messages=conversation
    )

    openai_response = response.choices[0].message

    session.add(helper.Message(conversation_id=conv_id, content=openai_response.content, role="assistant"))
    session.commit()

    conversation.append(openai_response)
    session.close()

    return {'content': openai_response.content}
