from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.product_schema import CreateProduct, ReadProduct, UpdateProduct
from src.enums.enums import UserRole
from src.core.exceptions import EntityNotFound, PermissionDenied, EntityAlreadyExist
from src.models.user import User

class ProductService:
    def __init__(self, uow_factory: UnitOfWork):
        self.uow_factory = uow_factory

    async def create_product(self, current_user: User, product_data: CreateProduct):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            product = await self.uow_factory.product_repo.get_product_by_name(product_data.name)
            if product:
                raise EntityAlreadyExist(
                    message="Product already exist in database",
                    details={
                        "recommendation": "Pass a different product name"
                    }
                )
            new_product = await self.uow_factory.product_repo.create_product(product_data)
        return {
            "status": "success",
            "message": "Product successfully created",
            "data": ReadProduct.model_validate(new_product)
        }
    

    async def bulk_create_products(self, current_user: User, products_data: list[CreateProduct]):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            new_products = await self.uow_factory.product_repo.bulk_create_products(products_data)
            return {
                "status": "success",
                "message": "Products successfully created",
                "data": [ReadProduct.model_validate(product) for product in new_products]
            }
        
    
    async def get_single_product(self, product_id: str):
        async with self.uow_factory:
            product = await self.uow_factory.product_repo.get_by_id(product_id)
        return {
            "status": "success",
            "message": "Product successfully created",
            "data": ReadProduct.model_validate(product)
        }
    

    async def get_multiple_products(self, product_ids: list[str]):
        async with self.uow_factory:
            products = await self.uow_factory.product_repo.get_multiple_products(product_ids)
        return {
            "status": "success",
            "message": "Products successfully retrieved",
            "data": [ReadProduct.model_validate(product) for product in products]
        }
    
    async def get_products_by_category(self, category_id: str):
        async with self.uow_factory:
            print("Hello World")
            products = await self.uow_factory.product_repo.get_products_by_category(category_id)
            print(products)
        return {
            "status": "success",
            "message": "Products successfully retrieved",
            "data": [ReadProduct.model_validate(product) for product in products]
        }

    async def update_product(self, current_user: User, product_id: str, product_data: UpdateProduct):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            product = await self.uow_factory.product_repo.get_by_id(product_id)
            if not product:
                raise EntityNotFound(
                    message="Product not found",
                    details={
                        "recommendation": "Make sure you pass the right product_id"
                    }
                )
            
            updated_product = await self.uow_factory.product_repo.update_product(product_id, product_data)
        return {
            "status": "success",
            "message": "Product successfully updated",
            "data": ReadProduct.model_validate(updated_product)
        }
    
    
    async def delete_product(self, current_user: User, product_id: str):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            product = await self.uow_factory.product_repo.get_by_id(product_id)
        
            if not product:
                raise EntityNotFound(
                    message="Product not found",
                    details={
                        "recommendation": "Make sure you pass the right product_id"
                    }
                )
        
            await self.uow_factory.product_repo.delete(product_id, soft=True)

        return {
            "status": "success",
            "message": "Product successfully deleted"
        }
    
    async def bulk_delete_products(self, current_user: User, products_id: list[str]):
        async with self.uow_factory:
            if current_user.role != UserRole.ADMIN:
                raise PermissionDenied(
                    message="You do not have permission to update product",
                    details={
                        "recommendation": "Make sure user is an admin"
                    }
                )
            products = await self.uow_factory.product_repo.get_multiple_products(products_id)
            if not products:
                raise EntityNotFound(
                    message="Product not found",
                    details={
                        "recommendation": "Make sure you pass the right product_id"
                    }
                )
            
            deleted_products = await self.uow_factory.product_repo.bulk_delete_products(products_id)
        return {
            "status": "success",
            "message": "Products successfully deleted",
            "total_products_deleted": deleted_products
        }
        
    


