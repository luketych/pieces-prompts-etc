---
source: https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents
---

# Be aware of prompt caching


Whenever possible, build your prompts such that they will be appended to during a session in order to avoid invalidating the prompt cache.


Example:

* If the prompt contains state that may change during a session (e.g. the current time), do not include them in the system prompt or in tool definitions, because once they change most of the prompt cache will be invalidated.


Instead, tell the model about the change in the next user message.
