# Built-in Dependencies
from typing import Any, Callable, Optional, Type, TypeVar, List, Tuple
from copy import deepcopy

# Third-Party Dependencies
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

# https://github.com/pydantic/pydantic/issues/1223
# https://github.com/pydantic/pydantic/pull/3179
# https://github.com/pydantic/pydantic/issues/1673


Model = TypeVar("Model", bound=Type[BaseModel])


def optional(without_fields: List[str] | None = None) -> Callable[[Model], Model]:
    """A decorator that create a partial model.

    Args:
        model (Type[BaseModel]): BaseModel model.

    Returns:
        Type[BaseModel]: ModelBase partial model.
    """
    if without_fields is None:
        without_fields = []

    def wrapper(model: Type[Model]) -> Type[Model]:
        base_model: Type[Model] = model

        def make_field_optional(
            field: FieldInfo, default: Any = None
        ) -> Tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]  # type: ignore
            return new.annotation, new

        if without_fields:
            base_model = BaseModel  # type: ignore

        return create_model(
            model.__name__,
            __base__=base_model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()  # type: ignore
                if field_name not in without_fields
            },
        )

    return wrapper  # type: ignore
