# TaskForge

A RESTful project and task management API built with FastAPI. Supports user authentication, project ownership, task tracking with status and priority filtering, and full CRUD operations with ownership-based access control.

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT tokens (python-jose) with bcrypt password hashing
- **Validation:** Pydantic schemas for request/response models
- **Testing:** pytest with FastAPI TestClient (28 tests)

## Features

- **JWT Authentication** — Token-based auth with secure password hashing and configurable expiration
- **Ownership-Based Access Control** — Users can only access their own projects and tasks. Endpoints return 403 for unauthorized access without revealing whether a resource exists
- **Nested Resource Routing** — Tasks are created and listed under `/projects/{id}/tasks`, while individual task operations use `/tasks/{id}` to avoid requiring the project ID when it's already known
- **Partial Updates** — PUT endpoints accept optional fields, only updating what's provided
- **Query Parameter Filtering** — Filter tasks by status (`todo`, `in_progress`, `done`) and priority (`low`, `medium`, `high`)
- **Cascading Deletes** — Deleting a project automatically removes all associated tasks
- **Isolated Test Suite** — 28 tests running against an in-memory SQLite database with dependency injection overrides

## Getting Started

### Prerequisites

- Python 3.11+

### Installation

```bash
git clone https://github.com/szmathias/TaskForge.git
cd TaskForge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and update the secret key:

```bash
cp .env.example .env
```

`.env` contents:

```
DATABASE_URL=sqlite:///./tracker.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRATION_MINUTES=30
```

### Running the Server

```bash
uvicorn app.main:TaskForge --reload
```

The API will be available at `http://localhost:8000`. Interactive documentation is at `http://localhost:8000/docs`.

### Running Tests

```bash
pytest -v
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Projects (requires authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects/` | Create a new project |
| GET | `/projects/` | List all projects for current user |
| GET | `/projects/{id}` | Get a specific project |
| PUT | `/projects/{id}` | Update a project |
| DELETE | `/projects/{id}` | Delete a project and its tasks |

### Tasks (requires authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects/{project_id}/tasks/` | Create a task in a project |
| GET | `/projects/{project_id}/tasks/` | List tasks for a project (filterable by `status` and `priority`) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Project Structure

```
TaskForge/
├── app/
│   ├── main.py              # FastAPI app initialization and router registration
│   ├── config.py            # Environment-based settings via Pydantic BaseSettings
│   ├── database.py          # SQLAlchemy engine, session factory, and Base
│   ├── auth.py              # Password hashing and JWT token utilities
│   ├── dependencies.py      # get_current_user dependency for protected routes
│   ├── models/
│   │   ├── user.py          # User table with email and hashed password
│   │   ├── project.py       # Project table with owner foreign key
│   │   └── task.py          # Task table with project and assignee foreign keys
│   ├── schemas/
│   │   ├── user.py          # UserCreate, UserResponse, Token
│   │   ├── project.py       # ProjectCreate, ProjectResponse, ProjectUpdate
│   │   └── task.py          # TaskCreate, TaskResponse, TaskUpdate, enums
│   └── routers/
│       ├── auth.py          # Registration and login endpoints
│       ├── projects.py      # Project CRUD endpoints
│       └── tasks.py         # Task CRUD with nested and standalone routes
├── tests/
│   ├── conftest.py          # Test fixtures: in-memory DB, client, auth helpers
│   ├── test_auth.py         # Auth flow and access control tests
│   ├── test_projects.py     # Project CRUD and ownership isolation tests
│   └── test_tasks.py        # Task CRUD, filtering, and cross-user access tests
├── .env.example
├── requirements.txt
└── README.md
```

## Design Decisions

**FastAPI over Flask/Django** — FastAPI provides automatic request validation through Pydantic, built-in OpenAPI documentation, and native async support. For an API-only project without server-rendered templates, it's a better fit than Django's batteries-included approach or Flask's lack of built-in validation.

**SQLite for development** — Keeps the project zero-dependency for anyone cloning the repo. No database server to install or configure. The SQLAlchemy abstraction means swapping to PostgreSQL for production is a one-line configuration change.

**403 instead of 404 for unauthorized access** — When a user requests a project or task they don't own (or that doesn't exist), the API returns 403 rather than 404. This prevents information leakage — an attacker can't probe for valid resource IDs by distinguishing "exists but not yours" from "doesn't exist."

**Split task routers** — Task creation and listing are nested under `/projects/{project_id}/tasks` because those operations are naturally scoped to a project. Individual task operations (get, update, delete) use `/tasks/{id}` because the task already stores its `project_id` — requiring the caller to provide it again adds friction without adding value.

**Separate Create/Update/Response schemas** — Each operation has its own Pydantic schema. `TaskCreate` doesn't accept `id` or `created_at` (server-generated). `TaskUpdate` makes all fields optional for partial updates. `TaskResponse` includes all fields for display. This prevents clients from setting fields they shouldn't control.

**String enums for status and priority** — Stored as plain strings in the database rather than SQLAlchemy `Enum` types. This avoids migration headaches when adding new statuses — adding a value to a string column requires no schema change, while database-level enums require `ALTER TYPE` statements.

**Dependency injection for auth** — `get_current_user` chains through `OAuth2PasswordBearer` and `get_db` via FastAPI's `Depends()`. This keeps authentication logic out of route handlers and makes it trivially overridable in tests.