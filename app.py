"""
This module contains the fastapi application logic
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from search_app import workflow  # from app.py

# Initialize FastAPI
app = FastAPI()

class GoogleSearchInput(BaseModel):
    """
    Pydantic model to parse input data for Google search
    """
    query_location: str

@app.post("/search")
async def google_search(input_data: GoogleSearchInput):
    """
    Endpoint to perform a Google search and sort the results
    """
    try:
        # Use the workflow from app.py for Google search and sorting
        sorted_results = workflow(input_data.query_location)
        return {"sorted_results": sorted_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
