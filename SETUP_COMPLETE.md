# Food Shop Setup

The Food Shop frontend and backend API run together in one FastAPI application.
The browser loads the UI from `/` and calls the API at `/api/v1` on the same
host and port.

## Start the application

From the project directory, start the app with one of:

```powershell
.\start.ps1
```

```cmd
start.bat
```

```bash
./start.sh
```

The launcher initializes the SQLite database and starts the combined app at
`http://127.0.0.1:8001/`.

| Component | URL |
|---|---|
| Frontend | http://127.0.0.1:8001/ |
| API | http://127.0.0.1:8001/api/v1 |
| Interactive API docs | http://127.0.0.1:8001/docs |

Press **Ctrl+C** in the terminal to stop the server.

## Run without the launcher

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

The frontend's API URL is relative (`/api/v1`), so if you choose a different
port, open the app on that port; no frontend configuration is needed.

Seed sample food items if needed:

```bash
python seed_foods.py
```

## Verify the app

With the server running, check:

- `http://127.0.0.1:8001/` loads the frontend.
- `http://127.0.0.1:8001/api/v1/foods` returns the food list.
- `http://127.0.0.1:8001/docs` opens the API documentation.

## Database

The app uses the SQLite database at `food_shop.db`. Tables are created when
the app starts. Use `seed_foods.py` to add sample food items.
