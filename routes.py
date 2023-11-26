from fastapi import APIRouter, Request, HTTPException, status, Body
from typing import List
from model import Airport, AdvertisingCampaign, Travel
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.post("/airports", response_description="Add a new airport",
             status_code=status.HTTP_201_CREATED, response_model=Airport)
def create_airport(request: Request, airport: Airport = Body(...)):
    airport = jsonable_encoder(airport)
    new_airport = request.app.database["airports"].insert_one(airport)
    created_airport = request.app.database["airports"].find_one(
        {"_id": new_airport.inserted_id}
    )
    return created_airport


@router.post("/campaigns", response_description="Add a new campaign",
             status_code=status.HTTP_201_CREATED, response_model=AdvertisingCampaign)
def create_campaign(request: Request, campaign: AdvertisingCampaign = Body(...)):
    campaign = jsonable_encoder(campaign)
    new_campaign = request.app.database["campaigns"].insert_one(campaign)
    created_camp = request.app.database["campaigns"].find_one(
        {"_id": new_campaign.inserted_id}
    )
    return created_camp


@router.post("/travels", response_description="Add a new travel",
             status_code=status.HTTP_201_CREATED, response_model=Travel)
def create_travel(request: Request, travel: Travel = Body(...)):
    travel = jsonable_encoder(travel)
    new_travel = request.app.database["travels"].insert_one(travel)
    created_travel = request.app.database["travels"].find_one(
        {"_id": new_travel.inserted_id}
    )
    return created_travel


@router.get("/airports", response_description="Get airports in a country", response_model=List[Airport])
def get_airports(request: Request, country: str = "USA"):
    airports = list(request.app.database["airports"].find({"country": {"$eq": country}}))
    return airports


@router.get("/advertising-months/{airport_name}",
            response_description="Get optimal advertising months for a specific airport", response_model=list)
def get_optimal_advertising_months(airport_name: str, request: Request):
    # Obtén el número de viajes por mes para el aeropuerto dado
    pipeline = [
        {"$match": {"$or": [{"from_airport": airport_name}, {"to_airport": airport_name}]}},
        {"$group": {"_id": "$month", "total_travels": {"$sum": 1}}},
        {"$sort": {"total_travels": -1}}
    ]
    results = list(request.app.database["travels"].aggregate(pipeline))
    if not results:
        raise HTTPException(status_code=404, detail="No travel data found for the specified airport.")

    # Se obtienen los meses con el mayor número de viajes
    optimal_months = [str(result["_id"]) for result in results]
    return optimal_months


