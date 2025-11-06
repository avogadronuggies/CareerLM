// Utility function for formatting AI-generated text with proper markdown handling

export const formatText = (text) => {
  if (!text) return "";

  // Make sure text is a string
  const textStr = typeof text === "string" ? text : String(text);

  // Replace numbered points with proper formatting
  let formatted = textStr.replace(/(\d+)\.\s+/g, "\n\n<strong>$1.</strong> ");

  // Replace bold markers with HTML bold tags
  formatted = formatted.replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>");

  // Replace section headers (text followed by colon)
  formatted = formatted.replace(/\n([A-Z][^:\n]+):/g, "\n<strong>$1:</strong>");

  // Replace bullet points
  formatted = formatted.replace(/\*\s+([^\n]+)/g, "<br/>• $1");
  formatted = formatted.replace(/•\s+([^\n]+)/g, "<br/>• $1");
  formatted = formatted.replace(/-\s+([^\n]+)/g, "<br/>• $1");

  // Add line breaks for better readability
  formatted = formatted.replace(/\n/g, "<br/>");

  // Handle multiple line breaks (collapse into double)
  formatted = formatted.replace(/(<br\/>){3,}/g, "<br/><br/>");

  // Clean up leading line breaks
  formatted = formatted.replace(/^(<br\/>)+/, "");

  return formatted;
};

export const formatAIAnalysis = (analysis) => {
  if (!analysis) return null;

  // Make sure analysis is a string
  const analysisText =
    typeof analysis === "string" ? analysis : JSON.stringify(analysis);

  // Try to extract numbered points with full descriptions
  const fullSuggestionRegex = /(\d+)\.\s+\*\*([^*]+)\*\*([\s\S]*?)(?=\d+\.|$)/g;
  let fullMatches = [...analysisText.matchAll(fullSuggestionRegex)];

  if (fullMatches.length > 0) {
    return fullMatches.map((match, index) => {
      const title = match[2].trim();
      const description = match[3].trim();

      return {
        title,
        description: formatText(description),
      };
    });
  }

  // Fallback to simple numbered list
  const numberedListRegex = /^\d+\.\s+(.+)$/gm;
  let matches = [...analysisText.matchAll(numberedListRegex)];

  if (matches.length > 0) {
    return matches.map((match) => ({
      title: null,
      description: formatText(match[1]),
    }));
  }

  // If no structured format found, return as formatted paragraphs
  const paragraphs = analysisText
    .split("\n\n")
    .filter((p) => p.trim().length > 0);

  if (paragraphs.length > 0) {
    return paragraphs.map((p) => ({
      title: null,
      description: formatText(p),
    }));
  }

  // Last resort - just format the whole text
  return [
    {
      title: null,
      description: formatText(analysisText),
    },
  ];
};

export const cleanMarkdown = (text) => {
  if (!text) return "";

  // Remove markdown formatting for plain text display
  return text
    .replace(/\*\*/g, "")
    .replace(/\*/g, "")
    .replace(/#+\s/g, "")
    .trim();
};
