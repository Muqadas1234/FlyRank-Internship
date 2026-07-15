from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing a to-do task list.",
    version="1.0"
)


# In-memory task list
tasks = [
    {
        "id": 1,
        "title": "Complete Python Homework",
        "done": False
    },
    {
        "id": 2,
        "title": "Attend Backend Internship Session",
        "done": False
    },
    {
        "id": 3,
        "title": "Submit Week 2 Assignment",
        "done": True
    }
]


# Request model
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


# Root endpoint
@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the Task API."
)
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health endpoint
@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the API server is running."
)
def health():
    return {
        "status": "ok"
    }


# Get all tasks
@app.get(
    "/tasks",
    summary="Get all tasks",
    description="Returns the complete list of tasks."
)
def get_all_tasks():
    return tasks


# Get single task
@app.get(
    "/tasks/{task_id}",
    summary="Get task by ID",
    description="Returns a specific task using its unique ID."
)
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Create task
@app.post(
    "/tasks",
    status_code=201,
    summary="Create a new task",
    description="Creates a new task. Title is required and cannot be empty."
)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# Update task
@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and completion status of an existing task."
)
def update_task(task_id: int, updated_task: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Delete task
@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task using its ID."
)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )