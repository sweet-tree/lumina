"""
Spiritual Coach App with Gradio Interface
A user-friendly interface for the spiritual coach RAG system.
"""

import gradio as gr
from gradio.themes import Soft
from rag import RAGService


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


def create_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(theme=Soft()) as demo:
        # Header
        gr.Markdown("# 🌿 Spiritual Coach")
        gr.Markdown(
            "Share your thoughts and receive personalized guidance combining psychological principles with authentic spiritual teachings.")

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
        server_port=7860,
        share=True,
        show_api=False,
        debug=True
    )


if __name__ == "__main__":
    main()
