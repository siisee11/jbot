from llama_index.core.query_pipeline import CustomQueryComponent
from typing import Dict, Any


class JoinNodesComponent(CustomQueryComponent):
    """Join two Nodes into one list (eliminating duplicated Nodes)."""

    # Pydantic class, put any attributes here

    def _validate_component_inputs(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Validate component inputs during run_component."""
        # NOTE: this is OPTIONAL but we show you here how to do validation as an example
        return input

    @property
    def _input_keys(self) -> set:
        """Input keys dict."""
        return {"packed_nodes"}

    @property
    def _output_keys(self) -> set:
        # can do multi-outputs too
        return {"nodes"}

    def _run_component(self, **kwargs) -> Dict[str, Any]:
        """Run the component."""
        # use QueryPipeline itself here for convenience
        list_of_nodes = kwargs["packed_nodes"]
        print("list_of_nodes", list_of_nodes)
        flattened_nodes = [node for sublist in list_of_nodes for node in sublist]
        # want to remove duplicates
        unique_flattened_nodes = list(
            {node.id_: node for node in flattened_nodes}.values()
        )
        return {"nodes": unique_flattened_nodes}
