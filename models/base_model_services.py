from typing import Type, List, Optional, TypeVar
from uuid import uuid4

from asgiref.sync import sync_to_async
from django.db import models, transaction


class ModelServices:
    T = TypeVar('T', bound=models.Model)

    def __init__(self, model_class_name: Type[models.Model]):
        self.__model = model_class_name

    async def insert(self, entity: T) -> Optional[uuid4]:
        """ Insert a single entity """
        if entity is None:
            return None
        try:
            entity.id = uuid4()  # Assuming ID is a UUID field
            await entity.save()
            return entity.id
        except Exception as ex:
            raise Exception(f"Error inserting entity: {ex}")

    async def insert_bulk(self, entities: List[T]) -> List[T]:
        """ Insert a list of entities """
        try:
            if not entities:
                return []
            for entity in entities:
                entity.id = uuid4()  # Assuming ID is a UUID field
            await self.__model.objects.bulk_create(entities)
            return entities
        except Exception as ex:
            raise Exception(f"Error inserting entities: {ex}")

    async def update(self, entity: T) -> bool:
        """ Update an existing entity """
        if entity is None:
            return False
        try:
            await entity.save(update_fields=[field.name for field in entity._meta.fields if field.name != "id"])
            return True
        except Exception as ex:
            raise Exception(f"Error updating entity: {ex}")

    async def update_bulk(self, entities: List[T]) -> List[T]:
        """ Update a list of entities """
        try:
            if not entities:
                return []
            updated_entities = []
            async with transaction.atomic():
                for entity in entities:
                    await entity.save(update_fields=[field.name for field in entity._meta.fields if field.name != "id"])
                    updated_entities.append(entity)
            return updated_entities
        except Exception as ex:
            raise Exception(f"Error updating entities: {ex}")

    @sync_to_async
    def get(self, entity_id: uuid4) -> Optional[T]:
        try:
            return self.__model.objects.get(pk=entity_id)
        except Exception as ex:
            raise Exception(f"Error retrieving entity: {ex}")

    async def get_by_condition(self, condition: dict) -> Optional[T]:
        """ Get an entity based on a condition """
        try:
            return await self.__model.objects.filter(**condition).first()
        except Exception as ex:
            raise Exception(f"Error retrieving entity by condition: {ex}")

    async def get_list(self, is_tracking: bool = True, skip: int = 0, limit: int = 100) -> List[T]:
        """ Get a list of entities with pagination """
        try:
            queryset = self.__model.objects.all() if is_tracking else self.__model.objects.all().only(
                *[field.name for field in self.__model._meta.fields])
            return await queryset.skip(skip).limit(limit).all()
        except Exception as ex:
            raise Exception(f"Error retrieving entity list: {ex}")

    async def get_list_by_condition(
            self,
            condition: dict,
            is_tracking: bool = True,
            skip: int = 0,
            limit: int = 100) -> List[T]:
        """ Get a list of entities based on a condition with pagination """
        try:
            queryset = self.__model.objects.filter(**condition)
            if not is_tracking:
                queryset = queryset.only(*[field.name for field in self.__model._meta.fields])
            return await queryset.skip(skip).limit(limit).all()
        except Exception as ex:
            raise Exception(f"Error retrieving filtered entity list: {ex}")

    async def remove(self, entity_id: uuid4) -> bool:
        """ Remove an entity by ID """
        try:
            entity = await self.__model.objects.filter(id=entity_id).first()
            if entity:
                await entity.delete()
                return True
            return False
        except Exception as ex:
            raise Exception(f"Error removing entity: {ex}")

    async def remove_by_condition(self, condition: dict) -> bool:
        """ Remove entities by condition """
        try:
            deleted_count, _ = await self.__model.objects.filter(**condition).delete()
            return deleted_count > 0
        except Exception as ex:
            raise Exception(f"Error removing entities: {ex}")

    async def count(self, condition: dict) -> int:
        """ Count the number of entities by condition """
        try:
            return await self.__model.objects.filter(**condition).count()
        except Exception as ex:
            raise Exception(f"Error counting entities: {ex}")

    async def sum(self, condition: dict, field: str) -> Optional[float]:
        """ Sum a numeric field based on condition """
        try:
            return await self.__model.objects.filter(**condition).aggregate(total=models.Sum(field))['total']
        except Exception as ex:
            raise Exception(f"Error summing field: {ex}")

    async def average(self, condition: dict, field: str) -> Optional[float]:
        """ Calculate average of a numeric field based on condition """
        try:
            return await self.__model.objects.filter(**condition).aggregate(average=models.Avg(field))['average']
        except Exception as ex:
            raise Exception(f"Error calculating average: {ex}")