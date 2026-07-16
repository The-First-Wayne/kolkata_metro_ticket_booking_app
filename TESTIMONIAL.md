# Project Testimonial

## My Approach

I first reviewed the project structure and identified the separate backend, frontend, and database components. I then started each service, tested the API endpoints, and fixed issues as they appeared.

## My Understanding of the Project

This project is a Kolkata Metro ticket-booking application. The React frontend allows users to plan routes, view system health, and book tickets. The FastAPI backend manages route calculations, ticket records, PostgreSQL verification, SQLite metro data, and a background scheduler.

## Bugs I Encountered and Resolved

- The `.env.example` database URL was missing the colon between `localhost` and port `5432`. I corrected the connection string so PostgreSQL could use the configured host and port correctly.
- SQLAlchemy was missing from the environment, so I installed the dependency.
- The frontend imported `lucide-react`, but the package was missing from the project dependencies. I installed it so the Vite application could build correctly.
- The SQLite database path used the wrong `metadata_graph.db` filename and treated the `sqlite_client.py` file as a directory. I used `.parent` to reference the folder containing the Python file, allowing the application to locate the database correctly.
- The frontend used the wrong API port and the backend CORS settings did not allow the Vite development server. I aligned both with port 8000 and allowed the Vite origin.
- The station-list and route-calculation backend functions were placeholders. I implemented the SQLite station query and Dijkstra-based route calculation.

## Challenges Faced

The main challenge was tracing issues across the frontend, backend, PostgreSQL, SQLite, and the background worker. Each layer depended on the others, so I verified the services and API responses step by step.

## Assumptions Made

- PostgreSQL is running locally and contains the provided schema and seed data.
- The frontend runs through Vite on port 5173.
- Metro connections and interchanges in the SQLite database can be travelled in both directions.

## Improvements with More Time

I would add automated tests for API endpoints and route calculations, improve error messages in the UI, move configuration values to environment files, and add authentication for ticket users.
