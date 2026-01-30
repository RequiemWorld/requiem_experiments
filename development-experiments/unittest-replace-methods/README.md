## Purpose of Experiment

Create TestCase classes which replace the test methods on the classes which inherit them.

## Discovery 1 -> Custom Failure is viable
- It is possible to replace a method with another and make it call the original and fail. This should be able to be used to create test case classes for performance testing which can use the code in the body of the method as what to measure.

## Discovery 2 -> pycharm debugging after replacement
- In pycharm after a method has been replaced with another which calls it, it is still possible to set breakpoints on the original for debugging. [\[1\]](https://ibb.co/0RCY5Pn9)