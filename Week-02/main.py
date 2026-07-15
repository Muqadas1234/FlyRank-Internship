from fastapi import FastAPI, HTTPException
app = FastAPI()

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

@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )