"""Template CRUD related error classes."""


class TemplateCRUDError(Exception):
    """Base exception class for template CRUD operations."""

    pass


class TemplateNotFoundError(TemplateCRUDError):
    """Exception raised when a template is not found."""

    def __init__(self, template_id: str):
        self.message = f" ❌ Template with ID {template_id} not found"
        super().__init__(self.message)


class TemplateAlreadyExistsError(TemplateCRUDError):
    """Exception raised when attempting to create a template that already exists."""

    def __init__(self, template_id: str):
        self.message = f" ❌ Template with ID {template_id} already exists"
        super().__init__(self.message)


class TemplateBulkCreateError(TemplateCRUDError):
    """Exception raised when attempting to bulk create templates that already exist."""

    def __init__(self, template_ids: set[str]):
        self.message = f" ❌ Templates with IDs {template_ids} already exist"
        super().__init__(self.message)


class TemplateOperationError(TemplateCRUDError):
    """Exception raised when a template operation fails."""

    def __init__(self, operation: str):
        self.message = f" ❌ Failed to {operation} template"
        super().__init__(self.message)
