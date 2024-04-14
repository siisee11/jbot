import os
from jbot.github.github import MyGithub
from jbot.vectorstore.weaviate import MyWeaviateVectorStore
from llama_index.core.schema import TextNode
from llama_index.core import Document


EMBED_TARGET_EXTENSIONS = [".py", ".ts", ".tsx", ".md"]


class Embedder:
    index = None

    def __init__(self, vectorstore: MyWeaviateVectorStore) -> None:
        self.root_dir = "data/getgpt"
        self.github = MyGithub()
        self.vectorstore = vectorstore

        self.index = self.load_vectorstore_index()

        if self.index is None:
            self.extract_all_files()
            self.embed()

    def extract_all_files(self):
        self.docs: list[Document] = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_extension = os.path.splitext(filename)[1]
                if file_extension in EMBED_TARGET_EXTENSIONS:
                    try:
                        with open(
                            os.path.join(dirpath, filename), "r", encoding="utf-8"
                        ) as f:
                            data = f.read()
                            doc = Document(
                                text=data,
                                metadata={
                                    "filename": filename,
                                    "extension": file_extension,
                                    "filepath": dirpath.replace(self.root_dir, "")
                                    + "/"
                                    + filename,
                                },
                            )
                            self.docs.append(doc)
                            return  # for now extract only one file
                    except Exception as e:
                        print(e)
                        pass

        print("# of docs loaded", len(self.docs))

    def embed(self):
        print("embed: docs[0]", self.docs[0])
        self.vectorstore.add_documents(self.docs)

    def _delete_directory(self, path):
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
            os.rmdir(path)

    def load_vectorstore_index(self):
        return self.vectorstore.load()

    def retrieve_results(self, query):
        result = self.vectorstore.query(query)
        return result["response"]
