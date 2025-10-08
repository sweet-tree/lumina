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

## Expanded Implementation Details

### API Routes

#### `/api/chat/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import { getRAGResponse } from "@/lib/rag-service";

export async function POST(request: NextRequest) {
  try {
    const { messages, namespaceId } = await request.json();
    const lastMessage = messages[messages.length - 1].content;

    const response = await getRAGResponse(lastMessage, namespaceId);

    return NextResponse.json({ response });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to process chat request" },
      { status: 500 }
    );
  }
}
```

#### `/api/files/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import {
  uploadDocument,
  getDocuments,
  deleteDocument,
} from "@/lib/document-service";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const namespaceId = searchParams.get("namespaceId");

    if (!namespaceId) {
      return NextResponse.json(
        { error: "namespaceId is required" },
        { status: 400 }
      );
    }

    const documents = await getDocuments(namespaceId);
    return NextResponse.json(documents);
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch documents" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const files = formData.getAll("files");
    const namespaceId = formData.get("namespaceId") as string;

    if (!files || files.length === 0) {
      return NextResponse.json({ error: "No files provided" }, { status: 400 });
    }

    const results = await Promise.all(
      Array.from(files).map((file) => uploadDocument(file, namespaceId))
    );

    return NextResponse.json({ success: true, results });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to upload files" },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const documentId = searchParams.get("documentId");
    const namespaceId = searchParams.get("namespaceId");

    if (!documentId || !namespaceId) {
      return NextResponse.json(
        { error: "documentId and namespaceId are required" },
        { status: 400 }
      );
    }

    await deleteDocument(documentId, namespaceId);
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to delete document" },
      { status: 500 }
    );
  }
}
```

### Core Components

#### `components/chat/Chat.tsx`

```tsx
"use client";
import { useChat } from "ai/react";
import { ChatMessage } from "./chat-message";
import UploadButton from "../ui/upload-button";
import { Workspace } from "@/lib/hooks/workspace-chat-context";
import { PromptGrid } from "../ui/prompt-grid";
import { ChangeEvent, useCallback, useEffect, useRef, useState } from "react";
import { Tooltip } from "../ui/tooltip";
import FileCard from "../ui/file-card";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import { FetchedFile } from "@/app/api/files/route";

const fetchFileUrls = async (workspaceId: string) => {
  try {
    const response = await fetch(`/api/files?namespaceId=${workspaceId}`);
    if (!response.ok) {
      throw new Error("Failed to fetch file URLs");
    }
    const files: FetchedFile[] = await response.json();
    return files;
  } catch (error) {
    console.error("Error fetching file URLs:", error);
    return [];
  }
};

