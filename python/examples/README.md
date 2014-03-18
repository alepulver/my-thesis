# Examples

These simple examples serve to try different ways to program workflow steps.

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

## Case 3

- Also show warning popup when name is invalid
- Add instructions on each step (use popup widgets for everything?)
- call/return semantics
- pause/resume too?
- Allow not only next/prev, but jumping to arbitrary parts?
- Model state with a stack, and popping actions; maybe one stack per widget?
- Allow composing workflows, using them as states of another workflows

...

## Case 4

- Use generators or macros for syntactic sugar

...
