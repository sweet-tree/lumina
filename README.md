# Spiritual Coach with RAG

A Retrieval-Augmented Generation (RAG) application using Qwen models hosted on Nebius, designed as a spiritual coach that combines psychological principles with Buddhist and Dzogchen teachings to help users live in the present moment, develop good habits, and work toward enlightenment.

## Overview

This project provides a foundation for a spiritual coaching application that analyzes user diary entries and provides personalized guidance by retrieving relevant teachings from authentic spiritual texts. The system combines:

- Chat completions with Qwen models on Nebius
- Embedding generation with Qwen3-Embedding-8B
- A knowledge base of spiritual teachings (Buddhist and Dzogchen traditions)
- RAG pipeline for personalized spiritual guidance
- Minimal dependencies (only `requests` and `python-dotenv`)

## Current Progress

- ✅ Fixed Nebius API integration (correct endpoint and authentication)
- ✅ Implemented chat and embedding services with proper error handling
- ✅ Created spiritual knowledge base with 15 core teachings in `spiritual_texts.json`
- ✅ Resolved all type checking issues in the codebase
- ✅ Verified all services are working correctly
- ✅ Implemented Pinecone vector store with reranking
- ✅ Built RAG service for personalized spiritual guidance
- ✅ Created comprehensive documentation
- ✅ Initialized git repository

## Setup

1. Ensure you have Python 3.7+ installed
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Nebius API key:
   ```bash
   NEBIUS_API_KEY=your_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```
5. Run the examples:

   ```bash
   # Test vector store
   python test_vector_store.py

   # Test RAG service
   python rag.py
   ```

## Components

### 1. Vector Store

- Uses Pinecone for efficient vector storage and retrieval
- Implements reranking using Qwen3-Embedding-8B model for improved relevance
- Stores 15 core spiritual teachings from Buddhist and Dzogchen traditions
- Provides similarity search for relevant teachings based on user queries

### 2. RAG Service

- Combines retrieval and generation for personalized guidance
- Uses retrieved spiritual teachings to augment chat responses
- Implements a compassionate system prompt for spiritual coaching
- Generates responses that:
  - Acknowledge the user's experience with empathy
  - Share relevant spiritual teachings
  - Offer practical advice for daily life
  - End with encouraging notes

### 3. Knowledge Base

- Contains 15 core teachings in `spiritual_texts.json`
- Covers key topics:
  - Present moment awareness
  - Impermanence and non-attachment
  - Working with difficult emotions
  - The path to enlightenment
  - Compassion and loving-kindness
  - Mindfulness practices

## Development Roadmap

### Phase 1: Simple Gradio Interface (Next Step)

The next development phase will focus on creating a simple user interface using Gradio to enable immediate user interaction. This approach prioritizes user experience and rapid feedback over complex backend systems.

**Why this order:**

1. **Faster Feedback Loop**: A simple UI allows immediate user interaction and feedback, which is invaluable for shaping the app's direction.
2. **Tangible Progress**: Users can see and interact with something real from the start, which builds confidence and engagement.
3. **Better Requirements Gathering**: By seeing how users actually interact with the app, we can make more informed decisions about what features to build next.
4. **Lower Barrier to Entry**: Gradio provides a simple, web-based interface that anyone can use without technical knowledge.

**Implementation Plan:**

- Create a basic Gradio interface with text input for diary entries
- Display the AI's spiritual guidance response
- This gives us immediate user interaction capability
- Collect user feedback to inform future development

### Phase 2: Document Upload and Processing

After establishing the basic interface, we will implement document upload functionality to expand the knowledge base.

**Implementation Plan:**

- Add PDF, DOCX, and TXT upload capabilities
- Implement text extraction from these file types
- Process and chunk the text appropriately
- Add extracted content to our knowledge base in Pinecone
- Enable users to personalize their spiritual guidance with their own texts

### Phase 3: Enhanced Analysis System

With real user interactions from the Gradio interface, we will implement a sophisticated diary analysis system.

**Implementation Plan:**

- Develop text analysis to extract emotional states, challenges, and patterns from user diary entries
- Identify key themes in user writing
- Connect psychological principles with spiritual teachings
- Implement habit tracking and goal achievement support
- All development will be informed by actual user behavior and feedback

### Phase 4: Advanced Features

After validating the core functionality with real users, we will implement advanced features.

**Implementation Plan:**

- Implement conversation memory for ongoing coaching
- Develop personalized feedback generation
- Add multi-turn dialogue support
- Create user profiles for personalized guidance
- Implement secure user authentication
- Add progress tracking for habits and mindfulness practice

## API Endpoints Used

- Chat: `/chat/completions`
- Embeddings: `/embeddings`

## Configuration

All configuration is managed through environment variables in `.env` and the `config.py` file.

## Project Context for New Sessions

This README serves as comprehensive documentation for continuing development in new AI sessions. It contains:

1. **Complete Project Overview**: The vision and purpose of the spiritual coach app
2. **Current State**: All components that have been implemented and verified
3. **Development Roadmap**: The phased approach for future development with clear reasoning for the order
4. **Technical Details**: Setup instructions, components, and configuration
5. **Decision Rationale**: Explanation of why we're prioritizing the Gradio interface first

This documentation ensures that any new AI session or developer can understand the project's current state, vision, and next steps without needing prior context.
