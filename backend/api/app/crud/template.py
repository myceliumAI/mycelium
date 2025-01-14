import logging
from pathlib import Path
from typing import List, Optional

import yaml

from ..schemas.template.objects.template import Template
from ..utils.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Constants
TEMPLATE_FILE_SUFFIX = ".yaml"
TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"

# In-memory storage for templates
_templates_cache: List[Template] = []


def _load_templates() -> None:
    """
    Loads all templates from the filesystem into memory.
    This is called internally when needed to refresh the cache.
    """
    try:
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        global _templates_cache
        _templates_cache = []

        for template_file in TEMPLATES_DIR.glob(f"*{TEMPLATE_FILE_SUFFIX}"):
            try:
                template_data = yaml.safe_load(template_file.read_text())
                template_data["id"] = template_file.stem
                template = Template.model_validate(template_data)
                _templates_cache.append(template)
            except Exception as e:
                logger.error(f" ❌ Error loading template {template_file}: {str(e)}")
                continue
        logger.info(f" 💡 Loaded {len(_templates_cache)} templates into memory")
    except Exception as e:
        logger.error(f" ❌ Error loading templates: {str(e)}")
        raise


def get_template(id: str) -> Optional[Template]:
    """
    Retrieves a template from the in-memory cache by its ID.

    :param str id: The unique identifier of the template to retrieve.
    :return Optional[Template]: The retrieved template, or None if not found.
    :raises Exception: If there's any unexpected error.
    """
    try:
        if not _templates_cache:
            _load_templates()

        template = next((t for t in _templates_cache if t.id == id), None)
        if template is None:
            logger.warning(f" ⚠️ Template not found: {id}")
            return None

        logger.info(f" ✅ Template retrieved successfully: {id}")
        return template
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while retrieving template: {str(e)}")
        raise


def list_templates() -> List[Template]:
    """
    Retrieves all templates from the in-memory cache.

    :return List[Template]: A list of all templates.
    :raises Exception: If there's any unexpected error.
    """
    try:
        if not _templates_cache:
            _load_templates()

        logger.info(f" ✅ Retrieved {len(_templates_cache)} templates successfully")
        return _templates_cache
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while retrieving templates: {str(e)}")
        raise
