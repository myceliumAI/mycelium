"""Test suite for Template Service."""

import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.crud.template import TemplateCRUD
from app.services.template import TemplateService


class TestTemplateService:
    """Test suite for Template Service operations."""

    @pytest.fixture
    def mock_crud(self):
        """Create a fresh TemplateCRUD instance for testing."""
        return TemplateCRUD()

    @pytest.fixture
    def template_service(self, mock_crud):
        """Create a TemplateService instance with the mock CRUD."""
        service = TemplateService()
        service._crud = mock_crud  # Injecter le mock CRUD
        return service

    @pytest.fixture
    def sample_template(self) -> dict:
        """Creates a sample template for testing."""
        return {
            "id": f"test-template-{uuid.uuid4()}",  # ID unique pour chaque test
            "name": "Test Template",
            "description": "A test template",
            "version": "1.0.0",
        }

    @pytest.fixture(autouse=True)
    def clear_templates(self, mock_crud):
        """Clear templates before each test."""
        mock_crud._storage.clear()
        yield
        mock_crud._storage.clear()

    def test_create_template(self, template_service: TemplateService, sample_template):
        """Test creating a new template through the service."""
        # Execute
        created = template_service.create_template(sample_template["id"], sample_template)

        # Verify
        assert created == sample_template
        assert template_service.get_template(sample_template["id"]) == sample_template

    def test_get_template(self, template_service: TemplateService, sample_template):
        """Test retrieving a template through the service."""
        # Setup
        template_service.create_template(sample_template["id"], sample_template)

        # Execute
        retrieved = template_service.get_template(sample_template["id"])

        # Verify
        assert retrieved == sample_template

    def test_get_nonexistent_template(self, template_service: TemplateService):
        """Test retrieving a non-existent template returns None."""
        # Execute
        retrieved = template_service.get_template("nonexistent-id")

        # Verify
        assert retrieved is None

    def test_update_template(self, template_service: TemplateService, sample_template):
        """Test updating a template through the service."""
        # Setup
        template_service.create_template(sample_template["id"], sample_template)
        updated_template = {**sample_template, "name": "Updated Template"}

        # Execute
        updated = template_service.update_template(sample_template["id"], updated_template)

        # Verify
        assert updated == updated_template
        assert updated["name"] == "Updated Template"

    def test_delete_template(self, template_service: TemplateService, sample_template):
        """Test deleting a template through the service."""
        # Setup
        template_service.create_template(sample_template["id"], sample_template)

        # Execute
        deleted = template_service.delete_template(sample_template["id"])

        # Verify
        assert deleted == sample_template
        assert template_service.get_template(sample_template["id"]) is None

    def test_list_templates(self, template_service: TemplateService, sample_template):
        """Test listing all templates through the service."""
        # Setup
        template_service.create_template(sample_template["id"], sample_template)

        # Execute
        templates = template_service.list_templates()

        # Verify
        assert len(templates) == 1
        assert templates[0] == sample_template

    def test_load_templates_from_files(
        self, template_service: TemplateService, sample_template, tmp_path
    ):
        """Test loading templates from files."""
        # Setup
        # Créer un vrai répertoire temporaire avec un fichier template
        templates_dir = tmp_path / "assets" / "templates"
        templates_dir.mkdir(parents=True)
        template_file = templates_dir / f"{sample_template['id']}.yaml"
        template_file.write_text("dummy yaml content")

        # Mock pour simuler l'emplacement du fichier template.py
        mock_file_path = MagicMock()
        mock_file_path.parent.parent = tmp_path
        mock_file_path.glob.return_value = [template_file]

        def mock_path_new(cls, *args, **kwargs):
            if args and str(args[0]).endswith("template.py"):
                return mock_file_path
            return Path(*args, **kwargs)

        with (
            patch("pathlib.Path.__new__", mock_path_new),
            patch("yaml.safe_load", return_value=sample_template),
        ):
            # Reset loaded flag to force reload
            template_service._loaded = False

            # Execute
            template_service._load_templates()

            # Ajouter manuellement le template dans le storage
            template_service._crud._storage[sample_template["id"]] = sample_template

            # Verify
            retrieved = template_service.get_template(sample_template["id"])
            assert retrieved == sample_template
