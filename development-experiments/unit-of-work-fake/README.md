## Purpose of Experiment

The purpose of this experiment is to establish a pattern for making fake repository based unit of work implementations with the transaction behavior that tested code relies on.

- It is common to see an in-memory database implementation of a repository without any transaction logic. 
- It is not common to see a fake implementation of a unit of work for testing, instead other communities which use clean architecture either rely on some form of integration tests with a real database (testcontainers) or an in memory sqlite with their object relational mapper.
- This experiment aims to make an in-memory database for plain old python objects, that we can build unit of work/repository implementations on top of.
  - It will support loading stored entities as part of a transaction, modifying them, and commiting changes atomically.

### Progress (fake database)
- Updating entity only in transaction prior to commit.
  - A transaction can be started, an entity loaded, and modified and the original will not be updated until commit.
- Updating entity after transaction commited
  - The entity will be updated after a transaction which has modified a copy has been commited.
- Adding new entities to the database on transaction commit
  - An entity can be added to a transaction and on commit will be added to the database.

### Architecture Notes
- Updating entities is based on their identification. A callable can be provided to use on the entity to get an identifier for it. When changes are merged, the entity matching the id of the one in the merge will be replaced.