export default function Chat({ workspace }: { workspace: Workspace }) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } =
    useChat({
      body: { namespaceId: workspace.id },
    });

  const [files, setFiles] = useState<FetchedFile[]>([]);
  const [fetchingFiles, setFetchingFiles] = useState(true);

  const [prompts, setPrompts] = useState<Prompt[]>([
    {
      id: "1",
      name: `Tell me about the content in the \"${workspace.name}\" workspace`,
      description: "",
      content: `Tell me about the content in the \"${workspace.name}\" workspace`,
      folderId: null,
    },
    {
      id: "2",
      name: `Give me some quotes about \"${workspace.name}\" from the content.`,
      description: "",
      content: `Give me some quotes about \"${workspace.name}\" from the content.`,
      folderId: null,
    },
    {
      id: "3",
      name: `Write me an essay about \"${workspace.name}\" from the content.`,
      description: "",
      content: `Write me an essay about \"${workspace.name}\" from the content.`,
      folderId: null,
    },
    {
      id: "4",
      name: `Tell me something I might not know about \"${workspace.name}\"`,
      description: "",
      content: `Tell me something I might not know about \"${workspace.name}\"`,
      folderId: null,
    },
  ]);

  const [activePromptIndex, setActivePromptIndex] = useState<number>(0);
  const promptListRef = useRef<HTMLDivElement | null>(null);

  const [shouldSubmit, setShouldSubmit] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const handlePromptSubmit = (prompt: Prompt) => {
    handleInputChange({
      target: { value: prompt.content },
    } as ChangeEvent<HTMLInputElement>);
    setShouldSubmit(true);
  };

  useEffect(() => {
    if (shouldSubmit) {
      const form = document.querySelector("form");
      if (form) {
        form.dispatchEvent(new Event("submit", { cancelable: true }));
        form.requestSubmit();
        setShouldSubmit(false);
      }
    }
  }, [shouldSubmit]);

  const handleDeleteFile = async (documentId: string) => {
    console.log(
      `/api/files?documentId=${documentId}&namespaceId=${workspace.id}`
    );
    try {
      const response = await fetch(
        `/api/files?documentId=${documentId}&namespaceId=${workspace.id}`,
        {
          method: "DELETE",
        }
      );
      const responseData = await response.json();
      console.log(responseData.message);
      fetchFiles();
    } catch (error) {
      console.error("Error deleting file:", error);
    }
  };

  const [documentTrayIsOpen, setDocumentTrayIsOpen] = useState(false);

  const toggleOpen = () => {
    setDocumentTrayIsOpen(!documentTrayIsOpen);
  };

  const fetchFiles = useCallback(async () => {
    setFetchingFiles(true);
    const files = await fetchFileUrls(workspace.id);
    setFiles(files);
    setFetchingFiles(false);
  }, [workspace.id]);

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  useEffect(() => {
    if (documentTrayIsOpen) {
      fetchFiles();
    }
  }, [documentTrayIsOpen, fetchFiles]);

  return (
    <div className="relative flex flex-col w-full max-w-md md:max-w-2xl h-full py-24 items-center justify-start">
      <div className={messages.length > 0 ? "h-full w-full" : "w-full"}>
        {messages.map((m) => (
          <div key={m.id} className={"whitespace-pre-wrap max-w-fit w-full"}>
            <ChatMessage key={m.id} message={m} />
          </div>
        ))}
        {isLoading && (
          <div className="animate-pulse bg-gray-500 h-4 w-4 rotate-45 rounded-sm"></div>
        )}
        <div className={documentTrayIsOpen ? "h-[70%]" : "h-1/3"}></div>
      </div>

      {messages.length === 0 && (
        <div className="relative flex flex-col items-center justify-center h-full">
          {!fetchingFiles &&
            (files.length > 0 ? (
              <PromptGrid
                prompts={prompts}
                activePromptIndex={activePromptIndex}
                onMouseOver={(index: number) => setActivePromptIndex(index)}
                promptListRef={promptListRef}
                handleSubmit={handlePromptSubmit}
              />
            ) : (
              <div className="text-gray-500 text-sm">
                {workspace.name === "Empty Workspace"
                  ? 'This is an example workspace with no uploaded documents for context. Try ask a question about "Richard Feynman" or any other workspace.'
                  : "No documents in this workspace... upload below!"}
              </div>
            ))}
        </div>
      )}

      <form
        onSubmit={(e: React.FormEvent<HTMLFormElement>) => handleSubmit(e)}
        className="fixed bottom-0 w-full max-w-[300px] sm:max-w-[400px] md:max-w-2xl z-50 pb-10"
      >
        <div className="flex flex-row items-center h-fit mb-4">
          <textarea
            className={
              "p-4 px-5 border border-gray-300 bg-white/80 text-black rounded flex-grow mr-4 backdrop-blur-lg shadow-md overflow-y-auto resize-none " +
              (isLoading ? "cursor-not-allowed" : "cursor-text")
            }
            value={input}
            placeholder={
              isLoading ? "Responding..." : "Chat with this workspace..."
            }
            disabled={isLoading}
            onChange={handleInputChange}
            onKeyDown={(e: any) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            rows={1}
            style={{
              height: "auto",
              maxHeight: "30vh",
              overflow: "auto",
              scrollbarColor: "transparent transparent",
            }}
            ref={(textarea) => {
              if (textarea) {
                textarea.style.height = "auto";
                textarea.style.height = `${Math.min(
                  textarea.scrollHeight,
                  window.innerHeight * 0.3
                )}px`;
                if (!isFocused) {
                  textarea.focus();
                  setIsFocused(true);
                }
              }
            }}
          />
          <div className="flex-shrink-0 relative">
            <Tooltip
              text={
                workspace.locked
                  ? "Read-Only Workspace"
                  : "Add PDF documents (do not upload private files)"
              }
              position="top"
            >
              <UploadButton
                workspaceId={workspace.id}
                uploadCompletionCallback={fetchFiles}
                locked={workspace.locked ?? false}
              />
            </Tooltip>
          </div>
        </div>

        {/* Document Tray */}
        <div className="flex flex-col items-center bg-white/80 backdrop-blur-lg border border-gray-300 rounded shadow-md">
          <button
            onClick={toggleOpen}
            className={`flex flex-row items-center justify-center font-normal cursor-pointer w-full p-2 gap-1 transition duration-200 ease-in-out hover:bg-slate-50 border-b`}
          >
            <span className="text-gray-500 text-sm">
              {workspace.locked ? "View Documents" : "Manage Documents"}{" "}
              {fetchingFiles ? (
                <>
                  (
                  <div className="inline-block w-2 h-4 mx-0 translate-y-1 bg-gray-200 animate-pulse" />

                  )
                </>
              ) : (
                `(${files.length})`
              )}
            </span>
            <div className={"-rotate-90 text-gray-500 scale-105"}>
              {documentTrayIsOpen ? <FiChevronRight /> : <FiChevronLeft />}
            </div>
          </button>
          {documentTrayIsOpen && (
            <div className="p-2 py-5 max-h-[120px] overflow-auto no-scrollbar">
              {files.length > 0 ? (
                <div className="flex flex-wrap gap-x-2 gap-y-5 ">
                  {files.map((file) => (
                    <FileCard
                      key={file.name}
                      fileUrl={file.url}
                      handleDeleteFile={() => handleDeleteFile(file.documentId)}
                      readOnly={workspace.locked}
                    />
                  ))}
                </div>
              ) : fetchingFiles ? (
                <div className="text-gray-500 text-sm animate-pulse">
                  Fetching documents...
                </div>
              ) : (
                <div className="text-gray-500 text-sm">
                  No documents uploaded
                </div>
              )}
            </div>
          )}
        </div>
      </form>
    </div>
  );
}

