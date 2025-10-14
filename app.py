"""
Spiritual Coach App with Gradio Interface
A user-friendly interface for the spiritual coach RAG system.
"""

import gradio as gr
from gradio.themes import Soft
from backend.services.rag_service import RAGService
from backend.services.vector_store_service import VectorStore
from backend.services.document_processor_service import DocumentProcessor
import os


def get_spiritual_guidance(diary_entry):
    """
    Generate spiritual guidance based on user's diary entry.

    Args:
        diary_entry (str): The user's diary entry or question

    Returns:
        str: Personalized spiritual guidance
    """
    # Validate input
    if not diary_entry or not diary_entry.strip():
        return "Please share something about your day, thoughts, or challenges so I can offer guidance."

    try:
        # Initialize RAG service
        rag_service = RAGService()

        # Generate response
        response = rag_service.generate_response(diary_entry.strip())

        return response

    except Exception as e:
        # Log the error (in a real app, you'd use proper logging)
        print(f"Error generating guidance: {e}")
        return ("I'm having trouble connecting to the spiritual guidance system. "
                "Please try again. If the problem persists, there may be an issue "
                "with the AI service or network connection.")


def upload_document(file, title, author, tradition):
    """Handle document upload and processing."""
    if file is None:
        return "Please select a PDF file to upload."

    try:
        # Initialize vector store
        vector_store = VectorStore()

        # Process and upsert the document
        result = vector_store.upsert_document(
            file.name,
            file.name.split("/")[-1],
            title,
            author,
            tradition
        )

        return f"Document '{result['metadata']['title']}' uploaded and processed successfully! " \
            f"Created {result['metadata']['chunk_count']} chunks."

    except Exception as e:
        return f"Error uploading document: {str(e)}"


def create_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(theme=Soft()) as demo:
        # Header
        gr.Markdown("# 🌿 Spiritual Coach")
        gr.Markdown(
            "Share your thoughts and receive personalized guidance combining psychological principles with authentic spiritual teachings.")

        # Admin Section for Document Upload
        gr.Markdown("## 📚 Admin Document Management")
        gr.Markdown("Upload spiritual texts and teachings (Admin only)")

        with gr.Row():
            with gr.Column():
                # File upload component
                file_input = gr.File(
                    label="Upload PDF Document",
                    file_types=[".pdf"],
                    file_count="single"
                )

                # Metadata inputs
                title_input = gr.Textbox(
                    label="Document Title",
                    placeholder="Enter document title"
                )
                author_input = gr.Textbox(
                    label="Author",
                    placeholder="Enter author name"
                )
                tradition_input = gr.Textbox(
                    label="Spiritual Tradition",
                    placeholder="Enter tradition (e.g., Buddhist, Dzogchen)"
                )

                # Upload button
                upload_btn = gr.Button("Upload Document", variant="primary")

            with gr.Column():
                # Upload status
                upload_status = gr.Textbox(
                    label="Upload Status",
                    value="No document uploaded yet"
                )

        # Main User Interface
        gr.Markdown("---")
        gr.Markdown("# 💬 Spiritual Guidance")
        gr.Markdown("Share your thoughts and receive personalized guidance")

        with gr.Row():
            with gr.Column(scale=2):
                # Input Area
                diary_input = gr.Textbox(
                    label="Your Diary Entry",
                    placeholder="Write about your day, thoughts, or challenges...",
                    lines=12,
                    show_copy_button=True
                )

                # Action Button
                submit_btn = gr.Button("Receive Guidance", variant="primary")

            with gr.Column(scale=3):
                # Output Area
                guidance_output = gr.Markdown(
                    label="Spiritual Guidance",
                    value="Your personalized guidance will appear here..."
                )

        # Footer
        gr.Markdown("---")
        gr.Markdown(
            "This spiritual coach combines psychological principles with authentic teachings "
            "from Buddhist and Dzogchen traditions to help you live in the present moment, "
            "develop good habits, and work toward enlightenment."
        )

        # Event Handling
        submit_btn.click(
            fn=get_spiritual_guidance,
            inputs=diary_input,
            outputs=guidance_output
        )

        # Allow submission with Enter key
        diary_input.submit(
            fn=get_spiritual_guidance,
            inputs=diary_input,
            outputs=guidance_output
        )

        # Document upload event
        upload_btn.click(
            fn=upload_document,
            inputs=[file_input, title_input, author_input,
                    tradition_input],
            outputs=upload_status
        )

    return demo


def main():
    """Launch the spiritual coach app."""
    print("Initializing Spiritual Coach App...")
    demo = create_interface()

    print("Launching interface...")
    # Launch with share=True to create a public link
    # In production, you might want to use share=False and host locally
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=True,
        show_api=False,
        debug=True
    )


if __name__ == "__main__":
    main()
