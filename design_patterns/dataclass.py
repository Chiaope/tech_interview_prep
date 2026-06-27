from pydantic import BaseModel, Field, field_validator

class MyDataClass(BaseModel):
    my_field_1: int
    my_field_2: str
    my_alias_field: str = Field(alias="my_alias")
    my_default_field: str = "my_default_value"
    my_optional_field: str | None = None
    my_validate_field_1: list[int]
    my_validate_field_2: list[int]
    
    @field_validator("my_validate_field_1", "my_validate_field_2")
    @classmethod
    def validate_int_greater_than_zero(cls, v):
        if not all(isinstance(i, int) and i > 0 for i in v):
            raise ValueError("All elements must be integers greater than zero")
        return v


def check_data_class(data, data_class):
    try:
        data_class(**data)
        return True
    except Exception as e:
        print(f"Data validation error: {e}")
        return False

def main():
    check_data = {
        "my_field_1": "42", 
        "my_field_2": "Hello", 
        "my_alias": "World",
        "my_validate_field_1": [1, 2, 3],
        "my_validate_field_2": [4, 5, "abc"]
    }
    if check_data_class(check_data, MyDataClass):
        data = MyDataClass(**check_data)
        print(data.model_dump(by_alias=True))

if __name__ == "__main__":
    main()