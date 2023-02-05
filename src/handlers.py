import os

import openai
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

openai.api_key = os.getenv('OPENAI_API_KEY')
model_engine = 'text-davinci-003'

start_message = 'Привет, этот бот дает доступ к GPT-3 без регистрации ' \
                'и СМС в любой стране. Я переадресую нейросети все твои ' \
                'сообщения, а чтобы начать новый диалог используй ' \
                'команду /new.'
new_message = 'Данные диалога очищены, можешь начинать заново'
bad_response = 'Некорректный ответ, попробуйте ещё раз'


async def start(message: Message):
    await message.answer(start_message)


async def new(message: Message, state: FSMContext):
    await state.set_data({'context': ''})
    await message.answer(new_message)


async def on_message(message: Message, state: FSMContext):
    context = (await state.get_data()).get('context', '')
    promt = f'context: {context}\n\nprompt: + {message.text}'

    completion = await openai.Completion.acreate(
        engine=model_engine,
        prompt=promt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    response = completion.choices[0].text

    await message.answer(response or bad_response)

    new_context = f"{context}\n\n{message.text}\n\n{response}"
    await state.set_data({'context': new_context})
