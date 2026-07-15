from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


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
@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Get all tasks
@app.get("/tasks")
def get_all_tasks():
    return tasks


# Get a single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    # Validate title
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    # Create new task
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    # Add task to the list
    tasks.append(new_task)

    # Return created task
    return new_task

@app.put("/tasks/{task_id}")
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

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )