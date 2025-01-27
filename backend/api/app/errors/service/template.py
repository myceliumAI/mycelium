"""Template service related error classes."""


class TemplateServiceError(Exception):
    """Base exception class for template service operations."""

    pass


class TemplateLoadError(TemplateServiceError):
    """Exception raised when loading templates fails."""

    def __init__(self, template_file: str):
        self.message = f" ❌ Error loading template {template_file}"
        super().__init__(self.message)


class TemplateValidationError(TemplateServiceError):
    """Exception raised when template validation fails."""

    def __init__(self, template_file: str):
        self.message = f" ❌ Invalid JSON in template file: {template_file}"
        super().__init__(self.message)


class TemplateMissingIDError(TemplateServiceError):
    """Exception raised when a template file has no ID."""

    def __init__(self, template_file: str):
        self.message = f" ❌ Template file {template_file} has no ID"
        super().__init__(self.message)


class TemplateDirectoryNotFoundError(TemplateServiceError):
    """Exception raised when the templates directory is not found."""

    def __init__(self):
        self.message = " ⚠️ Templates directory not found"
        super().__init__(self.message)
