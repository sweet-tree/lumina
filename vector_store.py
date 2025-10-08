from typing import List, Dict, Any, Optional, Iterator, Tuple
from pinecone import Pinecone, ServerlessSpec
from config import Config
from embeddings import EmbeddingService
from document_processor import DocumentProcessor
import itertools


class VectorStore:
    """Service for storing and retrieving vectors using Pinecone."""

    def __init__(self):
        Config.validate()
        self.embedding_service = EmbeddingService()
        self.document_processor = DocumentProcessor()

        # Initialize Pinecone
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)

        # Define index name
        self.index_name = "spiritual-coach"

        # Create index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=4096,  # Qwen3-Embedding-8B returns 4096-dimensional vectors
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        # Connect to the index
        self.index = self.pc.Index(self.index_name)

    def upsert_texts(self, texts: List[str], namespace: str = "spiritual-teachings") -> None:
        """
        Store texts in the vector database.

        Args:
            texts: List of text strings to store
            namespace: Namespace to store the vectors in
        """
        # Generate embeddings
        embeddings = self.embedding_service.create_embeddings(texts)

        # Prepare vectors for upsert
        vectors = []
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            vector = {
                "id": f"teaching_{i}",
                "values": embedding,
                "metadata": {"text": text}
            }
            vectors.append(vector)

        # Upsert vectors
        self.index.upsert(vectors=vectors, namespace=namespace)

    def _chunks(self, iterable: List, batch_size: int = 200) -> Iterator[Tuple]:
        """
        A helper function to break an iterable into chunks of size batch_size.

        Args:
            iterable: The iterable to chunk
            batch_size: Size of each chunk

        Yields:
            Tuples of chunks
        """
        it = iter(iterable)
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, batch_size))

    def upsert_document(self, file_path: str, filename: str,
                        title: Optional[str] = None, author: Optional[str] = None,
                        tradition: Optional[str] = None, namespace: str = "spiritual-library") -> Dict:
        """
        Process and upsert a document from a PDF file.

        Args:
            file_path: Path to the PDF file
            filename: Original filename
            title: Document title (optional)
            author: Document author (optional)
            tradition: Spiritual tradition (optional)
            namespace: Namespace to store the vectors in

        Returns:
            Dictionary containing document information
        """
        # Process the document
        result = self.document_processor.process_document(
            file_path, filename, title=title, author=author, tradition=tradition
        )

        # Extract chunks and metadata
        chunks = result["chunks"]
        metadata = result["metadata"]

        # Generate embeddings for chunks
        embeddings = self.embedding_service.create_embeddings(chunks)

        # Prepare vectors for upsert
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector = {
                "id": f"{metadata['id']}:{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "document_id": metadata["id"],
                    "title": metadata["title"],
                    "author": metadata["author"],
                    "tradition": metadata["tradition"],
                    "filename": metadata["filename"]
                }
            }
            vectors.append(vector)

        # Upsert vectors to Pinecone in batches to avoid size limits
        batch_size = 100  # Reduced batch size to stay under 2MB limit
        for vectors_chunk in self._chunks(vectors, batch_size=batch_size):
            self.index.upsert(vectors=list(vectors_chunk), namespace=namespace)

        return result

    def _rerank_results(self, query: str, documents: List[str], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Rerank documents based on their relevance to the query using the Qwen3-Embedding-8B model.

        Args:
            query: The search query
            documents: List of document texts to rerank
            top_n: Number of top results to return

        Returns:
            List of reranked results with text and relevance score
        """
        # Create pairs of query and document for reranking
        pairs = [[query, doc] for doc in documents]

        # Use the embedding service to get relevance scores
        # The Qwen3-Embedding-8B model can evaluate query-document relevance
        try:
            # Get embeddings for the pairs
            embeddings = self.embedding_service.create_embeddings(
                [f"Query: {query} Document: {doc}" for doc in documents])

            # Calculate similarity scores between query and document embeddings
            # For simplicity, we'll use the first half of the embedding as query representation
            # and the second half as document representation
            query_embedding = self.embedding_service.create_embedding(query)
            scores = []
            for i, emb in enumerate(embeddings):
                # Calculate cosine similarity
                dot_product = sum(
                    a * b for a, b in zip(query_embedding[:len(query_embedding)//2], emb[:len(emb)//2]))
                norm_query = sum(
                    a * a for a in query_embedding[:len(query_embedding)//2]) ** 0.5
                norm_doc = sum(b * b for b in emb[:len(emb)//2]) ** 0.5
                if norm_query * norm_doc == 0:
                    similarity = 0
                else:
                    similarity = dot_product / (norm_query * norm_doc)
                scores.append((similarity, documents[i]))

            # Sort by score and return top_n
            scores.sort(reverse=True)
            return [{"text": doc, "score": score} for score, doc in scores[:top_n]]

        except Exception as e:
            print(f"Error in reranking: {e}")
            # Fallback to original results if reranking fails
            return [{"text": doc, "score": 0.0} for doc in documents[:top_n]]

    def search(self, query: str, top_k: int = 10, namespace: str = "spiritual-teachings") -> List[Dict[str, Any]]:
        """
        Search for similar vectors and rerank results for better relevance.

        Args:
            query: Query string to search for
            top_k: Number of candidate results to retrieve (before reranking)
            namespace: Namespace to search in

        Returns:
            List of reranked results with text and relevance score
        """
        # Generate embedding for query
        query_embedding = self.embedding_service.create_embedding(query)

        # Search for similar vectors (retrieve more candidates for reranking)
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return []

        # Extract candidate documents
        candidates = []
        try:
            matches = getattr(results, 'matches', [])  # type: ignore
            for match in matches:
                candidates.append(match.metadata["text"])
        except Exception as e:
            print(f"Error processing results: {e}")
            return []

        # Rerank the candidates and return top 3
        return self._rerank_results(query, candidates, top_n=3)
