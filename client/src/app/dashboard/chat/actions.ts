"use server";

export async function sendMessage(message: string) {
  // Log message receipt
  console.log("Message received in server action:", message);

  try {
    // Call the backend chat API
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    // Parse the response
    const data = await response.json();

    // Return the response in the expected format
    return {
      success: data.success,
      response: data.response,
      error: data.error,
    };
  } catch (error) {
    console.error("Error calling chat API:", error);
    return {
      success: false,
      response: null,
      error: "Failed to connect to the chat service",
    };
  }
}
