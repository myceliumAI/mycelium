from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud.data_contract import (
    create_data_contract,
    delete_data_contract,
    get_data_contract,
    list_data_contracts,
    update_data_contract,
)
from ..database.manager import db_manager
from ..schemas.data_contract.routes.data_contract_create import (
    DataContractCreate,
    DataContractCreateResponse,
)
from ..schemas.data_contract.routes.data_contract_delete import (
    DataContractDelete,
    DataContractDeleteResponse,
)
from ..schemas.data_contract.routes.data_contract_get import DataContractGetResponse
from ..schemas.data_contract.routes.data_contract_list import DataContractListResponse
from ..schemas.data_contract.routes.data_contract_update import (
    DataContractUpdate,
    DataContractUpdateResponse,
)

router = APIRouter(tags=["Data Contract"])


@router.post(
    "/",
    response_model=DataContractCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new data contract",
    description="Creates a new data contract and stores it in the database.",
    response_description="Successfully created data contract",
    responses={
        201: {
            "content": {"application/json": {"example": DataContractCreateResponse.get_example()}},
        },
        400: {
            "description": "Invalid input",
            "content": {"application/json": {"example": {"detail": " ❌ Invalid data contract schema"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to create data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contract"],
)
async def create_data_contract_route(
    data_contract: DataContractCreate,
    db: Session = Depends(db_manager.get_db),
) -> DataContractCreateResponse:
    """
    Creates a new data contract and stores it in the database.

    This endpoint accepts a DataContractCreate object, validates it, and attempts to create
    a new data contract in the database. If successful, it returns the created contract.
    If an error occurs during the process, it raises an appropriate HTTP exception.

    :param DataContractCreate data_contract: The data contract to be created, validated against the DataContractCreate model.
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractCreateResponse: A response containing a success message and the created data contract.
    :raises HTTPException:
        - 400 Bad Request: If the input data is invalid.
        - 500 Internal Server Error: If there's an unexpected error during contract creation.
    """
    try:
        created_contract = create_data_contract(db, data_contract)
        return DataContractCreateResponse(message=" ✅ Data contract created successfully", data=created_contract)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f" ❌ Invalid data contract schema: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to create data contract: {str(e)}"
        )


@router.get(
    "/{id}",
    response_model=DataContractGetResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a data contract",
    description="Retrieves a data contract from the database by its ID.",
    response_description="Successfully retrieved data contract",
    responses={
        200: {
            "content": {"application/json": {"example": DataContractGetResponse.get_example()}},
        },
        404: {
            "description": "Data contract not found",
            "content": {"application/json": {"example": {"detail": " ❌ Data contract not found"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to retrieve data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contract"],
)
async def get_data_contract_route(id: str, db: Session = Depends(db_manager.get_db)) -> DataContractGetResponse:
    """
    Retrieves a data contract from the database by its ID.

    This endpoint accepts a data contract ID, attempts to retrieve the corresponding
    data contract from the database. If successful, it returns the retrieved contract.
    If the contract is not found or an error occurs, it raises an appropriate HTTP exception.

    :param str id: The unique identifier of the data contract to retrieve. Example: "urn:datacontract:checkout:orders-latest"
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractGetResponse: A response containing a success message and the retrieved data contract.
    :raises HTTPException:
        - 404 Not Found: If the data contract with the given ID is not found.
        - 500 Internal Server Error: If there's an unexpected error during contract retrieval.
    """
    try:
        retrieved_contract = get_data_contract(db, id)
        if retrieved_contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" ❌ Data contract not found: {id}")
        return DataContractGetResponse(message=" ✅ Data contract retrieved successfully", data=retrieved_contract)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to retrieve data contract: {str(e)}"
        )


@router.get(
    "/",
    response_model=DataContractListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all data contracts",
    description="Retrieves all data contracts from the database.",
    response_description="Successfully retrieved data contracts",
    responses={
        200: {
            "content": {"application/json": {"example": DataContractListResponse.get_example()}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to retrieve data contracts: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contract"],
)
async def list_data_contracts_route(db: Session = Depends(db_manager.get_db)) -> DataContractListResponse:
    """
    Retrieves all data contracts from the database.

    This endpoint attempts to retrieve all data contracts from the database.
    If successful, it returns a list of all contracts.
    If an error occurs during the process, it raises an appropriate HTTP exception.

    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractListResponse: A response containing a success message and the list of data contracts.
    :raises HTTPException:
        - 500 Internal Server Error: If there's an unexpected error during contract retrieval.
    """
    try:
        contracts = list_data_contracts(db)
        return DataContractListResponse(message=" ✅ Data contracts retrieved successfully", data=contracts)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f" ❌ Failed to retrieve data contracts: {str(e)}",
        )


@router.put(
    "/{id}",
    response_model=DataContractUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a data contract",
    description="Updates an existing data contract in the database.",
    response_description="Successfully updated data contract",
    responses={
        200: {
            "content": {"application/json": {"example": DataContractUpdateResponse.get_example()}},
        },
        404: {
            "description": "Data contract not found",
            "content": {"application/json": {"example": {"detail": " ❌ Data contract not found"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to update data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contract"],
)
async def update_data_contract_route(
    id: str,
    data_contract_update: DataContractUpdate,
    db: Session = Depends(db_manager.get_db),
) -> DataContractUpdateResponse:
    """
    Updates an existing data contract in the database.

    This endpoint accepts a data contract ID and update information, attempts to update the corresponding
    data contract in the database. If successful, it returns the updated contract.
    If the contract is not found or an error occurs, it raises an appropriate HTTP exception.

    :param str id: The unique identifier of the data contract to update.
    :param DataContractUpdate data_contract_update: The update information for the data contract.
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractUpdateResponse: A response containing a success message and the updated data contract.
    :raises HTTPException:
        - 404 Not Found: If the data contract with the given ID is not found.
        - 500 Internal Server Error: If there's an unexpected error during contract update.
    """
    try:
        updated_contract = update_data_contract(db, id, data_contract_update)
        if updated_contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" ❌ Data contract not found: {id}")
        return DataContractUpdateResponse(message=" ✅ Data contract updated successfully", data=updated_contract)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to update data contract: {str(e)}"
        )


@router.delete(
    "/{id}",
    response_model=DataContractDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a data contract",
    description="Deletes an existing data contract from the database.",
    response_description="Successfully deleted data contract",
    responses={
        200: {
            "content": {"application/json": {"example": DataContractDeleteResponse.get_example()}},
        },
        404: {
            "description": "Data contract not found",
            "content": {"application/json": {"example": {"detail": " ❌ Data contract not found"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to delete data contract: Internal server error"}
                }
            },
        },
    },
    tags=["Data Contract"],
)
async def delete_data_contract_route(
    id: str = "urn:datacontract:checkout:orders-latest",
    db: Session = Depends(db_manager.get_db),
) -> DataContractDeleteResponse:
    """
    Deletes an existing data contract from the database.

    This endpoint accepts a data contract ID, attempts to delete the corresponding
    data contract from the database. If successful, it returns the deleted contract.
    If the contract is not found or an error occurs, it raises an appropriate HTTP exception.

    :param str id: The unique identifier of the data contract to delete.
    :param Session db: The database session, automatically provided by FastAPI's dependency injection.
    :return DataContractDeleteResponse: A response containing a success message and the deleted data contract.
    :raises HTTPException:
        - 404 Not Found: If the data contract with the given ID is not found.
        - 500 Internal Server Error: If there's an unexpected error during contract deletion.
    """
    try:
        data_contract_delete = DataContractDelete(id=id)
        deleted_contract = delete_data_contract(db, data_contract_delete)
        if deleted_contract is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" ❌ Data contract not found: {id}")
        return DataContractDeleteResponse(message=" ✅ Data contract deleted successfully", data=deleted_contract)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Failed to delete data contract: {str(e)}"
        )
