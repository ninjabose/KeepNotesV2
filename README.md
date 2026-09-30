# KeepNotesV2

A production-oriented Notes API built with FastAPI, Pydantic, and native async PyMongo.

This project is primarily a backend engineering personal project focused on:

- FastAPI architecture
- Pydantic validation
- MongoDB and query design
- Authentication and JWT security
- REST API design
- Async Python
- Testing
- Security best practices
- Production-oriented architecture

## Features

- User authentication and authorization
- JWT-based authentication
- Password hashing with Argon2
- CRUD operations for notes
- Note visibility:
  - Private
  - List
  - Friends
  - Public
- Note status:
  - Draft
  - Published
  - Archived
- Tag-based note searching
- Public note exploration/feed
- Cursor-based pagination
- MongoDB aggregation pipelines
- Admin analytics
- User note statistics
- Filtering and sorting
- Async database operations
- Pydantic request/response validation

## Pagination

The project implements cursor/keyset pagination for feed-style endpoints.

Instead of relying on increasingly expensive offsets such as:

    page=500&limit=10

the API uses a cursor based on a deterministic ordering:

    created_at + _id

The cursor is encoded into a token and returned to the client as `next_cursor`.

The client treats the cursor as an opaque value and sends it back when requesting the next batch.

Conceptually:

    GET /explore?limit=10
            ↓
       10 notes
            +
       next_cursor
            ↓
    GET /explore?limit=10&cursor=...
            ↓
       next 10 notes

This project also explores how pagination strategy connects with MongoDB indexing and query design.

## Feed / Explore

The `/explore` endpoint demonstrates a simple feed architecture:

    published + public notes
            ↓
       deterministic sort
            ↓
      cursor pagination
            ↓
          client

The project also uses this as a foundation for understanding more advanced feed systems such as candidate generation, ranking, personalization, and recommendation systems.

## MongoDB

MongoDB is used as the primary database through native async PyMongo.

The project covers:

- MongoDB queries
- Filtering
- Sorting
- Projection
- Aggregation pipelines
- `$group`
- `$lookup`
- `$project`
- `$arrayElemAt`
- Pagination
- Query/index design

## Tech Stack

- Python
- FastAPI
- Pydantic
- MongoDB
- PyMongo Async
- JWT
- Argon2

## Project Goal

KeepNotesV2 was built primarily as a backend engineering learning project.

The goal was not simply to build a notes application, but to use the application as a vehicle for learning how real backend systems are designed:

- API architecture
- Database modeling
- Query design
- Authentication
- Security
- Pagination
- Indexing
- Aggregation
- Scalability considerations
- Production-oriented design decisions

## Status

✅ Project completed

KeepNotesV2 is considered complete as a learning project.

Future experiments involving real-time communication, social graphs, personalized feeds, and WebSockets will be explored in separate projects.