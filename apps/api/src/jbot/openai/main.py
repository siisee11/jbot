from src.jbot.openai.assistant import OpenAIAssistant

# my_assistant = OpenAIAssistant(
#     assistant_id="asst_1iA2KbtRW0lenVJmnesuJMcF",
#     vector_store_id="vs_8JexOG6WgPCIPCZdkjQ4M6yR",
# )
assistant_id = "asst_64OUin9tDFmOPi0qkCZLs5Gu"  # wordbricks bot (code search)
my_assistant = OpenAIAssistant()
my_assistant.create_or_load_assistant(assistant_id=assistant_id)
# my_assistant.create_vector_store("getgpt")
my_assistant.chat("How to run GetGPT?")
# print(my_assistant.list_assistants())
