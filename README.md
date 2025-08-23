# Python FastAPI Starter

- [Python FastAPI Starter](#python-fastapi-starter)
  - [Overview](#overview)
  - [Project Structure](#project-structure)
  - [Scripts](#scripts)
  - [Setup](#setup)
  - [Environment Variables](#environment-variables)
    - [Files](#files)
  - [Running the API](#running-the-api)
    - [With Docker Compose](#with-docker-compose)
    - [Locally (Uvicorn)](#locally-uvicorn)
    - [In VS Code](#in-vs-code)
  - [Testing](#testing)
    - [Run all tests](#run-all-tests)
    - [Run tests in a group/file](#run-tests-in-a-groupfile)
    - [Run a single test](#run-a-single-test)
  - [Passing Arguments to Poetry Scripts](#passing-arguments-to-poetry-scripts)
  - [Linting \& Formatting](#linting--formatting)
  - [Releasing](#releasing)
  - [Git Hooks](#git-hooks)
  - [Database](#database)
    - [Initialization](#initialization)
    - [Wiping the Database and Starting Fresh](#wiping-the-database-and-starting-fresh)
  - [Debugging](#debugging)
    - [Debugging in VS Code](#debugging-in-vs-code)
    - [Debugging in Terminal (poetry run start)](#debugging-in-terminal-poetry-run-start)
    - [Debugging in Docker/Docker Compose](#debugging-in-dockerdocker-compose)
  - [Anything Else?](#anything-else)
  - [Contributing](#contributing)
  - [NGINX Security Configuration](#nginx-security-configuration)

## Overview 

A starter template for building FastAPI applications with Poetry, Docker, semantic-release, lefthook, and VS Code integration.

## Project Structure

- `src/python_fastapi_starter/cli.py` — CLI utilities and entry points
- `src/python_fastapi_starter/api/` — FastAPI app code (main.py, routers, models, etc.)
- `tests/` — Pytest test files
- `db/schema.sql` — Database schema
- `db/seed.sql` — Seed data
- `.github/workflows/` — CI/CD workflows
- `Dockerfile` & `docker-compose.yaml` — Containerization
- `pyproject.toml` — Poetry dependencies & scripts
- `ruff.toml` — Ruff linting & formatting configuration
- `lefthook.yml` — Git hooks configuration
- `scripts/` — Project automation scripts (see below)

## Scripts

All project automation and hook scripts should be placed in the `scripts/` directory. Current scripts include:

- `pre_push.sh` — Used by Lefthook for pre-push checks (linting, tests, etc.)
- `postinstall.sh` — Post-install setup steps to 
- `python-autoenv.sh` — Used by direnv for automated Python environment setup

If you add custom automation or hook scripts, place them in this directory for consistency.

## Setup

1. **Clone the repo:**
   ```sh
   git clone <repo-url>
   cd python-fastapistarter
   ```
1. **Automated Python virtualenv setup (recommended):**

   There is an `.envrc` file included in the repo, so no setup of the `virtualenv` is needed except approving it i.e. `direnv allow`. The automated environment uses [direnv](https://direnv.net/), the `.envrc` and the included `scripts/python-autoenv.sh` script:

   1. **Install direnv** (if not already installed):
      - On Ubuntu/Debian:
        ```sh
        sudo apt install direnv
        ```
      - On macOS (Homebrew):
        ```sh
        brew install direnv
        ```
      - Or see [direnv installation docs](https://direnv.net/docs/installation.html)
   1. **Enable direnv in your shell:**
      - For bash, add to `~/.bashrc`:
        ```sh
        eval "$(direnv hook bash)"
        ```
      - For zsh, add to `~/.zshrc`:
        ```sh
        eval "$(direnv hook zsh)"
        ```

   1. **Approve the environment:**
      ```sh
      direnv allow
      ```
      This enables the automated setup: when you enter the project directory, direnv will create and activate `.venv` if missing and install dependencies automatically.

   If you don't use direnv, you can remove the `.envrc` file and manually set up the environment, but I don't recommend that, automation prevents stupid mistakes:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   poetry install
   ```
1. **Set up environment variables:**
   - For local development, create a `.env.local` file if needed (e.g., for DB connection, secrets).
   - For GitHub releases, set `GH_TOKEN` in your GitHub repository secrets.

## Environment Variables

Environment variables are used to configure the application.

### Files

- `.env`: Used for static/build-time environment variables. These are values that do not change across deployment environments (e.g., `ROOT_PATH`). This file is copied into the Docker image and is available in all environments.
- `.env.local`: Used for secrets and environment-specific variables (e.g., credentials, API keys, local overrides). This file should NOT be copied into the Docker image and is intended for local development or runtime overrides. It is referenced via `env_file` in `docker-compose.yml` and can be injected at runtime in production (e.g., via Kubernetes secrets).

**Best practice:**
- Keep sensitive values (secrets, credentials) in `.env.local` and out of version control.
- Use `.env` for configuration that is safe to bake into the image and share across environments.
- In Docker Compose, you can reference both files in `env_file` to allow local overrides and secrets to take precedence over static values.

## Running the API

### With Docker Compose

```sh
docker compose up --build
```
- API: http://localhost:8000
- DB: PostgreSQL/PostGIS, data persisted in Docker volume

### Locally (Uvicorn)

```sh
poetry run start
```
- Hot-reloading enabled

### In VS Code

- Use the provided launch and task configurations in `.vscode/`.
- Press `F5` or run tasks for `Lint & Format`, `Test`, and `Run API`, `Start Docker`.

## Testing

### Run all tests

```sh
poetry run test
```
### Run tests in a group/file

```sh
poetry run test tests/test_main.py
```
### Run a single test

```sh
poetry run test tests/test_main.py::test_read_root
```

## Passing Arguments to Poetry Scripts

You can pass additional arguments to Poetry scripts defined in `pyproject.toml`. For example:

- Run a specific test file:
  ```sh
  poetry run test tests/test_main.py
  ```
- Run a single test:
  ```sh
  poetry run test tests/test_main.py::test_read_root
  ```
- Lint and format a specific directory:
  ```sh
  poetry run lint src/python_fastapi_starter/api
  ```

Arguments after the script name are forwarded to the underlying tool (pytest, ruff, etc.).

## Linting & Formatting

**Ruff** is used for both linting and formatting. Configuration is in `ruff.toml`. It should be the default provider for `python` in VS Code, see `.vscode/settings.json`.

**Import Sorting:** Ruff is configured to sort imports automatically as part of the linting process. Running `poetry run lint` will fix lint issues, format code, and sort imports—no separate step is required.

**NOTE:** There is an issue with **Ruff** in that it doesn't automatically format import statements unless you run the lint command. So while it may fix code on save/past/type, it won't update the imports. Make sure to run `poetry run lint` or `Lint & Format` task regularly to keep imports sorted.

- To lint and format code manually, use the Poetry scripts:
  ```sh
  poetry run lint
  ```
  This runs both linting, formatting, and import sorting on `src` and `tests`.
- Or use the VS Code task: **Lint & Format**.

## Releasing

- Releases are automated via GitHub Actions (`.github/workflows/release.yml`).
- Ensure your commit messages follow the [Angular commit guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines).
- Set `GH_TOKEN` in your GitHub repository secrets for release automation.
- To trigger a release manually:
  - Go to GitHub Actions → RELEASE → Run workflow

## Git Hooks

- Managed by `lefthook` (see `lefthook.yml`).
- Pre-push hook runs lint and tests via `scripts/pre_push.sh`.

## Database

### Initialization

- On the first run, schema and seed data are loaded from `db/schema.sql` and `db/seed.sql`.
- Data is persisted in Docker volume `db_data`.

### Wiping the Database and Starting Fresh

To completely reset the database and start from scratch:

1. **Stop all running containers:**
   ```sh
   docker compose down
   ```
1. **Remove the database volume:**
   ```sh
   docker volume rm python-fastapistarter_db_data
   ```
   (If your project folder name changes, adjust the volume name accordingly.)
1. **Start containers again:**
   ```sh
   docker compose up --build
   ```
   This will re-run the schema and seed scripts and create a fresh database.

## Debugging

You can debug your FastAPI app using either Docker or VS Code, depending on your workflow preference.

### Debugging in VS Code

- For a richer experience, use the VS Code debugger with the provided launch configuration (`.vscode/launch.json`).
  - This uses `debugpy` automatically and starts the app via `cli.py`.
  - Press `F5` or select "Run FastAPI (cli.py with Docker DB)" in the Run & Debug panel.
  - The database will be started automatically before the app launches.

### Debugging in Terminal (poetry run start)

If you prefer to run the app manually in your terminal (with Docker running for the database), you can debug using Python's built-in debugger:

- Add a breakpoint in your code:
  ```python
  import pdb; pdb.set_trace()
  ```
- Start the database using Docker Compose:
  ```sh
  docker compose up -d
  ```
- Run the app in your terminal:
  ```sh
  poetry run start
  ```
- When execution reaches the breakpoint, you'll drop into the interactive pdb debugger in your terminal.

This method works for any local development workflow and does not require extra dependencies. For more advanced debugging (e.g., remote attach), see the VS Code section above.

### Debugging in Docker/Docker Compose

- To use Python's built-in debugger (`pdb`), run your container interactively:
  ```sh
  docker compose run --service-ports --rm <service> python -m pdb <your_script.py>
  ```
  Or add `import pdb; pdb.set_trace()` in your code and start the service normally:
  ```sh
  docker compose run --service-ports --rm <service> poetry run start
  ```
  This will drop you into the debugger in your terminal when the breakpoint is hit.

## Anything Else?

- Customize `.gitmessage` for commit templates
- Use VS Code recommended extensions for best experience
- All dependencies are managed in `pyproject.toml` for reproducibility

## Contributing

We welcome contributions! Please follow these guidelines:

- **Code style:** Use Ruff for linting and formatting. Run `poetry run lint` before submitting PRs.
- **Testing:** Ensure all tests pass with `poetry run test`.
- **Commit messages:** Follow the [Angular commit guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines). A commit message template is provided in `.gitmessage`.
- **PRs:** Make pull requests against the `main` branch. Include a clear description and reference any related issues.
- **Release management:** Releases are automated via semantic-release and GitHub Actions. See the release section above for details.

## NGINX Security Configuration

When deploying behind NGINX (e.g., in Kubernetes), add the following to your NGINX config for improved security:

```
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;

limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
server {
    location / {
        limit_req zone=api_limit burst=20 nodelay;
        # ...other config...
    }
}
```

These headers and rate limiting settings help protect your API from common web vulnerabilities and basic DoS attacks. Adjust values as needed for your environment.
