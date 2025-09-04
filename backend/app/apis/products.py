import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.product import ProductService
from app.dto.product import ProductCreate, ProductUpdate
from app.responses.product import ProductResponse, ProductListResponse
from app.responses.common import MessageResponse
from app.exceptions import ProductNotFoundError, DatabaseError
from app.dependencies import get_product_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):

    try:
        new_product = await service.create_product(product)
        logger.info(f"Product created via API: {new_product.id}")
        return new_product
    except DatabaseError as e:
        logger.error(f"Database error in create_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ProductListResponse)
async def get_products(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    available_only: bool = Query(False, description="Только доступные товары"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(10, ge=1, le=100, description="Количество товаров на странице"),
    service: ProductService = Depends(get_product_service)
):

    try:
        products, total = await service.get_products(
            category=category,
            available_only=available_only,
            page=page,
            limit=limit
        )

        return ProductListResponse(
            products=[p.model_dump() for p in products],
            total=total,
            page=page,
            limit=limit
        )
    except DatabaseError as e:
        logger.error(f"Database error in get_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):

    try:
        product = await service.get_product(product_id)
        return product
    except ProductNotFoundError as e:
        logger.warning(f"Product not found in API: {product_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in get_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):

    try:
        updated_product = await service.update_product(product_id, product)
        logger.info(f"Product updated via API: {product_id}")
        return updated_product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in update_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):

    try:
        success = await service.delete_product(product_id)
        if success:
            logger.info(f"Product deleted via API: {product_id}")
            return MessageResponse(message="Product deleted successfully")
        else:
            raise HTTPException(status_code=500, detail="Failed to delete product")
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in delete_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
