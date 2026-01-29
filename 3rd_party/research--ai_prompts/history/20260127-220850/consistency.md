---
source: https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents
---

Example:

* The system prompt includes the line The current directory is $CWD

* The execute_command tool, which allows the agent to execute shell commands, includes an optional cwd parameter. Consistency implies that the default value of this parameter should be $CWD. This can be specified in the tool definition. If it is not, the model will likely assume that is the case.

* The read_file tool accepts a path parameter of the file to read. If supplied with a relative path, it should be interpreted as being relative to $CWD.


💡 Note: Avoid surprising the model. Models are easily confused. If the model is likely to expect a certain outcome from a tool call, make sure to either provide that outcome, or explain the deviation in the tool result. For example, if the tool definition promises to return an output of a certain length, either return output of that length, or preface the answer with a statement like Output of length N was requested, but returning output of length K instead because ...


Example:

* If the prompt contains state that may change during a session (e.g. the current time), do not include them in the system prompt or in tool definitions
* Instead, tell the model about the change in the next user message. This keeps the prompt internally consistent: the model can see what the state was at each turn.

