# JARVIS-X

**A Multimodal Autonomous Personal AI Agent with Long-Term Memory, Tool Use, Vision and Proactive Intelligence.**

## Project Vision

JARVIS-X is a long-term project to develop a personal AI assistant inspired by intelligent virtual assistants. Its goal is to combine natural language interaction, persistent memory, tool usage, multimodal capabilities, task planning, and proactive assistance into a single system.

The project is being developed incrementally, with an emphasis on modular architecture, reliability, privacy, and extensibility.

## Current Status

JARVIS-X currently supports text-based AI conversations, conversation context, and persistent long-term memory. The project is under active development.

## Current Features

- **Natural Language Conversation:** Interact with the assistant using everyday language.
- **Conversation Context:** Use recent conversation history to maintain continuity across messages.
- **Persistent Long-Term Memory:** Store selected information and retrieve relevant memories in later conversations.
- **Memory Management:** List, search, delete, and clear stored memories through supported commands.
- **Memory Extraction:** Identify potentially useful information from conversations for long-term storage.
- **Context-Aware Responses:** Combine relevant memories, recent conversation history, and system instructions when generating responses.
- **Configurable LLM Integration:** Configure the supported language model provider and model through environment variables.

## Technology Stack

- **Programming Language:** Python
- **Language Model Integration:** Groq API
- **Configuration:** Environment variables
- **Memory Storage:** JSON-based local persistence
- **Version Control:** Git and GitHub

## Project Structure

```text
JARVIS-X/
├── app/
│   ├── core/
│   │   └── jarvis.py
│   ├── llm/
│   │   └── client.py
│   └── memory/
│       ├── manager.py
│       ├── extractor.py
│       └── models.py
├── data/
│   └── memory/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The structure above describes the main project components and may evolve as development continues.*

## Configuration

JARVIS-X uses environment variables to configure its language model integration.

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | API key used to authenticate with Groq |
| `GROQ_MODEL` | Language model used by the Groq integration |
| `LLM_PROVIDER` | Selects the configured language model provider, where supported |

Sensitive credentials must remain in the local environment and must never be committed to the repository.

## Security and Limitations

- API credentials must be stored securely and excluded from version control.
- Memory is persisted locally using JSON files.
- Stored memories may contain personal information, so memory access and deletion must be handled carefully.
- Tool execution, vision, autonomous planning, proactive intelligence, and other advanced capabilities require further implementation and validation before they can be considered supported features.

## Contributing

JARVIS-X is an evolving personal AI project. Contributions, suggestions, bug reports, and architectural improvements are welcome.

Before proposing changes, ensure that the implementation is consistent with the existing architecture and that relevant functionality is tested.

## Author

**Atharva Malviya**

- GitHub: https://github.com/Atharva10807

## License

No license has been specified for this repository yet. Until a license is added, reuse and redistribution are subject to the applicable default copyright rules.

