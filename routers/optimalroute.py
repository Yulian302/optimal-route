
from fastapi import Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter


from main import *
from optimal_route import best_k_city_tsp


router = APIRouter()


@router.post("/optimal")
async def get_optimal_route(start_address: str = Form(...), n_best: int = Form(...), file: UploadFile | None = None, addresses: str | None = Form(None)):
    if file:
        contents = await file.read()
        addresses_ = list(
            map(lambda s: s.decode("ascii"), contents.splitlines()))
    elif addresses:
        addresses_ = addresses.split(";")
    else:
        return JSONResponse(content={
            "error": "No input destinations! Upload a file or specify manually."
        }, status_code=422)

    adj_matrix = create_adjacency_matrix(start_address, addresses_)
    _, min_cost, best_path = best_k_city_tsp(adj_matrix, n_best, 0)
    minutes, seconds = divmod(min_cost, 60)
    best_path_verbose = " -> ".join([start_address if node ==
                                     0 else addresses_[node-1] for node in best_path])+" -> "+start_address
    return {"Minimum travel time": f"{minutes:.0f} minutes {seconds:.0f} seconds", "Optimal path": best_path_verbose}
