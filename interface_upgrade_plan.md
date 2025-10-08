# Spiritual Coach Interface Upgrade Plan

## Current Limitations

Our current Gradio interface, while functional, has several limitations:

- Basic UI with limited customization options
- No persistent user sessions or history
- Limited document management capabilities
- Minimal visual feedback and interactivity

## Proposed Upgrade: Next.js + Tailwind Interface

Based on the Pinecone namespace-notes sample app, we propose upgrading to a Next.js + Tailwind interface with the following components:

### 1. Core Architecture

```
src/
├── app/
│   ├── (workspace)/
│   │   ├── [slug]/
│   │   │   ├── (chat)/
│   │   │   │   └── Chat.tsx
│   │   │   └── page.tsx
│   │   └── workspace/
│   │       ├── new/
│   │       │   └── page.tsx
│   └── layout.tsx
├── components/
│   ├── chat/
│   │   ├── chat-message.tsx
│   │   ├── chat-message-actions.tsx
│   │   └── chat.tsx
│   └── ui/
│       ├── button.tsx
│       ├── icons.tsx
│       ├── tooltip.tsx
│       └── upload-button.tsx
└── lib/
    ├── hooks/
    │   └── workspace-chat-context.ts
    └── utils.ts
```

### 2. Key Features to Implement

#### Document Management

- Upload PDFs with drag-and-drop interface
- View uploaded documents in a card layout
- Delete documents with confirmation
- Document tray that can be expanded/collapsed

#### Chat Interface

- Persistent chat history within a workspace
- Copy message functionality
- Typing indicators
- Markdown rendering with syntax highlighting

#### Workspace Management

- Create new workspaces with custom names
- Isolate content using Pinecone namespaces
- Navigate between workspaces
- Delete workspaces with all associated documents

### 3. Implementation Steps

1. **Set up Next.js project**

```bash
npx create-next-app@latest spiritual-coach-ui
cd spiritual-coach-ui
npm install tailwindcss postcss autoprefixer --save-dev
npx tailwindcss init -p
```

2. **Create API routes for backend integration**

- `/api/chat`: Proxy to our current RAG service
- `/api/files`: Handle document uploads and management
- `/api/workspaces`: Manage workspace creation and deletion

3. **Implement core components**

- Create `Chat` component with message history
- Implement `UploadButton` for document uploads
- Build `FileCard` for document visualization
- Add `PromptGrid` for suggested prompts

4. **Integrate with existing backend**

- Update `vector_store.py` to support workspace isolation
- Modify `document_processor.py` to handle namespace-based storage
- Ensure API compatibility between frontend and backend

### 4. Benefits of This Approach

1. **Enhanced User Experience**

   - Modern, responsive interface
   - Better document visualization
   - Improved navigation and workflow

2. **Scalability**

   - Support for multiple users/workspaces
   - Better state management
   - Easier feature additions

3. **Maintainability**

   - Component-based architecture
   - Clear separation of concerns
   - Better code organization

4. **Future-Proofing**
   - Easier integration with authentication
   - Support for mobile responsiveness
   - Foundation for additional features (user profiles, analytics)

## Migration Strategy

1. Develop the new interface in parallel with the current Gradio app
2. Test thoroughly with existing document uploads
3. Deploy alongside current system for user feedback
4. Gradually migrate users to the new interface
5. Decommission Gradio interface once migration is complete

This upgrade will significantly enhance the user experience while maintaining all current functionality and preparing the application for future growth.
