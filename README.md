# FitTrack – Backend API

A scalable backend service for tracking fitness sessions, exercise repetitions, and pose-assisted workout data. Built to support modern mobile and web fitness applications.

![App Screenshot](app/UI_Templates/Home_Page.jpg)

## Overview

FitTrack is a RESTful backend built with FastAPI that manages fitness users, workout sessions, rep-level feedback, and progress tracking.
It is designed as a secure and extensible API layer for fitness platforms.

## Features

- *Role-Based Authentication*: Trainee, Trainer, and Admin support
- *JWT Security*: Secure login and protected endpoints
- *Exercise Sessions*: Start, record, and end workout sessions
- *Pose-Assisted Data*: Store per-rep landmarks, correctness, and feedback
- *Progress Tracking*: Session history and performance data

## Tech Stack

- *Backend*: Python 3.10+, FastAPI
- *ORM*: SQLAlchemy
- *Validation*: Pydantic
- *Authentication*: JWT
- *Server*: Uvicorn

## API Endpoints

### Authentication

- POST /auth/register – Register trainee, trainer, or admin
- POST /auth/login – Login and receive JWT token

### Exercise Sessions

- POST /exercise/session/start – Start workout session
- POST /exercise/session/{id}/data – Add rep data
- POST /exercise/session/{id}/end – End session
- GET /exercise/session/history – View session history

## Installation

### Clone the repository

bash
git clone <repository-url>


### Create virtual environment

bash
python -m venv .venv
source .venv/Scripts/activate


### Install dependencies

bash
pip install -r requirements.prod.txt


### Configure environment variables

- Create .env.development
- Add DATABASE_URL and SECRET_KEY

### Run the server

bash
uvicorn app.main:app --reload


## Usage

- *Swagger UI*: http://127.0.0.1:8000/docs
- *ReDoc*: http://127.0.0.1:8000/redoc
