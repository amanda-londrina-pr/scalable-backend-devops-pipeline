# How to Play

## Develop Life Cycle

1. Create a GitHub Issue.
2. Assign issue to me.
3. On GitHub Issue Page: create branch (feature/bugfix/release/docs/hotfix).
4. Implement changes on new branch.
5. Commit and create PR.
6. Review PR.
7. Merge on `develop` branch.

## Test

```bash
rm -rf .pytest_cache
poetry run pytest
```

## Seed

We can populate the database running:

```bash
poetry run seed 50
```

But, in development it is automaticaly during app startup.



