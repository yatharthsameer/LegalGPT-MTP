from itertools import chain
from injector import inject, singleton
from llama_index.core import (
    Document,
    StorageContext,
    SummaryIndex,
)
from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.core.node_parser import SemanticSplitterNodeParser  # Updated
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.storage.docstore.types import RefDocInfo
from llama_index.core.types import TokenGen

from private_gpt.components.embedding.embedding_component import EmbeddingComponent
from private_gpt.components.llm.llm_component import LLMComponent
from private_gpt.components.node_store.node_store_component import NodeStoreComponent
from private_gpt.components.vector_store.vector_store_component import (
    VectorStoreComponent,
)
from private_gpt.open_ai.extensions.context_filter import ContextFilter
from private_gpt.settings.settings import Settings

DEFAULT_SUMMARIZE_PROMPT = """
    You are a legal analyst specializing in Indian law, known for highly accurate and detailed summaries of case documents.
    Summarize this legal document by focusing on essential facts and details relevant to the case. 
    Include critical aspects such as the ruling, main arguments, applicable laws, sections, articles, 
    hearing details, petitions, cited cases, citations, participants, panelists, names of judges, victims, 
    petitioners,facts of the Case,Procedural History(district court case summary, appeals court case summary, 
    how this issue reached this Court) and any legally significant information. Please ensure the summary is concise, fact-focused, 
    and retains all important points without unnecessary information or repetition. It should be a single coherent paragraph.
"""


@singleton
class SummarizeService:
    @inject
    def __init__(
        self,
        settings: Settings,
        llm_component: LLMComponent,
        node_store_component: NodeStoreComponent,
        vector_store_component: VectorStoreComponent,
        embedding_component: EmbeddingComponent,
    ) -> None:
        self.settings = settings
        self.llm_component = llm_component
        self.node_store_component = node_store_component
        self.vector_store_component = vector_store_component
        self.embedding_component = embedding_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )

    @staticmethod
    def _filter_ref_docs(
        ref_docs: dict[str, RefDocInfo], context_filter: ContextFilter | None
    ) -> list[RefDocInfo]:
        if context_filter is None or not context_filter.docs_ids:
            return list(ref_docs.values())

        return [
            ref_doc
            for doc_id, ref_doc in ref_docs.items()
            if doc_id in context_filter.docs_ids
        ]

    def _summarize(
        self,
        use_context: bool = False,
        stream: bool = False,
        text: str | None = None,
        instructions: str | None = None,
        context_filter: ContextFilter | None = None,
        prompt: str | None = None,
    ) -> str | TokenGen:

        nodes_to_summarize = []

        # Add text to summarize
        if text:
            text_documents = [Document(text=text)]
            nodes_to_summarize += SemanticSplitterNodeParser(
                buffer_size=4,  # Adjust based on document complexity
                breakpoint_percentile_threshold=95,  # Standard for semantic splitting
            ).get_nodes_from_documents(text_documents)

        # Add context documents to summarize
        if use_context:
            # 1. Recover all ref docs
            ref_docs: dict[str, RefDocInfo] | None = (
                self.storage_context.docstore.get_all_ref_doc_info()
            )
            if ref_docs is None:
                raise ValueError("No documents have been ingested yet.")

            # 2. Filter documents based on context_filter (if provided)
            filtered_ref_docs = self._filter_ref_docs(ref_docs, context_filter)

            # 3. Get all nodes from the filtered documents
            filtered_node_ids = chain.from_iterable(
                [ref_doc.node_ids for ref_doc in filtered_ref_docs]
            )
            filtered_nodes = self.storage_context.docstore.get_nodes(
                node_ids=list(filtered_node_ids),
            )

            nodes_to_summarize += filtered_nodes

        # Create a SummaryIndex to summarize the nodes
        summary_index = SummaryIndex(
            nodes=nodes_to_summarize,
            storage_context=StorageContext.from_defaults(),  # In memory SummaryIndex
            show_progress=True,
        )

        # Make a tree summarization query
        query_engine = summary_index.as_query_engine(
            llm=self.llm_component.llm,
            response_mode=ResponseMode.TREE_SUMMARIZE,
            streaming=stream,
            use_async=self.settings.summarize.use_async,
        )

        prompt = prompt or DEFAULT_SUMMARIZE_PROMPT
        summarize_query = prompt + "\n" + (instructions or "")

        response = query_engine.query(summarize_query)
        if isinstance(response, Response):
            return response.response or ""
        elif isinstance(response, StreamingResponse):
            return response.response_gen
        else:
            raise TypeError(f"The result is not of a supported type: {type(response)}")

    def summarize(
        self,
        use_context: bool = False,
        text: str | None = None,
        instructions: str | None = None,
        context_filter: ContextFilter | None = None,
        prompt: str | None = None,
    ) -> str:
        return self._summarize(
            use_context=use_context,
            stream=False,
            text=text,
            instructions=instructions,
            context_filter=context_filter,
            prompt=prompt,
        )  # type: ignore

    def stream_summarize(
        self,
        use_context: bool = False,
        text: str | None = None,
        instructions: str | None = None,
        context_filter: ContextFilter | None = None,
        prompt: str | None = None,
    ) -> TokenGen:
        return self._summarize(
            use_context=use_context,
            stream=True,
            text=text,
            instructions=instructions,
            context_filter=context_filter,
            prompt=prompt,
        )  # type: ignore
