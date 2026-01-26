document.addEventListener("DOMContentLoaded", async () => {
  const titleInput = document.getElementById("title");
  const urlInput = document.getElementById("url");
  const notesInput = document.getElementById("notes");
  const saveBtn = document.getElementById("saveBtn");
  const statusDiv = document.getElementById("status");

  // Get current tab info
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab) {
    titleInput.value = tab.title || "";
    urlInput.value = tab.url || "";
  }

  saveBtn.addEventListener("click", async () => {
    const title = titleInput.value;
    const url = urlInput.value;
    const notes = notesInput.value;

    if (!url) {
      showStatus("Error: No URL found", "error");
      return;
    }

    saveBtn.disabled = true;
    saveBtn.textContent = "Sending...";
    showStatus("", "");

    // Construct formatting for Deckard
    // We'll format it as markdown so the agent understands it's a saved link
    let textContent = `Saved Link: [${title}](${url})`;
    if (notes) {
      textContent += `\n\nUser Notes: ${notes}`;
    }

    try {
      const response = await fetch("http://localhost:8000/api/ingest/text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: textContent,
        }),
      });

      if (response.ok) {
        showStatus("Saved to Deckard!", "success");
        setTimeout(() => window.close(), 1500);
      } else {
        const errorData = await response.json();
        showStatus(
          `Error: ${errorData.detail || response.statusText}`,
          "error",
        );
        saveBtn.disabled = false;
        saveBtn.textContent = "Send to Deckard";
      }
    } catch (error) {
      console.error(error);
      showStatus("Connection failed. Is Deckard running?", "error");
      saveBtn.disabled = false;
      saveBtn.textContent = "Send to Deckard";
    }
  });

  function showStatus(msg, type) {
    statusDiv.textContent = msg;
    statusDiv.className = "status " + type;
  }
});
