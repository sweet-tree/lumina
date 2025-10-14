"""
Document processing service for handling PDF uploads and text extraction.
Uses pymupdf4llm for high-quality PDF text extraction with markdown formatting.
"""

import os
import uuid
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import pymupdf4llm


class DocumentProcessor:
    """Service for processing uploaded documents and extracting text."""

    def __init__(self, uploads_dir: str = "uploads", metadata_dir: str = "metadata"):
        """
        Initialize the document processor.

        Args:
            uploads_dir: Directory to store uploaded files
            metadata_dir: Directory to store document metadata
        """
        self.uploads_dir = Path(uploads_dir)
        self.metadata_dir = Path(metadata_dir)
        self.metadata_file = self.metadata_dir / "documents.json"

        # Create directories if they don't exist
        self.uploads_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)

        # Initialize metadata file if it doesn't exist
        if not self.metadata_file.exists():
            with open(self.metadata_file, 'w') as f:
                json.dump([], f)

    def generate_document_id(self) -> str:
        """Generate a unique document ID."""
        return str(uuid.uuid4())

    def save_upload(self, file_path: str, filename: str) -> str:
        """
        Save uploaded file to the uploads directory.

        Args:
            file_path: Path to the uploaded file
            filename: Original filename

        Returns:
            Path to the saved file
        """
        # Generate unique filename
        file_ext = Path(filename).suffix
        unique_filename = f"{self.generate_document_id()}{file_ext}"
        save_path = self.uploads_dir / unique_filename

        # Copy file to uploads directory
        with open(file_path, 'rb') as src, open(save_path, 'wb') as dst:
            dst.write(src.read())

        return str(save_path)

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a PDF file using pymupdf4llm.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text in markdown format

        Raises:
            Exception: If text extraction fails
        """
        try:
            # Convert PDF to markdown with pymupdf4llm
            md_text = pymupdf4llm.to_markdown(file_path)
            return md_text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def chunk_text(self, text: str, max_chunk_size: int = 1500, min_chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks suitable for vector storage.

        Args:
            text: Text to chunk
            max_chunk_size: Maximum size of each chunk
            min_chunk_size: Minimum size of each chunk

        Returns:
            List of text chunks
        """
        chunks = []
        current_chunk = ""

        # Split by paragraphs (double newlines)
        paragraphs = text.split('\n\n')

        for paragraph in paragraphs:
            # Clean up paragraph
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If adding this paragraph would exceed max size
            if len(current_chunk) + len(paragraph) + 2 > max_chunk_size and len(current_chunk) >= min_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk if it meets minimum size
        if current_chunk and len(current_chunk) >= min_chunk_size:
            chunks.append(current_chunk.strip())
        elif chunks and current_chunk:
            # Add to last chunk if it's small
            chunks[-1] += "\n\n" + current_chunk.strip()

        return chunks

    def save_metadata(self, metadata: Dict) -> None:
        """
        Save document metadata to the metadata file.

        Args:
            metadata: Document metadata to save
        """
        # Load existing metadata
        with open(self.metadata_file, 'r') as f:
            documents = json.load(f)

        # Add new document
        documents.append(metadata)

        # Save updated metadata
        with open(self.metadata_file, 'w') as f:
            json.dump(documents, f, indent=2)

    def get_document_by_id(self, doc_id: str) -> Optional[Dict]:
        """
        Retrieve document metadata by ID.

        Args:
            doc_id: Document ID to retrieve

        Returns:
            Document metadata if found, None otherwise
        """
        with open(self.metadata_file, 'r') as f:
            documents = json.load(f)

        for doc in documents:
            if doc.get('id') == doc_id:
                return doc

        return None

    def list_documents(self) -> List[Dict]:
        """
        List all stored documents.

        Returns:
            List of document metadata
        """
        with open(self.metadata_file, 'r') as f:
            documents = json.load(f)

        return documents

    def process_document(self, file_path: str, filename: str, password: Optional[str] = None,
                         title: Optional[str] = None, author: Optional[str] = None,
                         tradition: Optional[str] = None) -> Dict:
        """
        Process an uploaded document: save, extract text, chunk, and store metadata.

        Args:
            file_path: Path to the uploaded file
            filename: Original filename
            password: Password for encrypted PDFs (optional)
            title: Document title (optional, will be extracted from filename if not provided)
            author: Document author (optional)
            tradition: Spiritual tradition (optional)

        Returns:
            Dictionary containing document information and extracted text chunks
        """
        # Generate document ID
        doc_id = self.generate_document_id()

        # Use filename as title if not provided
        if not title:
            title = Path(filename).stem

        # Save the uploaded file
        saved_path = self.save_upload(file_path, filename)

        # Extract text from PDF
        extracted_text = self.extract_text(saved_path)

        # Chunk the text
        chunks = self.chunk_text(extracted_text)

        # Create metadata
        metadata = {
            "id": doc_id,
            "title": title,
            "author": author,
            "tradition": tradition,
            "filename": filename,
            "saved_path": saved_path,
            "upload_date": str(datetime.now()),
            "chunk_count": len(chunks),
            "status": "processed"
        }

        # Save metadata
        self.save_metadata(metadata)

        return {
            "id": doc_id,
            "metadata": metadata,
            "chunks": chunks,
            "text": extracted_text
        }
