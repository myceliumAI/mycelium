from typing import Any, Dict

from pydantic import BaseModel


class BaseModelWithExample(BaseModel):

    @classmethod
    def get_example(cls) -> Dict[str, Any]:
        """
        Create a dictionary with example data for all fields in the model.

        :return Dict[str, Any]: A dictionary representation of the model with example data.
        """
        example = {}
        for field_name, field in cls.model_fields.items():
            if field.json_schema_extra and "example" in field.json_schema_extra:
                example[field_name] = field.json_schema_extra["example"]
        return example