/**
 * Extracts the documentId from a given file URL.
 * Assumes the URL pattern is:
 * https://domain/[namespaceId]/[documentId]/[filename]
 *
 * @param fileUrl - The URL of the file from which to extract the documentId.
 * @returns The extracted documentId or an empty string if the URL is invalid.
 */
export function getDocumentIdFromFileUrl(fileUrl: string): string {
  try {
    // Parsing the URL to get the pathname
    const url = new URL(fileUrl);
    const pathSegments = url.pathname
      .split("/")
      .filter((part) => part.trim() !== "");

    // Assuming the documentId is always the second segment in the path
    const documentId = pathSegments[1]; // 0: namespaceId, 1: documentId, 2: filename
    return documentId;
  } catch (error) {
    console.error("Error extracting documentId from URL:", error);
    return "";
  }
}
```

#### `components/chat/chat-message.tsx`

```tsx
// Inspired by Chatbot-UI and modified to fit the needs of this project
// @see https://github.com/mckaywrigley/chatbot-ui/blob/main/components/Chat/ChatMessage.tsx

import { Message } from "ai";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { cn } from "@/lib/utils";
import { CodeBlock } from "@/components/ui/codeblock";
import { MemoizedReactMarkdown } from "@/components/ui/markdown";
import { IconPinecone, IconUser } from "@/components/ui/icons";
import { ChatMessageActions } from "@/components/chat/chat-message-actions";

export interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message, ...props }: ChatMessageProps) {
  return (
    <div
      className={cn("group relative mb-4 flex items-start md:-ml-12 py-5")}
      {...props}
    >
      <div
        className={cn(
          "flex size-6 shrink-0 select-none items-center justify-center rounded-md",
          message.role === "user"
            ? "bg-background "
            : "bg-primary text-primary-foreground"
        )}
      >
        {message.role === "user" ? (
          <IconUser className="size-6 text-black" />
        ) : (
          <IconPinecone />
        )}
      </div>
      <div className="flex-1 px-1 ml-4 space-y-2 overflow-visible">
        <MemoizedReactMarkdown
          className="prose break-words prose-p:leading-relaxed prose-pre:p-0 text-black"
          remarkPlugins={[remarkGfm, remarkMath]}
          components={{
            p({ children }) {
              return <p className="mb-0 last:mb-0">{children}</p>;
            },
            li({ children }) {
              return (
                <li className="max-h-fit ml-3 mb-3 max-w-2xl">{children}</li>
              );
            },
            ul({ children }) {
              return (
                <ul className="!list-disc max-h-fit !whitespace-normal">
                  {children}
                </ul>
              );
            },
            ol({ children }) {
              return (
                <ol className="!list-decimal max-h-fit !whitespace-normal">
                  {children}
                </ol>
              );
            },
            a({ node, className, children, ...props }) {
              return (
                <a
                  className="text-blue-600 hover:underline font-bold"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                >
                  {children}
                </a>
              );
            },
            code({ node, inline, className, children, ...props }) {
              if (children.length) {
                if (children[0] == "▍") {
                  return (
                    <span className="mt-1 cursor-default animate-pulse">▍</span>
                  );
                }

                children[0] = (children[0] as string).replace("`▍`", "▍");
              }

              const match = /language-(\w+)/.exec(className || "");

              if (inline) {
                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              }

              return (
                <CodeBlock
                  key={Math.random()}
                  language={(match && match[1]) || ""}
                  value={String(children).replace(/\n$/, "")}
                  {...props}
                />
              );
            },
          }}
        >
          {message.content}
        </MemoizedReactMarkdown>
        <ChatMessageActions message={message} />
      </div>
    </div>
  );
}
```

#### `components/chat/chat-message-actions.tsx`

```tsx
"use client";

