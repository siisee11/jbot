import os
import pandas as pd
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
from jbot.rag.constants import (
    INDEX_PERSIST_DIR,
    REPOSITORY_DATA_ROOT,
)
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage


def load_repo_index():
    if not os.path.exists(INDEX_PERSIST_DIR):
        # nodes: list[TextNode] = []

        # node = TextNode(
        #     id_=f"{chapter_id}_{article_id}_{index}",
        #     text=row["content"],
        #     metadata={
        #         "filename": "정보통신공사업법",
        #         "label": f"{chapter_id}장 {article_id}조",
        #         "chapter_title": row["chapter_title"],
        #         "article_title": row["article_title"],
        #         "chapter_id": chapter_id,
        #         "article_id": article_id,
        #     },
        #     excluded_llm_metadata_keys=["chapter_id", "article_id"],
        # )

        # node.relationships[NodeRelationship.PARENT] = RelatedNodeInfo(
        #     node_id=curr_article_node.id_,
        # )

        # nodes.append(node)

        reader = SimpleDirectoryReader(input_dir=REPOSITORY_DATA_ROOT)
        documents = reader.load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=INDEX_PERSIST_DIR)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=INDEX_PERSIST_DIR),
        )

    return index
