# CampusCare

CampusCare is a complaint management web application for a campus. Students can register, sign in, submit complaints, and review their complaint history. The dashboard shows complaint counts and separates unresolved complaints from resolved complaints. Administrators can review complaints and mark them resolved.

The project has two parts:

- **Backend:** FastAPI, SQLAlchemy, and MySQL
- **Frontend:** HTML, CSS, and JavaScript, served as static files

## Project structure

```text
.
├── main.py                  # FastAPI application entry point
├── database.py              # Database connection and session setup
├── models.py                # SQLAlchemy models
├── database_create.py       # Optional standalone table creation script
├── auth.py                  # Login token creation
├── routes/
│   ├── auth_routes.py       # Registration and login endpoints
│   └── complaint_routes.py  # Complaint and dashboard endpoints
├── utils/
│   └── security.py          # Password hashing helpers
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── css/
│   └── js/app.js
├── requirements.txt
└── .env                     # Local settings; do not commit credentials
```

## Requirements

- Python 3.10 or later
- MySQL server and a database/schema for CampusCare
- Visual Studio Code with the Live Server extension, or another static HTTP server

## Configure the database

Create a MySQL database, then configure the backend environment variables in a `.env` file in the project root. Use your own database credentials; do not publish this file or commit real credentials.

```dotenv
DATABASE_URL=mysql+pymysql://DB_USER:DB_PASSWORD@DB_HOST:3306/DB_NAME
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
```

For a local MySQL instance, `DB_HOST` is commonly `localhost`. URL-encode special characters in the username or password if necessary. The MySQL database must exist and be reachable before starting the backend.

On startup, `main.py` calls SQLAlchemy `create_all()` to create any missing tables from `models.py`. It does not migrate or alter existing table schemas. `database_create.py` is also available to create the tables independently:

```powershell
python database_create.py
```

## Run locally with Uvicorn and Live Server

Use two terminals from the project root (`D:\mini project 2` in this workspace).

### 1. Start the backend

In PowerShell, create and activate a virtual environment, then install the listed dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

If PowerShell blocks virtual environment activation, you can invoke the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Keep this terminal running while using the frontend. Visit `http://127.0.0.1:8000/docs` to inspect and try the API endpoints.

### 2. Open the frontend with Live Server

In VS Code, right-click `templates/login.html` and choose **Open with Live Server**. Use the Live Server URL shown in the browser (often `http://127.0.0.1:5500/templates/login.html`) to register or sign in. The login page links to registration, and a successful login opens `dashboard.html`.

The frontend currently sends API requests to `http://127.0.0.1:8000`, as set by `BASE_URL` at the top of `templates/js/app.js`. This works when the browser and backend are running on the same computer. If your backend is hosted elsewhere, change `BASE_URL` to that backend's public HTTPS URL before using the frontend.

## API overview

Interactive API documentation is at `/docs` while the backend is running.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Backend health message |
| `POST` | `/register` | Register a user |
| `POST` | `/login` | Authenticate and return a token and user details |
| `POST` | `/complaints` | Submit a complaint |
| `GET` | `/complaints/user/{user_id}` | List a user's complaints |
| `GET` | `/complaints/zone/{zone}` | List complaints for a zone |
| `PATCH` | `/complaints/{complaint_id}` | Update a complaint status |
| `GET` | `/dashboard/stats` | Get complaint counts |
| `GET` | `/complaints` | List all complaints |

Supported user roles are `student`, `staff`, `warden`, and `admin`. Complaint statuses are `pending`, `assigned`, and `resolved`. The dashboard groups `resolved` complaints as solved and other statuses as pending.

## Deploying the frontend and backend separately

1. Deploy the FastAPI backend to a Python-capable host and configure its `DATABASE_URL`, `SECRET_KEY`, and `ALGORITHM` environment variables there. Run the app with a production ASGI server command such as `uvicorn main:app --host 0.0.0.0 --port $PORT` (adapt `$PORT` to the host's required port variable).
2. Confirm the backend is reachable over HTTPS and its `/` and `/docs` endpoints respond.
3. Set `BASE_URL` in `templates/js/app.js` to the backend's public HTTPS origin, for example `https://api.example.com` (no trailing slash is needed).
4. Deploy the contents of `templates/` as static files to a static web host. Set the deployed site's start page to `login.html` or open that page directly.
5. Configure the backend CORS policy in `main.py` to allow the exact origin of the deployed frontend. The current development setting allows every origin and should be narrowed for a public deployment.

Because the frontend is static, it does not require Python or Uvicorn. The browser calls the backend directly, so the API URL and CORS settings must match the deployed hosts. Keep database credentials and the token signing secret only in the backend environment; never put them in frontend JavaScript.

## Notes

- The application stores registered users, complaints, and locations in MySQL.
- The login flow stores returned user details and the access token in browser `localStorage`.
- The API currently allows requests without enforcing the returned token on complaint endpoints. Add server-side authentication and authorization before exposing administrative operations publicly.
- Keep the backend and database secrets out of source control. Rotate any credentials that have been exposed and use environment-specific credentials for development and deployment.
