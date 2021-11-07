from aiogram import types


async def test_handlers_from_another_file(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
