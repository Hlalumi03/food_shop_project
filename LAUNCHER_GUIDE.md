# Food Shop Launcher

The launcher starts one FastAPI server for both the frontend and backend. The
page and its `/api/v1` requests use the same host and port, so there is no
separate frontend server or API URL to configure.

## Start the application

From the project directory, run one of:

```powershell
.\start.ps1
```

```cmd
start.bat
```

```bash
./start.sh
```

The launcher initializes the SQLite database and starts the server on
`127.0.0.1:8001`.

| Component | URL |
|---|---|
| Frontend | http://127.0.0.1:8001/ |
| API | http://127.0.0.1:8001/api/v1 |
| API docs | http://127.0.0.1:8001/docs |

The frontend calls relative paths such as `/api/v1/foods`, so it continues to
use the same API when the application is hosted on another port or domain.

Press **Ctrl+C** in the launcher terminal to stop the server.

## Run the server directly

The same combined application can be started without the launcher:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

To change the port, change the `--port` value. The frontend API URL does not
need to be changed.
