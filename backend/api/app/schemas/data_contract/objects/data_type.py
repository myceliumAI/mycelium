from enum import Enum


class DataType(str, Enum):
    """
    Enumeration of supported data types for model fields and definitions.
    """

    STRING = "string"
    TEXT = "text"
    VARCHAR = "varchar"
    NUMBER = "number"
    DECIMAL = "decimal"
    NUMERIC = "numeric"
    INT = "int"
    INTEGER = "integer"
    LONG = "long"
    BIGINT = "bigint"
    FLOAT = "float"
    DOUBLE = "double"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    TIMESTAMP_TZ = "timestamp_tz"
    TIMESTAMP_NTZ = "timestamp_ntz"
    DATE = "date"
    ARRAY = "array"
    MAP = "map"
    BYTES = "bytes"
    OBJECT = "object"
    RECORD = "record"
    STRUCT = "struct"
    NULL = "null"
