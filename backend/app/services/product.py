import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import Binary
from bson.errors import InvalidId

from app.models.product import Product
from app.dto.product import ProductCreate, ProductUpdate
from app.exceptions import ProductNotFoundError, DatabaseError

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, db_client: MongoClient):
        self.db = db_client.restaurant_db
        self.collection = self.db.products

    async def create_product(self, product_data: ProductCreate) -> Product:
        """Создание товара"""
        try:
            product = Product(**product_data.model_dump())

            result = self.collection.insert_one(product.model_dump(by_alias=True))

            if result.inserted_id:
                logger.info(f"Product created successfully: {product.id}")
                return product
            else:
                raise DatabaseError("Failed to create product")

        except PyMongoError as e:
            logger.error(f"Database error creating product: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def get_product(self, product_id: UUID) -> Optional[Product]:

        try:
            product_data = self.collection.find_one({"_id": Binary.from_uuid(product_id)})

            if not product_data:
                logger.warning(f"Product not found: {product_id}")
                raise ProductNotFoundError(f"Product {product_id} not found")

            product_data["id"] = product_id
            del product_data["_id"]

            return Product(**product_data)

        except InvalidId:
            logger.error(f"Invalid product ID format: {product_id}")
            raise ProductNotFoundError(f"Invalid product ID: {product_id}")
        except PyMongoError as e:
            logger.error(f"Database error getting product {product_id}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def get_products(self,
        category: Optional[str] = None,
        available_only: bool = False,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[List[Product], int]:
        try:
            filter_query = {}

            if category:
                filter_query["category"] = category
            if available_only:
                filter_query["is_available"] = True

            total = self.collection.count_documents(filter_query)

            cursor = self.collection.find(filter_query).skip((page - 1) * limit).limit(limit)

            products = []
            for product_data in cursor:
                product_data["id"] = product_data["_id"]
                del product_data["_id"]
                products.append(Product(**product_data))

            logger.info(f"Retrieved {len(products)} products (page {page}, total {total})")
            return products, total

        except PyMongoError as e:
            logger.error(f"Database error getting products: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Product:
        try:
            await self.get_product(product_id)

            update_data = {k: v for k, v in product_data.model_dump().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()

            result = self.collection.update_one(
                {"_id": Binary.from_uuid(product_id)},
                {"$set": update_data}
            )

            if result.modified_count > 0:
                logger.info(f"Product updated successfully: {product_id}")
                return await self.get_product(product_id)
            else:
                logger.warning(f"No changes made to product: {product_id}")
                return await self.get_product(product_id)

        except ProductNotFoundError:
            raise
        except PyMongoError as e:
            logger.error(f"Database error updating product {product_id}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            await self.get_product(product_id)

            result = self.collection.delete_one({"_id": Binary.from_uuid(product_id)})

            if result.deleted_count > 0:
                logger.info(f"Product deleted successfully: {product_id}")
                return True
            else:
                return False

        except ProductNotFoundError:
            raise
        except PyMongoError as e:
            logger.error(f"Database error deleting product {product_id}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")