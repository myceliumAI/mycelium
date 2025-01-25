"""Template management module."""

import json
from pathlib import Path
from typing import Any

from ..utils.logger import get_logger


logger = get_logger(__name__)


class TemplateCache:
    """Manages template caching and operations."""

    def __init__(self):
        """Initialize the template cache."""
        self._cache: dict[str, dict[str, Any]] = {}
        self._loaded = False

    def get(self, template_id: str) -> dict[str, Any] | None:
        """
        Get a template by its ID from the cache.

        :param str template_id: The ID of the template to retrieve
        :return Optional[Dict[str, Any]]: The template if found, None otherwise
        """
        self._ensure_loaded()
        return self._cache.get(template_id)

    def list_all(self) -> list[dict[str, Any]]:
        """
        List all available templates.

        :return List[Dict[str, Any]]: List of all templates
        """
        self._ensure_loaded()
        return list(self._cache.values())

    def _ensure_loaded(self) -> None:
        """Ensure templates are loaded into cache."""
        if not self._loaded:
            self._load_templates()

    def _load_templates(self) -> None:
        """
        Load all templates from the templates directory.

        This method scans the templates directory and loads all JSON template files
        into the cache. Each template file should be a valid JSON file.
        """
        try:
            templates_dir = Path(__file__).parent.parent / "assets" / "templates"
            if not templates_dir.exists():
                logger.warning(" ⚠️ Templates directory not found")
                self._loaded = True
                return

            for template_file in templates_dir.glob("*.json"):
                try:
                    with template_file.open("r", encoding="utf-8") as f:
                        template_data = json.load(f)
                        template_id = template_data.get("id")
                        if template_id:
                            self._cache[template_id] = template_data
                            logger.debug(f" 💡 Loaded template: {template_id}")
                        else:
                            logger.warning(f" ⚠️ Template file {template_file} has no ID")
                except json.JSONDecodeError:
                    logger.exception(f" ❌ Invalid JSON in template file: {template_file}")
                except Exception:
                    logger.exception(f" ❌ Error loading template {template_file}")

            logger.info(f" ✅ Loaded {len(self._cache)} templates")
            self._loaded = True

        except Exception:
            logger.exception(" ❌ Failed to load templates")
            self._loaded = True  # Prevent repeated loading attempts


# Singleton instance
template_cache = TemplateCache()


def get_template(template_id: str) -> dict[str, Any] | None:
    """
    Retrieve a template by its ID.

    :param str template_id: The ID of the template to retrieve
    :return Optional[Dict[str, Any]]: The template if found, None otherwise
    """
    return template_cache.get(template_id)


def list_templates() -> list[dict[str, Any]]:
    """
    List all available templates.

    :return List[Dict[str, Any]]: List of all templates
    """
    return template_cache.list_all()
