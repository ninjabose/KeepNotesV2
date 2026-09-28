# KeepNotesV2

A production-oriented Notes API built with FastAPI, Pydantic, MongoDB, and native async PyMongo.

## About

KeepNotesV2 is a backend engineering project focused on building a secure,
async REST API while exploring real-world backend architecture and MongoDB.

The project currently includes:

- User authentication and authorization
- JWT access and refresh tokens
- Argon2 password hashing
- User profile management
- Notes CRUD operations
- Pydantic request/response validation
- MongoDB aggregation pipelines
- Admin-only endpoints
- Note analytics
- Async database operations
- OpenAPI / Swagger documentation

## Tech Stack

- Python
- FastAPI
- Pydantic
- MongoDB
- PyMongo Async
- JWT
- Argon2

## API

### Users

- `POST /users/signup` — User signup
- `POST /users/login` — User login
- `POST /users/refresh` — Renew access token
- `PATCH /users/` — Update user

### Notes

- `POST /notes/` — Create note
- `GET /notes/` — Get notes
- `PATCH /notes/{note_id}` — Edit note
- `DELETE /notes/{note_id}` — Delete note

### Admin

- `GET /admin/get_count` — Get note statistics
- `GET /admin/notes_per_user` — Get notes grouped by user
- `GET /admin/notes_per_year` — Get notes grouped by year

## Current Status

### V1 — Complete ✅

The first working version of the API is complete.

Future development will focus on improving architecture, testing,
security hardening, persistence/service separation, and production readiness.