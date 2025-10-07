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

## Future Extension Plan

### 1. Diary Analysis System

- Develop text analysis for user diary entries
- Identify emotional states, challenges, and patterns in user writing
- Connect psychological principles with spiritual teachings
- Implement habit tracking and goal achievement support

### 2. User Interface

- Create web interface for diary entry and coaching
- Implement secure user authentication
- Add progress tracking for habits and mindfulness practice
- Design intuitive interface for receiving guidance

### 3. Advanced RAG Features

- Implement conversation memory for ongoing coaching
- Develop personalized feedback generation
- Add multi-turn dialogue support
- Create user profile for personalized guidance

## API Endpoints Used

- Chat: `/chat/completions`
- Embeddings: `/embeddings`

## Configuration

All configuration is managed through environment variables in `.env` and the `config.py` file.
