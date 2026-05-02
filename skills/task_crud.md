# Skill: Task CRUD Operations

Reusable skill for interacting with the Task management API during development and testing.

## Endpoints covered
- `POST /tasks` — create a task
- `GET /tasks` — list all tasks
- `GET /tasks/{id}` — get a specific task
- `PUT /tasks/{id}` — update a task
- `DELETE /tasks/{id}` — delete a task

## Sample payload (POST / PUT)
```json
{
  "title": "Implement login endpoint",
  "description": "Create JWT-based authentication endpoint",
  "priority": "alta",
  "effort_hours": 4.5,
  "status": "pendiente",
  "assigned_to": "dev1"
}
```

## Expected responses
- `201 Created` with the new task object on POST.
- `200 OK` with task object on GET / PUT.
- `204 No Content` on DELETE.
- `404 Not Found` when the task ID does not exist.
