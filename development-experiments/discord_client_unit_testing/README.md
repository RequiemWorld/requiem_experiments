## Purpose of Experiment
The purpose of this experiment which is not necessarily going to be concluded is to develop a small discord bot or client class and test the correctness of the API/Gateway communication logic through fakes.

- The first abstraction choice is: sending and receiving gateway events to a gateway which can be connected and disconnected from.
- The second abstraction choice is: sending and getting data to the discord API as required e.g. ``get_own_user`` and ``get_other_user``.
- The fake api and gateway can act as fake implementations of discord that allow verification of actions and sending specific responses.


### Design Emphasis
- There is an emphasis to be placed on the choice of using fakes. By injecting groups of objects that can be collaborated with like the real thing, we can test as though we are giving it a real discord, and inspecting the state afterward.
- There is too much going on and required to work for stubbing to be a reasonable option, and spying on interactions/confirming them alone isn't enough.
- This requires hand-writing fake implementations of the collaborating classes. The complexity and needs for testing will increase and if care is not taken it could become unmaintainable. Experiments like this one should help us get a feel for writing fakes, and establishing patterns to do stuff in non-error prone ways.

