import unittest

from api.models.data_contract import DataContract as DBDataContract
from app.schemas.data_contract.config_object import ConfigObject
from app.schemas.data_contract.contact_object import ContactObject
from app.schemas.data_contract.data_contract import DataContract as PydanticDataContract
from app.schemas.data_contract.definition_object import DefinitionObject
from app.schemas.data_contract.example_object import ExampleObject
from app.schemas.data_contract.field_object import FieldObject
from app.schemas.data_contract.info_object import InfoObject
from app.schemas.data_contract.model_object import ModelObject
from app.schemas.data_contract.quality_object import QualityObject
from app.schemas.data_contract.server_object import ServerObject
from app.schemas.data_contract.service_level_object import ServiceLevelObject
from app.schemas.data_contract.term_object import TermObject
from api.utils.tools import db_to_pydantic_model, pydantic_to_db_model


class TestTools(unittest.TestCase):
    """
    Test cases for the tools module.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.pydantic_data_contract = PydanticDataContract(
            data_contract_specification="0.9.3",
            id="urn:datacontract:checkout:orders-latest",
            info=InfoObject(
                title="Orders Latest",
                version="1.0.0",
                description="Successful customer orders in the webshop. All orders since 2020-01-01. Orders with their line items are in their current state (no history included).",
                owner="Checkout Team",
                contact=ContactObject(
                    name="John Doe (Data Product Owner)",
                    url="https://teams.microsoft.com/l/channel/example/checkout",
                ),
            ),
            tags=["checkout", "orders", "s3"],
            links={"datacontractCli": "https://cli.datacontract.com"},
            servers={
                "production": ServerObject(
                    type="s3",
                    environment="prod",
                    location="s3://datacontract-example-orders-latest/data/{model}/*.json",
                    format="json",
                    delimiter="new_line",
                    description="One folder per model. One file per day.",
                )
            },
            terms=TermObject(
                usage="Data can be used for reports, analytics and machine learning use cases. Order may be linked and joined by other tables",
                limitations="Not suitable for real-time use cases. Data may not be used to identify individual customers. Max data processing per day: 10 TiB",
                billing="5000 USD per month",
                notice_period="P3M",
            ),
            models={
                "orders": ModelObject(
                    description="One record per order. Includes cancelled and deleted orders.",
                    type="table",
                    fields={
                        "order_id": FieldObject(
                            type="text",
                            description="Unique identifier for the order",
                            required=True,
                            unique=True,
                            primary=True,
                        ),
                        "order_timestamp": FieldObject(
                            description="The business timestamp in UTC when the order was successfully registered in the source system and the payment was successful.",
                            type="timestamp",
                            required=True,
                            example="2024-09-09T08:30:00Z",
                        ),
                        "order_total": FieldObject(
                            description="Total amount the smallest monetary unit (e.g., cents).",
                            type="long",
                            required=True,
                            example="9999",
                        ),
                        "customer_id": FieldObject(
                            description="Unique identifier for the customer.",
                            type="text",
                            min_length=10,
                            max_length=20,
                        ),
                        "customer_email_address": FieldObject(
                            description="The email address, as entered by the customer. The email address was not verified.",
                            type="text",
                            format="email",
                            required=True,
                            pii=True,
                            classification="sensitive",
                        ),
                        "processed_timestamp": FieldObject(
                            description="The timestamp when the record was processed by the data platform.",
                            type="timestamp",
                            required=True,
                            config=ConfigObject(json_type="string", json_format="date-time"),
                        ),
                    },
                ),
                "line_items": ModelObject(
                    description="A single article that is part of an order.",
                    type="table",
                    fields={
                        "lines_item_id": FieldObject(
                            type="text",
                            description="Primary key of the lines_item_id table",
                            required=True,
                            unique=True,
                            primary=True,
                        ),
                        "order_id": FieldObject(
                            type="text",
                            description="An internal ID that identifies an order in the online shop.",
                            references="orders.order_id",
                        ),
                        "sku": FieldObject(
                            type="text",
                            description="A Stock Keeping Unit (SKU) is an internal unique identifier for an article. It is typically associated with an article's barcode, such as the EAN/GTIN.",
                            ref="#/definitions/sku",
                        ),
                    },
                ),
            },
            definitions={
                "order_id": DefinitionObject(
                    domain="checkout",
                    name="order_id",
                    title="Order ID",
                    type="text",
                    format="uuid",
                    description="An internal ID that identifies an order in the online shop.",
                    example="243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
                    pii=True,
                    classification="restricted",
                    tags=["orders"],
                ),
                "sku": DefinitionObject(
                    domain="inventory",
                    name="sku",
                    title="Stock Keeping Unit",
                    type="text",
                    pattern="^[A-Za-z0-9]{8,14}$",
                    example="96385074",
                    description="A Stock Keeping Unit (SKU) is an internal unique identifier for an article. It is typically associated with an article's barcode, such as the EAN/GTIN.",
                    links={"wikipedia": "https://en.wikipedia.org/wiki/Stock_keeping_unit"},
                    tags=["inventory"],
                ),
            },
            examples=[
                ExampleObject(
                    type="csv",
                    model="orders",
                    description="An example list of order records.",
                    data="order_id,order_timestamp,order_total,customer_id,customer_email_address,processed_timestamp\n"
                    '"1001","2030-09-09T08:30:00Z",2500,"1000000001","mary.taylor82@example.com","2030-09-09T08:31:00Z"\n'
                    '"1002","2030-09-08T15:45:00Z",1800,"1000000002","michael.miller83@example.com","2030-09-09T08:31:00Z"\n'
                    '"1003","2030-09-07T12:15:00Z",3200,"1000000003","michael.smith5@example.com","2030-09-09T08:31:00Z"\n'
                    '"1004","2030-09-06T19:20:00Z",1500,"1000000004","elizabeth.moore80@example.com","2030-09-09T08:31:00Z"\n'
                    '"1005","2030-09-05T10:10:00Z",4200,"1000000004","elizabeth.moore80@example.com","2030-09-09T08:31:00Z"\n',
                ),
                ExampleObject(
                    type="csv",
                    model="line_items",
                    description="An example list of line items.",
                    data="lines_item_id,order_id,sku\n"
                    '"LI-1","1001","5901234123457"\n'
                    '"LI-2","1001","4001234567890"\n'
                    '"LI-3","1002","5901234123457"\n'
                    '"LI-4","1002","2001234567893"\n'
                    '"LI-5","1003","4001234567890"\n',
                ),
            ],
            service_level=ServiceLevelObject(
                availability={"description": "The server is available during support hours", "percentage": "99.9%"},
                retention={"description": "Data is retained for one year", "period": "P1Y", "unlimited": False},
                latency={
                    "description": "Data is available within 25 hours after the order was placed",
                    "threshold": "25h",
                    "source_timestamp_field": "orders.order_timestamp",
                    "processed_timestamp_field": "orders.processed_timestamp",
                },
                freshness={
                    "description": "The age of the youngest row in a table.",
                    "threshold": "25h",
                    "timestamp_field": "orders.order_timestamp",
                },
                frequency={
                    "description": "Data is delivered once a day",
                    "type": "batch",
                    "interval": "daily",
                    "cron": "0 0 * * *",
                },
                support={
                    "description": "The data is available during typical business hours at headquarters",
                    "time": "9am to 5pm in EST on business days",
                    "response_time": "1h",
                },
                backup={
                    "description": "Data is backed up once a week, every Sunday at 0:00 UTC.",
                    "interval": "weekly",
                    "cron": "0 0 * * 0",
                    "recovery_time": "24 hours",
                    "recovery_point": "1 week",
                },
            ),
            quality=QualityObject(
                type="SodaCL",
                specification={
                    "type": "SodaCL",
                    "specification": """
                    checks for orders:
                      - row_count >= 5
                      - duplicate_count(order_id) = 0
                    checks for line_items:
                      - values in (order_id) must exist in orders (order_id)
                      - row_count >= 5
                    """,
                },
            ),
        )

        self.db_data_contract = DBDataContract(
            id="urn:datacontract:checkout:orders-latest",
            data_contract_specification="0.9.3",
            info={
                "title": "Orders Latest",
                "version": "1.0.0",
                "description": "Successful customer orders in the webshop. All orders since 2020-01-01. Orders with their line items are in their current state (no history included).",
                "owner": "Checkout Team",
                "contact": {
                    "name": "John Doe (Data Product Owner)",
                    "url": "https://teams.microsoft.com/l/channel/example/checkout",
                },
            },
            servers={
                "production": {
                    "type": "s3",
                    "environment": "prod",
                    "location": "s3://datacontract-example-orders-latest/data/{model}/*.json",
                    "format": "json",
                    "delimiter": "new_line",
                    "description": "One folder per model. One file per day.",
                }
            },
            terms={
                "usage": "Data can be used for reports, analytics and machine learning use cases. Order may be linked and joined by other tables",
                "limitations": "Not suitable for real-time use cases. Data may not be used to identify individual customers. Max data processing per day: 10 TiB",
                "billing": "5000 USD per month",
                "notice_period": "P3M",
            },
            models={
                "orders": {
                    "description": "One record per order. Includes cancelled and deleted orders.",
                    "type": "table",
                    "fields": {
                        "order_id": {
                            "type": "text",
                            "description": "Unique identifier for the order",
                            "required": True,
                            "unique": True,
                            "primary": True,
                        },
                        "order_timestamp": {
                            "description": "The business timestamp in UTC when the order was successfully registered in the source system and the payment was successful.",
                            "type": "timestamp",
                            "required": True,
                            "example": "2024-09-09T08:30:00Z",
                        },
                        "order_total": {
                            "description": "Total amount the smallest monetary unit (e.g., cents).",
                            "type": "long",
                            "required": True,
                            "example": "9999",
                        },
                        "customer_id": {
                            "description": "Unique identifier for the customer.",
                            "type": "text",
                            "min_length": 10,
                            "max_length": 20,
                        },
                        "customer_email_address": {
                            "description": "The email address, as entered by the customer. The email address was not verified.",
                            "type": "text",
                            "format": "email",
                            "required": True,
                            "pii": True,
                            "classification": "sensitive",
                        },
                        "processed_timestamp": {
                            "description": "The timestamp when the record was processed by the data platform.",
                            "type": "timestamp",
                            "required": True,
                            "config": {"json_type": "string", "json_format": "date-time"},
                        },
                    },
                },
                "line_items": {
                    "description": "A single article that is part of an order.",
                    "type": "table",
                    "fields": {
                        "lines_item_id": {
                            "type": "text",
                            "description": "Primary key of the lines_item_id table",
                            "required": True,
                            "unique": True,
                            "primary": True,
                        },
                        "order_id": {
                            "type": "text",
                            "description": "An internal ID that identifies an order in the online shop.",
                            "references": "orders.order_id",
                        },
                        "sku": {
                            "type": "text",
                            "description": "A Stock Keeping Unit (SKU) is an internal unique identifier for an article. It is typically associated with an article's barcode, such as the EAN/GTIN.",
                            "ref": "#/definitions/sku",
                        },
                    },
                },
            },
            definitions={
                "order_id": {
                    "domain": "checkout",
                    "name": "order_id",
                    "title": "Order ID",
                    "type": "text",
                    "format": "uuid",
                    "description": "An internal ID that identifies an order in the online shop.",
                    "example": "243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
                    "pii": True,
                    "classification": "restricted",
                    "tags": ["orders"],
                },
                "sku": {
                    "domain": "inventory",
                    "name": "sku",
                    "title": "Stock Keeping Unit",
                    "type": "text",
                    "pattern": "^[A-Za-z0-9]{8,14}$",
                    "example": "96385074",
                    "description": "A Stock Keeping Unit (SKU) is an internal unique identifier for an article. It is typically associated with an article's barcode, such as the EAN/GTIN.",
                    "links": {"wikipedia": "https://en.wikipedia.org/wiki/Stock_keeping_unit"},
                    "tags": ["inventory"],
                },
            },
            examples=[
                {
                    "type": "csv",
                    "model": "orders",
                    "description": "An example list of order records.",
                    "data": "order_id,order_timestamp,order_total,customer_id,customer_email_address,processed_timestamp\n"
                    '"1001","2030-09-09T08:30:00Z",2500,"1000000001","mary.taylor82@example.com","2030-09-09T08:31:00Z"\n'
                    '"1002","2030-09-08T15:45:00Z",1800,"1000000002","michael.miller83@example.com","2030-09-09T08:31:00Z"\n'
                    '"1003","2030-09-07T12:15:00Z",3200,"1000000003","michael.smith5@example.com","2030-09-09T08:31:00Z"\n'
                    '"1004","2030-09-06T19:20:00Z",1500,"1000000004","elizabeth.moore80@example.com","2030-09-09T08:31:00Z"\n'
                    '"1005","2030-09-05T10:10:00Z",4200,"1000000004","elizabeth.moore80@example.com","2030-09-09T08:31:00Z"\n',
                },
                {
                    "type": "csv",
                    "model": "line_items",
                    "description": "An example list of line items.",
                    "data": "lines_item_id,order_id,sku\n"
                    '"LI-1","1001","5901234123457"\n'
                    '"LI-2","1001","4001234567890"\n'
                    '"LI-3","1002","5901234123457"\n'
                    '"LI-4","1002","2001234567893"\n'
                    '"LI-5","1003","4001234567890"\n',
                },
            ],
            service_level={
                "availability": {"description": "The server is available during support hours", "percentage": "99.9%"},
                "retention": {"description": "Data is retained for one year", "period": "P1Y", "unlimited": False},
                "latency": {
                    "description": "Data is available within 25 hours after the order was placed",
                    "threshold": "25h",
                    "source_timestamp_field": "orders.order_timestamp",
                    "processed_timestamp_field": "orders.processed_timestamp",
                },
                "freshness": {
                    "description": "The age of the youngest row in a table.",
                    "threshold": "25h",
                    "timestamp_field": "orders.order_timestamp",
                },
                "frequency": {
                    "description": "Data is delivered once a day",
                    "type": "batch",
                    "interval": "daily",
                    "cron": "0 0 * * *",
                },
                "support": {
                    "description": "The data is available during typical business hours at headquarters",
                    "time": "9am to 5pm in EST on business days",
                    "response_time": "1h",
                },
                "backup": {
                    "description": "Data is backed up once a week, every Sunday at 0:00 UTC.",
                    "interval": "weekly",
                    "cron": "0 0 * * 0",
                    "recovery_time": "24 hours",
                    "recovery_point": "1 week",
                },
            },
            quality={
                "type": "SodaCL",
                "specification": {
                    "type": "SodaCL",
                    "specification": """
                    checks for orders:
                      - row_count >= 5
                      - duplicate_count(order_id) = 0
                    checks for line_items:
                      - values in (order_id) must exist in orders (order_id)
                      - row_count >= 5
                    """,
                },
            },
            links={"datacontractCli": "https://cli.datacontract.com"},
            tags=["checkout", "orders", "s3"],
        )

    def test_pydantic_to_db_model(self):
        """
        Test conversion from Pydantic model to DB model.
        """
        db_model = pydantic_to_db_model(self.pydantic_data_contract)

        self.assertIsInstance(db_model, DBDataContract)
        self.assertEqual(db_model.id, self.pydantic_data_contract.id)
        self.assertEqual(db_model.data_contract_specification, self.pydantic_data_contract.data_contract_specification)
        self.assertEqual(db_model.info, self.pydantic_data_contract.info.model_dump(mode="json"))
        self.assertEqual(
            db_model.servers,
            {k: v.model_dump(mode="json") for k, v in self.pydantic_data_contract.servers.items()},
        )
        # To continue with more tests

    def test_db_to_pydantic_model(self):
        """
        Test conversion from DB model to Pydantic model.
        """
        pydantic_model = db_to_pydantic_model(self.db_data_contract)

        self.assertIsInstance(pydantic_model, PydanticDataContract)
        self.assertEqual(pydantic_model.id, self.db_data_contract.id)
        self.assertEqual(pydantic_model.data_contract_specification, self.db_data_contract.data_contract_specification)

        # Remove None fields from the dumped model
        pydantic_info = pydantic_model.info.model_dump(mode="json", exclude_unset=True)
        self.assertEqual(pydantic_info, self.db_data_contract.info)

        pydantic_servers = {
            k: v.model_dump(mode="json", exclude_unset=True) for k, v in pydantic_model.servers.items()
        }
        self.assertEqual(pydantic_servers, self.db_data_contract.servers)

        # Additional assertions for other fields can be added here

    def test_bidirectional_conversion(self):
        """
        Test bidirectional conversion between Pydantic and DB models.
        """
        db_model = pydantic_to_db_model(self.pydantic_data_contract)
        converted_pydantic_model = db_to_pydantic_model(db_model)

        self.assertEqual(
            self.pydantic_data_contract.model_dump(mode="json"),
            converted_pydantic_model.model_dump(mode="json"),
        )


if __name__ == "__main__":
    unittest.main()
