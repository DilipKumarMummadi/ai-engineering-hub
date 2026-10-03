# Scenario

A team is adding a task tracking feature to an ASP.NET Core API that serves a React and TypeScript front end. They need an API design before implementation.

# Input

Please design the API for project tasks. Include the endpoints, request and response models, validation, errors and security.

# Context

Requirements:

- A user belongs to one or more organizations. A project belongs to one organization. A task belongs to one project.
- Users can list the tasks in a project, filtered by status (`open`, `in_progress`, `done`) and by assignee, sorted by due date or creation date.
- A project can have thousands of tasks.
- Users can create a task (title required, up to 200 characters; optional description, assignee and due date), change its title, description, assignee or due date, change its status, and delete it.
- Only members of the project's organization can see its tasks. Only organization admins or the task's assignee can change a task's status. Only admins can delete tasks.
- The API uses JWT bearer authentication already. Existing endpoints in the project return JSON with camelCase properties and use URL paths like `/projects/{projectId}/members`.
- The front end needs the assignee's display name in the task list.
- Task data is stored with EF Core in PostgreSQL. The `Task` entity has an internal `RowVersion` and a `CreatedByUserId`.

# Expected Behavior

The response models tasks as a resource under projects, consistent with the existing path style, and defines operations with appropriate methods and status codes: list, create, read, partial update, status change and delete. It covers list behavior with filtering, sorting and pagination with bounded page size, and stable ordering. It uses separate request and response models (not the EF entity), excluding internal fields such as `RowVersion` and `CreatedByUserId` unless intended, and includes the assignee display name in the list response. It defines validation (title required and max 200 characters, allowed status values, valid dates and assignees) with 400 responses in one consistent error format. It separates authentication from authorization: non-members get 403 or 404 (and explains the choice), only admins or the assignee can change status, only admins can delete, and object-level checks are made against the project's organization and not only the route. It considers concurrent edits (optimistic concurrency), the documented OpenAPI contract, and testing the authorization rules. It lists open questions, for example whether deleted tasks must be recoverable, or how to treat changing status to the same value.

# Important Checks

- Resources and URLs are consistent with the existing style, and operations use correct methods.
- Status codes are specific and correct for each case (201, 204, 400, 401, 403 or 404, 409 or 412).
- Pagination and filtering are defined for a large collection, with limits.
- The entity is not exposed. Internal fields are kept out.
- The assignee display name requirement is handled.
- Authentication and authorization are treated separately, and object-level authorization is covered.
- The error format is consistent.
- Concurrency and compatibility (new API, so OpenAPI documentation) are considered.
- Open questions are listed, not invented answers.

# Failure Conditions

- Verb-based or inconsistent URLs that ignore the existing style, with incorrect methods (for example GET to change state).
- Returning the EF entity or internal fields.
- No pagination for a list that can be thousands of items.
- Treating a valid token as sufficient permission.
- Checking authorization only on the project route and not for the task's own access.
- Using 200 for errors or 500 for validation failures.
- Ignoring the permission differences between status change and delete.
- Proposing a different protocol or framework without a stated reason.
- Inventing requirements that are not in the context.

# Notes

Several URL and payload designs are acceptable, for example `PATCH` for status or a sub-resource for status transitions. Judge consistency and reasoning. Either 403 or 404 for non-members is acceptable if the trade-off is explained.
