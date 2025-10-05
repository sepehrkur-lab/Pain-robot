from ai_client import AIClient

ai = AIClient(db_path="pain_memory.db")

# وقتی میخوای سوالی از ربات بپرسی:
res = ai.answer("Who is Sepehr?")
print(res["answer"])
# بعد این متن را TTS کن و نمایش بده.
