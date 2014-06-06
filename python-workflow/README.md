# Workflow examples

These simple examples serve to try different ways to program workflow steps.

They use the same libraries as the Python version, so see [python-circles](../python-circles) for installation instructions.

## Case 1

- Ask for 3 names
- Display them
- Prompt to exit

In the "simple" implementation, communication is done by shared variables among the closures used as callbacks.
But in the "workflow" version there are 2 choices: passing input as constructor arguments (only input), or using a dictionary shared among steps.
The variable names in this case are constant for each step class, but should be configurable as well as other things (like title).

## Case 2

- Ask for 3 names, with a custom rejection function
- Display them, allowing to enter them again if not satisfied
- Prompt to exit

Similar to the previous one, but added the ability to go to the previous step in the workflow.
The decision of when to do so is still in the step's logic, not configurable.

## Case 2.5

- Encapsulate the logic with the State Pattern

Each method represents a different entry point, using instance variables for communication. Note that branching and looping constructs have to be simulated by setting the next state (using native language constructs inside the entry points). Also states have a start method, but they can only return by starting another one.

## Case 3

- Move the logic to a handler

Storage was removed from workflow, as it's kept inside the steps and returned to the handler, which in turn passes it to the next steps.
Control flow is managed from a handler function, and it's hard to follow because there is a single entry point.

## Case 4

- Use generators to pause and resume the handler

Generators make the handler function easier to read and modify, as we can use if/while constructs as in normal code.
This is because of the multiple entry points (one for each `yield` statement).

# Composing workflows

## Case 5

- Use coroutines (stackless) to avoid `yield from` in previous

...
