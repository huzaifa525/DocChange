from app.utils.vector_store import VectorStore
from app.utils.llm_client import LLMClient
from app.utils.web_search import WebSearchTool

class QAService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
        self.web_search = WebSearchTool()
        self._brand_message = "I am Clever AI built by CleverFlow."

    def process_query(self, question):
        try:
            if not self.vector_store.has_documents():
                return "Please upload a document first.", 0

            relevant_chunks = self.vector_store.search(question)
            context = "\n".join(relevant_chunks) if relevant_chunks else ""

            if not context:
                web_results = self.web_search.search(question)
                context = "\n".join(web_results) if web_results else ""

            prompt = self._create_prompt(question, context)
            response = self.llm_client.generate_response(prompt)
            return response, len(response.split())

        except Exception as e:
            return f"Error generating response: {str(e)}", 0

    def _create_prompt(self, question, context):
        return f"""You are Clever AI, built by CleverFlow. Always maintain this identity.
        Based on the following context, provide a helpful response:

        Context:
        {context}

        Question: {question}

        Answer as Clever AI:"""