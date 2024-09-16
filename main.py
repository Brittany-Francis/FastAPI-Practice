from fastapi import FastAPI, HTTPException

#API will take pydanctic model and convert it into json
from pydantic import BaseModel

from typing import List, Optional

#python function to call that generate a unique ID
from uuid import UUID, uuid4


#creates an instance of fastAPI
app=FastAPI()

#task model
class Task(BaseModel):
    #id is optional and will be a unique id using uuid4()
    id: Optional[UUID]=None
    #title is manditory and is a string
    title: str
    #description is optional but will be a string
    description: Optional[str]=None
    #task is incomplete upon creation
    complete:bool=False

#list of tasks
tasks=[]

#create a new task using Task class
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    #generate a new id for each task using uuid4()
    task.id=uuid4()
    #append this task to the task list
    tasks.append(task)
    return task

#creating the "read" part of crud, will retrieve information
@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    #returns the list of tasks
    return tasks

#retrieve one tasks by its id
@app.get("/tasks/{task_id}", response_model=Task)
def read_one_task(task_id: UUID):
    for task in tasks:
        if task.id== task_id:
            return task
    raise HTTPException(status_code= 404, detail="Task not found")

#update a task based on its id
@app.put("/tasks/{task_id}", response_model=Task)
#pass in task id and Task model
def update_task(task_id: UUID, task_update: Task):
    #allows you to loop over something with an automatic counter
    for idx, task in enumerate(tasks):
        if task.id== task_id:
            #copies the task you found, allows you to update, ignore unset values from model
            updated_task=task.copy(update=task_update.model_dump(exclude_unset=True))
            tasks[idx]=updated_task
            return updated_task
    #make your own status code in case there is no task with the requested id
    raise HTTPException(status_code= 404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id==task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code= 404, detail="Task not found")


if __name__=="__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
