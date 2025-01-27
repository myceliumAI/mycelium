"""Template CRUD operations module."""

from typing import Any

from ..exceptions.crud.template import (
    TemplateAlreadyExistsError,
    TemplateBulkCreateError,
    TemplateNotFoundError,
)


class TemplateCRUD:
    """CRUD operations for templates."""

    def __init__(self):
        """Initialize the template storage."""
        self._storage: dict[str, dict[str, Any]] = {}

    def create_template(self, template_id: str, template_data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new template.

        :param template_id: The ID of the template
        :param template_data: The template data to store
        :return: The created template
        :raises TemplateAlreadyExistsError: If template with given ID already exists
        """
        if template_id in self._storage:
            raise TemplateAlreadyExistsError(template_id)

        self._storage[template_id] = template_data
        return template_data

    def read_template(self, template_id: str) -> dict[str, Any] | None:
        """
        Read a template by its ID.

        :param template_id: The ID of the template to retrieve
        :return: The template if found, None otherwise
        """
        return self._storage.get(template_id)

    def update_template(self, template_id: str, template_data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing template.

        :param template_id: The ID of the template to update
        :param template_data: The new template data
        :return: The updated template
        :raises TemplateNotFoundError: If template with given ID doesn't exist
        """
        if template_id not in self._storage:
            raise TemplateNotFoundError(template_id)

        self._storage[template_id] = template_data
        return template_data

    def delete_template(self, template_id: str) -> dict[str, Any]:
        """
        Delete a template.

        :param template_id: The ID of the template to delete
        :return: The deleted template
        :raises TemplateNotFoundError: If template with given ID doesn't exist
        """
        if template_id not in self._storage:
            raise TemplateNotFoundError(template_id)

        return self._storage.pop(template_id)

    def list_templates(self) -> list[dict[str, Any]]:
        """
        List all templates.

        :return: List of all templates
        """
        return list(self._storage.values())

    def bulk_create_templates(self, templates: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Create multiple templates at once.

        :param templates: Dictionary of template_id to template_data mappings
        :return: List of created templates
        :raises TemplateBulkCreateError: If any template ID already exists
        """
        existing = set(templates.keys()) & set(self._storage.keys())
        if existing:
            raise TemplateBulkCreateError(existing)

        self._storage.update(templates)
        return list(templates.values())


# Singleton instance
template_crud = TemplateCRUD()
