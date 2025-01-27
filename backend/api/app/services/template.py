from pathlib import Path
from typing import Any

import yaml

from ..crud.template import template_crud
from ..utils.logger import get_logger


logger = get_logger(__name__)


class TemplateService:
    """Service class for managing templates."""

    def __init__(self):
        """Initialize the template service."""
        self._loaded = False
        self._ensure_templates_loaded()

    def create_template(self, template_id: str, template_data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new template.

        :param template_id: The ID of the template
        :param template_data: The template data
        :return: The created template
        :raises ValueError: If template already exists
        """
        return template_crud.create_template(template_id, template_data)

    def get_template(self, template_id: str) -> dict[str, Any] | None:
        """
        Get a template by its ID.

        :param template_id: The ID of the template to retrieve
        :return: The template if found, None otherwise
        """
        return template_crud.read_template(template_id)

    def update_template(self, template_id: str, template_data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing template.

        :param template_id: The ID of the template
        :param template_data: The new template data
        :return: The updated template
        :raises ValueError: If template doesn't exist
        """
        return template_crud.update_template(template_id, template_data)

    def delete_template(self, template_id: str) -> dict[str, Any]:
        """
        Delete a template.

        :param template_id: The ID of the template
        :return: The deleted template
        :raises ValueError: If template doesn't exist
        """
        return template_crud.delete_template(template_id)

    def list_templates(self) -> list[dict[str, Any]]:
        """
        List all available templates.

        :return: List of all templates
        """
        return template_crud.list_templates()

    def _ensure_templates_loaded(self) -> None:
        """Ensure templates are loaded from files."""
        if not self._loaded:
            self._load_templates()

    def _load_templates(self) -> None:
        """
        Load all templates from the templates directory.

        This method scans the templates directory and loads all YAML template files.
        """
        try:
            templates_dir = Path(__file__).parent.parent / "assets" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)

            templates_to_load = {}
            for template_file in templates_dir.glob("*.y*ml"):
                try:
                    # Load template data
                    template_data = yaml.safe_load(template_file.read_text(encoding="utf-8"))

                    # Add template ID based on filename
                    template_id = template_file.stem
                    template_data["id"] = template_id

                    # Store template
                    templates_to_load[template_id] = template_data
                    logger.debug(f" 💡 Loaded template: {template_id}")

                except yaml.YAMLError:
                    logger.exception(f" ❌ Invalid YAML in template file: {template_file}")
                except Exception:
                    logger.exception(f" ❌ Error loading template {template_file}")

            if templates_to_load:
                template_crud.bulk_create_templates(templates_to_load)
                logger.info(f" ✅ Loaded {len(templates_to_load)} templates")
            else:
                logger.warning(" ⚠️ No templates found in templates directory")

        except Exception:
            logger.exception(" ❌ Failed to load templates")
            raise  # Important de propager l'erreur pour éviter un état incohérent
        finally:
            self._loaded = True


# Singleton instance
template_service = TemplateService()
