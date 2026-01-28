---
name: voice-to-slack
description: Converts stream-of-consciousness voice transcripts into structured, Slack-ready messages with multiple variants. Use when the user asks to write a Slack message, convert text to Slack format, make something Slack-ready, help with Slack messaging, or transform a transcript into a Slack post.
---

# Voice-to-Slack Transformer

Converts raw, unstructured voice transcripts (stream-of-consciousness thoughts) into clear, structured, Slack-ready messages. Generates three distinct message variants so you can choose the best framing.

## When to Use

Activate this skill when the user explicitly requests:
- "Help me write a Slack message"
- "Convert this to Slack"
- "Make this Slack-ready"
- "Transform this transcript into a Slack message"
- "Help me format this for Slack"

**Do NOT activate automatically** just because a transcript is present - only when explicitly requested.

## Core Process

1. **Interpret the transcript** - Infer what the user is really trying to communicate
   - Identify intent: update, reflection, question, or request
   - Determine core message and key supporting points
   - Omit tangents or self-corrections unless contextually important

2. **Organize the message**
   - Auto-generate a relevant title with emoji (e.g., 🧠 Reflection, 🔍 Question, ✅ Update, ❓ Request)
   - Start with a one-liner TL;DR summarizing the essence or intent
   - Follow with a Details section that's structured and scannable

3. **Generate 3 distinct variants**
   - Each variant should use a different framing style:
     - **Variant A**: Concise summary / high signal
     - **Variant B**: Balanced and explanatory
     - **Variant C**: Reflective or narrative
   - Vary sentence structure, layout, and emphasis for meaningful choice
   - Examples of different framings: Pros/Cons/Next Steps, Headline + Narrative, Key Takeaways + Open Questions, Data/Strategy/Risk

4. **Flag ambiguities** - If meaning is unclear, summarize what's certain and flag what needs clarification

## Output Format

For each variant:

```
[Emoji] [Auto-generated title]
[1-sentence summary of the main point, intent, or ask]

Details
• Topic: [short phrase or idea]
• [additional points, actions, or reflections]
```

Separate variants with `---`

## Formatting Guidelines

- Use Slack-compatible Markdown (bold, italics, bullet points, line breaks)
- Use emojis sparingly and intentionally for readability and tone
- Maintain whitespace for easy reading on Slack mobile and desktop
- Preserve the user's natural tone while removing filler, hesitation, and redundancy
- Adapt length and structure dynamically based on content and intent

## Context Handling

- If provided with historical Slack context (previous messages or threads), use it implicitly to maintain coherence and avoid redundancy
- Don't explicitly reference context unless the user's intent clearly requires it
- If context seems missing but required, suggest what could help

## Quality Standards

- **Clarity**: Every message should be instantly scannable
- **Brevity**: Prioritize signal over comprehensiveness
- **Tone**: Consistent with user's natural voice
- **Variants**: Each meaningfully distinct in framing (not just rewrites)

## Error Handling

- If transcript is unclear or fragmented: summarize what's certain and flag ambiguities
- Never fabricate content; infer only within reason
- If context is missing but seems required: suggest what could help

## Safety

- Never include private or sensitive information unless explicitly provided
- Respect confidentiality and tone appropriateness for workplace contexts
- Avoid speculation or personal attribution unless clearly in the source
