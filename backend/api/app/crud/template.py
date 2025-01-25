import logging
from pathlib import Path

import yaml
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

from ..schemas.template.objects.template import Template
from ..utils.config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Constants
TEMPLATE_FILE_SUFFIX = ".yaml"
TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"

# In-memory storage for templates
_templates_cache: list[Template] = []


def _get_safe_template_path(template_id: str) -> Path | None:
    """
    Safely constructs a template file path, preventing path traversal attacks.

    :param str template_id: The template identifier to sanitize
    :return Optional[Path]: Safe path to the template file, or None if path is unsafe
    """
    try:
        # Sanitize the template ID
        safe_id = secure_filename(template_id)
        if not safe_id:
            logger.warning(f" ⚠️ Invalid template ID: {template_id}")
            return None

        # Safely join paths to prevent directory traversal
        safe_path = safe_join(str(TEMPLATES_DIR), f"{safe_id}{TEMPLATE_FILE_SUFFIX}")
        if safe_path is None:
            logger.warning(f" ⚠️ Unsafe template path detected for ID: {template_id}")
            return None

        return Path(safe_path)
    except Exception as e:
        logger.error(f" ❌ Error creating safe template path: {e!s}")
        return None


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
                # Verify the file path is safe
                safe_path = _get_safe_template_path(template_file.stem)
                if safe_path is None or safe_path != template_file:
                    logger.warning(f" ⚠️ Skipping unsafe template file: {template_file}")
                    continue

                template_data = yaml.safe_load(template_file.read_text())
                template_data["id"] = template_file.stem
                template = Template.model_validate(template_data)
                _templates_cache.append(template)
            except Exception as e:
                logger.error(f" ❌ Error loading template {template_file}: {e!s}")
                continue
        logger.info(f" 💡 Loaded {len(_templates_cache)} templates into memory")
    except Exception as e:
        logger.error(f" ❌ Error loading templates: {e!s}")
        raise


def get_template(id: str) -> Template | None:
    """
    Retrieves a template from the in-memory cache by its ID.

    :param str id: The unique identifier of the template to retrieve.
    :return Optional[Template]: The retrieved template, or None if not found.
    :raises Exception: If there's any unexpected error.
    """
    try:
        # Verify the template ID is safe
        if _get_safe_template_path(id) is None:
            logger.warning(f" ⚠️ Invalid template ID requested: {id}")
            return None

        if not _templates_cache:
            _load_templates()

        template = next((t for t in _templates_cache if t.id == id), None)
        if template is None:
            logger.warning(f" ⚠️ Template not found: {id}")
            return None

        logger.info(f" ✅ Template retrieved successfully: {id}")
        return template
    except Exception as e:
        logger.error(f" ❌ Unexpected error occurred while retrieving template: {e!s}")
        raise


def list_templates() -> list[Template]:
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
        logger.error(f" ❌ Unexpected error occurred while retrieving templates: {e!s}")
        raise
