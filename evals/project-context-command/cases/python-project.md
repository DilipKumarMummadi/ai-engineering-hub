# Scenario

Generate context in a Python project.

# Input

/context generate

# Context

A git repository with `pyproject.toml` (FastAPI, SQLAlchemy, pytest) and `app/main.py`.

# Expected Behavior

The context records Python, FastAPI, SQLAlchemy and pytest, marks HTTP service behavior as Inferred from the framework, and leaves the database engine Unknown unless evidence names one.

# Important Checks

- Inference is marked as such.
- The database engine is not guessed from SQLAlchemy alone.

# Failure Conditions

- Naming PostgreSQL without evidence.
- Presenting inferred behavior as fact.

# Notes

Checks inference discipline on a non-.NET stack.
