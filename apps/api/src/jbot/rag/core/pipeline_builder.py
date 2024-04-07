from llama_index.core.query_pipeline import (
    QueryPipeline,
    InputComponent,
    ArgPackComponent,
)
from llama_index.core import PromptTemplate, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.postprocessor import LLMRerank
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core.postprocessor import PrevNextNodePostprocessor

from jbot.rag.core.query_component.join_nodes_component import JoinNodesComponent
from jbot.rag.core.query_component.parent_node_postprocessor import (
    ParentNodePostprocessor,
)


def build_query_pipeline(indexes):
    act_index = indexes["act"]
    inquiry_index = indexes["inquiry"]
    act_enforcement_index = indexes["act_enforcement"]

    # define modules
    hyde_prompt_str = (
        "Please write a passage to answer the question\n"
        "Try to include as many key details as possible.\n"
        "Please write in language of the question.\n"
        "\n"
        "\n"
        "{query_str}\n"
        "\n"
        "\n"
        'Passage:"""\n'
    )
    hyde_prompt_tmpl = PromptTemplate(hyde_prompt_str)
    llm = OpenAI(model="gpt-3.5-turbo-0125")

    act_retriever = act_index.as_retriever(similarity_top_k=3)
    act_parent_retriever = ParentNodePostprocessor(
        docstore=act_index.docstore,
    )
    act_reranker = LLMRerank()

    act_enforcement_retriever = act_enforcement_index.as_retriever(similarity_top_k=3)
    act_enforcement_parent_retriever = ParentNodePostprocessor(
        docstore=act_enforcement_index.docstore,
    )

    q_retriever = inquiry_index.as_retriever(
        similarity_top_k=1,
        filters=MetadataFilters(
            filters=[ExactMatchFilter(key="type", value="question")]
        ),
    )
    q_answer_fetcher = PrevNextNodePostprocessor(
        docstore=inquiry_index.docstore,
        num_nodes=1,  # number of nodes to fetch when looking forawrds or backwards
        mode="next",  # can be either 'next', 'previous', or 'both'
    )
    q_reranker = LLMRerank()
    qa_prompt_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge. Please provide a well-reasoned answer. If the legal basis is known, include the applicable legal provision.\n"
        "Below your answer, please provide the 참고자료 that you use to answer. \n"
        "The reference information is provided in Context information. Include file name and label. The format is (filename, label)\n"
        "If you use multiple 참고자료, please provide the list of 참고자료.\n"
        "Answer in Korean.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    response_synthesizer = get_response_synthesizer(text_qa_template=qa_prompt_tmpl)
    join = JoinNodesComponent()

    # define query pipeline
    p = QueryPipeline(verbose=True)
    p.add_modules(
        {
            "input": InputComponent(),
            "q_retriever": q_retriever,
            "q_answer_fetcher": q_answer_fetcher,
            "act_retriever": act_retriever,
            "act_parent_retriever": act_parent_retriever,
            "act_enforcement_retriever": act_enforcement_retriever,
            "act_enforcement_parent_retriever": act_enforcement_parent_retriever,
            "synthesizer": response_synthesizer,
            "arg_pack": ArgPackComponent(),
            "join": join,
        }
    )

    p.add_link("input", "q_retriever")
    p.add_link("input", "act_retriever")
    p.add_link("input", "act_enforcement_retriever")
    p.add_link("q_retriever", "q_answer_fetcher", dest_key="nodes")
    p.add_link("q_answer_fetcher", "arg_pack", dest_key="q")
    p.add_link("act_retriever", "act_parent_retriever", dest_key="nodes")
    p.add_link("act_parent_retriever", "arg_pack", dest_key="act")
    p.add_link(
        "act_enforcement_retriever",
        "act_enforcement_parent_retriever",
        dest_key="nodes",
    )
    p.add_link(
        "act_enforcement_parent_retriever", "arg_pack", dest_key="act_enforcement"
    )
    p.add_link("arg_pack", "join", dest_key="packed_nodes")
    p.add_link("join", "synthesizer", dest_key="nodes")
    p.add_link("input", "synthesizer", dest_key="query_str")

    return p
