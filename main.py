from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Expanded synthetic data representing domestic workers
workers_data = {
    1: {
        "name": "Alice Johnson",
        "age": 35,
        "contact": "alice@example.com",
        "employment_records": [
            {"employer": "Smith Family", "job_role": "Housekeeper", "months": 12},
            {"employer": "Brown Family", "job_role": "Nanny", "months": 24},
        ],
        "salary_details": {
            "salary_amount": 1500,
            "salary_slips": ["url_to_salary_slip_1", "url_to_salary_slip_2"],
            "current_months": 12,
            "payment_history": [1500, 1500, 1500],
        },
        "attendance": "96%",
        "performance_reviews": "Excellent",
    },
    2: {
        "name": "Bob Smith",
        "age": 42,
        "contact": "bob@example.com",
        "employment_records": [
            {"employer": "Anderson Family", "job_role": "Gardener", "months": 30},
            {"employer": "Miller Family", "job_role": "Driver", "months": 18},
        ],
        "salary_details": {
            "salary_amount": 2000,
            "salary_slips": ["url_to_salary_slip_3", "url_to_salary_slip_4"],
            "current_months": 30,
            "payment_history": [2000, 2000, 2000],
        },
        "attendance": "98%",
        "performance_reviews": "Very Good",
    },
    3: {
        "name": "Catherine Green",
        "age": 29,
        "contact": "catherine@example.com",
        "employment_records": [
            {"employer": "Jones Family", "job_role": "Cook", "months": 20},
            {"employer": "Taylor Family", "job_role": "Housekeeper", "months": 10},
        ],
        "salary_details": {
            "salary_amount": 1800,
            "salary_slips": ["url_to_salary_slip_5", "url_to_salary_slip_6"],
            "current_months": 20,
            "payment_history": [1800, 1800, 1800],
        },
        "attendance": "94%",
        "performance_reviews": "Good",
    },
    4: {
        "name": "David Lee",
        "age": 31,
        "contact": "david@example.com",
        "employment_records": [
            {"employer": "Williams Family", "job_role": "Driver", "months": 15},
            {"employer": "Harris Family", "job_role": "Gardener", "months": 25},
        ],
        "salary_details": {
            "salary_amount": 1700,
            "salary_slips": ["url_to_salary_slip_7", "url_to_salary_slip_8"],
            "current_months": 15,
            "payment_history": [1700, 1700, 1700],
        },
        "attendance": "92%",
        "performance_reviews": "Satisfactory",
    }
}

# Pydantic model for validating worker details
class WorkerDetails(BaseModel):
    name: str
    age: int
    contact: str
    employment_records: List[dict]
    salary_details: dict
    attendance: Optional[str] = None
    performance_reviews: Optional[str] = None

# GET endpoint to retrieve worker details by ID
@app.get("/worker/{worker_id}", response_model=WorkerDetails)
async def get_worker_details(worker_id: int):
    if worker_id in workers_data:
        return workers_data[worker_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with ID {worker_id} not found. Please check the ID and try again."
        )

# POST endpoint to create a new worker record
@app.post("/worker/", response_model=WorkerDetails)
async def create_worker(worker: WorkerDetails):
    new_id = max(workers_data.keys()) + 1
    workers_data[new_id] = worker.dict()
    return workers_data[new_id]

# PUT endpoint to update an existing worker's details
@app.put("/worker/{worker_id}", response_model=WorkerDetails)
async def update_worker(worker_id: int, worker: WorkerDetails):
    if worker_id in workers_data:
        workers_data[worker_id] = worker.dict()
        return workers_data[worker_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with ID {worker_id} not found. Unable to update non-existent record."
        )

# DELETE endpoint to remove a worker's record by ID
@app.delete("/worker/{worker_id}", response_model=dict)
async def delete_worker(worker_id: int):
    if worker_id in workers_data:
        del workers_data[worker_id]
        return {"message": "Worker deleted successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Worker with ID {worker_id} not found. No record to delete."
        )
