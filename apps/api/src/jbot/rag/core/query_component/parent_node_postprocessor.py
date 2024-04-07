from typing import Dict, List, Optional
from llama_index.core.bridge.pydantic import Field, validator
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.response_synthesizers import (
    ResponseMode,
    get_response_synthesizer,
)
from llama_index.core.schema import NodeRelationship, NodeWithScore, QueryBundle
from llama_index.core.service_context import ServiceContext
from llama_index.core.storage.docstore import BaseDocumentStore


def get_parent_node(
    node_with_score: NodeWithScore, docstore: BaseDocumentStore
) -> Dict[str, NodeWithScore]:
    """Get Parent nodes."""
    node = node_with_score.node
    nodes: Dict[str, NodeWithScore] = {}

    next_node_info = node.parent_node
    if next_node_info is None:
        # parent is none = it is self article
        nodes[node.node_id] = node_with_score
        return nodes

    next_node_id = next_node_info.node_id
    next_node = docstore.get_node(next_node_id)
    nodes[next_node.node_id] = NodeWithScore(node=next_node)
    return nodes


class ParentNodePostprocessor(BaseNodePostprocessor):
    """Parent Node post-processor.

    Allows users to fetch additional nodes from the document store,
    based on the relationships of the nodes.

    NOTE: this is a beta feature.

    Args:
        docstore (BaseDocumentStore): The document store.
    """

    docstore: BaseDocumentStore

    @classmethod
    def class_name(cls) -> str:
        return "PrevNextNodePostprocessor"

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        """Postprocess nodes."""
        all_parent_nodes: Dict[str, NodeWithScore] = {}
        for node in nodes:
            parent_node = get_parent_node(node, self.docstore)
            all_parent_nodes.update(parent_node)

        all_parent_nodes_values: List[NodeWithScore] = list(all_parent_nodes.values())
        return all_parent_nodes_values
