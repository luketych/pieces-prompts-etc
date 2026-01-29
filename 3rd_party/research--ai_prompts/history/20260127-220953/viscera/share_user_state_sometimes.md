---
source: https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents
---

Consider the user’s perspective, and try aligning the model with that perspective.


💡Note: This is not to suggest that one of these prompts is necessarily better than the other. The potential downside of the detailed prompt is that the model might start paying too much attention to the IDE state, which isn’t always the best signal for what the user is trying to do.


Example: When the user works in the IDE, the model can be presented with a detailed view of the IDE state, focusing on the elements the user is most likely to care about, or refer to in their instructions.

Examples of things that can potentially help align the model:

* The user’s current time and timezone
* The user’s current location
* The user’s activity history


Example of a basic system prompt that includes IDE state:

```
The user works in an IDE. The current IDE state:

The file foo.py is open.
The IDE is of type VSCode.
```


Example of a more detailed system prompt that describes the IDE state:

```
The user works in an IDE. The current IDE state:

The IDE is of type VSCode.

The currently open file is foo.py.
Lines 134 through 179 are visible on the screen.
Here is the currently visible text, with the cursor location denoted by <CURSOR>:

```python
134  def bar():
135    print("hell<CURSOR>o")
...
179  # TODO implement this
```

There is no selected text.
There are 14 open tabs. Here they are from most recently to last recently visited:
foo.py
bar.py ...
xyz.py
```
