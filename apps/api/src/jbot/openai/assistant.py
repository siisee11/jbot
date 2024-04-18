import os
from jbot.openai.constants import VECTOR_STORE_TARGET_FILE_EXTENSION
from openai import NOT_GIVEN, OpenAI
from openai.types.beta import Assistant, Thread

from jbot import config


class OpenAIAssistant:
    client: OpenAI
    assistant: Assistant
    thread: Thread = None

    def __init__(self):
        self.client = OpenAI(api_key=config.get_or_error("OPENAI_API_KEY"))
        print(self.client.beta.vector_stores.list())

    def create_or_load_assistant(
        self, assistant_id: str = None, vector_store_id: str = None
    ):
        if assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        else:
            self.assistant = self.client.beta.assistants.create(
                name="Code Search Assistant",
                instructions="You are an expert programmer and you have access to code base. Use you knowledge base to search relevant code.",
                model="gpt-4-turbo",
                tools=[{"type": "file_search"}],
                tool_resources=(
                    ({"file_search": {"vector_store_ids": [vector_store_id]}})
                    if vector_store_id
                    else NOT_GIVEN
                ),
            )
            print("assistant created", self.assistant.id)

    def list_assistants(self):
        return list(self.client.beta.assistants.list())

    def create_vector_store(self, name: str, file_root_dir: str = "data/getgpt"):
        vector_store = self.client.beta.vector_stores.create(name=name)

        file_paths = []
        for dirpath, dirnames, filenames in os.walk(file_root_dir):
            print("-------------", dirpath, "---------------")
            for filename in filenames:
                file_extension = os.path.splitext(filename)[1][1:]
                if file_extension in VECTOR_STORE_TARGET_FILE_EXTENSION:
                    file_paths.append(os.path.join(dirpath, filename))

            if len(file_paths) < 100:
                continue
            self.upload_files(file_paths=file_paths, vector_store_id=vector_store.id)
            file_paths = []

        self.upload_files(file_paths=file_paths, vector_store_id=vector_store.id)

        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

    def upload_files(self, file_paths: list[str], vector_store_id: str):
        file_streams = [open(path, "rb") for path in file_paths]
        try:
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store_id, files=file_streams
            )
            # You can print the status and the file counts of the batch to see the result of this operation.
            print("status", file_batch.status, "# of files:", file_batch.file_counts)
            print("------------------------------------")
        except Exception as e:
            print(e)
        finally:
            for stream in file_streams:
                stream.close()

    def create_new_thread(self, message: str):
        self.thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ]
        )

    def chat(self, message: str):
        if self.thread is None:
            self.create_new_thread(message)
        else:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, role="user", content=message
            )
        self.run_thread()

    def run_thread(self):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )

        messages = list(
            self.client.beta.threads.messages.list(
                thread_id=self.thread.id, run_id=run.id
            )
        )

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))