import { type Message } from "ai";

import { Button } from "@/components/ui/button";
import { IconCheck, IconCopy } from "@/components/ui/icons";
import { useCopyToClipboard } from "@/lib/hooks/use-copy-to-clipboard";
import { cn } from "@/lib/utils";

interface ChatMessageActionsProps extends React.ComponentProps<"div"> {
  message: Message;
}

export function ChatMessageActions({
  message,
  className,
  ...props
}: ChatMessageActionsProps) {
  const { isCopied, copyToClipboard } = useCopyToClipboard({ timeout: 2000 });

  const onCopy = () => {
    if (isCopied) return;
    copyToClipboard(message.content);
  };

  return (
    <div
      className={cn(
        "flex items-center justify-end transition-opacity group-hover:opacity-100 md:absolute md:-right-10 md:-top-2 md:opacity-0",
        className
      )}
      {...props}
    >
      <Button variant="ghost" size="icon" onClick={onCopy}>
        {isCopied ? <IconCheck /> : <IconCopy />}
        <span className="sr-only">Copy message</span>
      </Button>
    </div>
  );
}
```

#### `lib/utils.ts`

```ts
import clsx, { ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

#### `lib/hooks/use-copy-to-clipboard.ts`

```ts
import { useCallback, useState } from "react";

export function useCopyToClipboard({ timeout = 2000 } = {}) {
  const [isCopied, setIsCopied] = useState(false);

  const copyToClipboard = useCallback(
    (value: string) => {
      navigator.clipboard
        .writeText(value)
        .then(() => {
          setIsCopied(true);

          setTimeout(() => {
            setIsCopied(false);
          }, timeout);
        })
        .catch((error) => {
          console.error("Failed to copy to clipboard:", error);
        });
    },
    [timeout]
  );

  return {
    isCopied,
    copyToClipboard,
  };
}
```

### Backend Integration

#### `lib/rag-service.ts`

```ts
import axios from "axios";

export async function getRAGResponse(
  query: string,
  namespaceId: string
): Promise<string> {
  try {
    const response = await axios.post("/api/rag", {
      query,
      namespaceId,
    });
    return response.data.response;
  } catch (error) {
    console.error("Error getting RAG response:", error);
    return "I apologize, but I encountered an error while processing your request. Please try again.";
  }
}
```

#### `lib/document-service.ts`

```ts
import axios from "axios";

export async function uploadDocument(
  file: File,
  namespaceId: string
): Promise<any> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("namespaceId", namespaceId);

  try {
    const response = await axios.post("/api/files", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading document:", error);
    throw error;
  }
}

export async function getDocuments(
  namespaceId: string
): Promise<FetchedFile[]> {
  try {
    const response = await axios.get(`/api/files?namespaceId=${namespaceId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching documents:", error);
    return [];
  }
}

export async function deleteDocument(
  documentId: string,
  namespaceId: string
): Promise<void> {
  try {
    await axios.delete(
      `/api/files?documentId=${documentId}&namespaceId=${namespaceId}`
    );
  } catch (error) {
    console.error("Error deleting document:", error);
    throw error;
  }
}
```

### Migration Strategy

1. Develop the new interface in parallel with the current Gradio app
2. Test thoroughly with existing document uploads
3. Deploy alongside current system for user feedback
4. Gradually migrate users to the new interface
5. Decommission Gradio interface once migration is complete

This upgrade will significantly enhance the user experience while maintaining all current functionality and preparing the application for future growth.
