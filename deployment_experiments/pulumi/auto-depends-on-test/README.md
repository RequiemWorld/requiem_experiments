

## Discovery 1 - UpResult.summary.resource_changes won't be empty when no changes have been made
- Issue Encountered: I found the summary.resource_changes when going through what was available in PyCharm. I assumed that it would be empty when no changes were made. The condition which was meant to execute when there were changes happened when there were no changes and showed {'same': 3}. [\[\1\]](https://ibb.co/DDMTwz4Q)
- Lesson Learned/Observation: The resource changes dictionary contains a mapping of the type of change and how many occurred i.e., how many resources created, how many remain the same, etc. [\[1\]](https://ibb.co/DDMTwz4Q)
- Preferred Solution: Add a helper function to check if there are any changes to resources based on if same is exclusively in the dictionary and not **anything** else including strings not part of the OpType enum.

## Discovery 2 - The type used in UpResult.summary.resource_changes is an pulumi.automation.events.OpType 
- Lesson Learned/Observation: All the available operations that apply to resources can be found under it. This may be useful for determining if any changes have occurred in a more meaningful way than if exclusively "same" is in the result. [\[1\]](https://ibb.co/KzqbccBB)
