from typing import Any

import pytest

from app.crud.template import TemplateCRUD
from app.exceptions.crud.template import (
    TemplateAlreadyExistsError,
    TemplateBulkCreateError,
    TemplateNotFoundError,
)


@pytest.fixture
def template_crud() -> TemplateCRUD:
    """Creates a TemplateCRUD instance for testing."""
    return TemplateCRUD()


@pytest.fixture
def sample_template() -> dict[str, Any]:
    """Creates a sample template for testing."""
    return {
        "id": "test-template",
        "name": "Test Template",
        "description": "A test template",
        "version": "1.0.0",
    }


def test_create_template(template_crud: TemplateCRUD, sample_template: dict[str, Any]) -> None:
    """Test creating a new template."""
    created = template_crud.create_template(sample_template["id"], sample_template)
    assert created == sample_template


def test_create_duplicate_template(
    template_crud: TemplateCRUD,
    sample_template: dict[str, Any],
) -> None:
    """Test creating a duplicate template raises TemplateAlreadyExistsError."""
    template_crud.create_template(sample_template["id"], sample_template)

    with pytest.raises(TemplateAlreadyExistsError) as exc_info:
        template_crud.create_template(sample_template["id"], sample_template)
    assert str(exc_info.value) == f" ❌ Template with ID {sample_template['id']} already exists"


def test_read_template(template_crud: TemplateCRUD, sample_template: dict[str, Any]) -> None:
    """Test reading a template."""
    template_crud.create_template(sample_template["id"], sample_template)
    retrieved = template_crud.read_template(sample_template["id"])
    assert retrieved == sample_template


def test_read_nonexistent_template(template_crud: TemplateCRUD) -> None:
    """Test reading a non-existent template returns None."""
    retrieved = template_crud.read_template("nonexistent-id")
    assert retrieved is None


def test_update_template(template_crud: TemplateCRUD, sample_template: dict[str, Any]) -> None:
    """Test updating a template."""
    template_crud.create_template(sample_template["id"], sample_template)

    updated_template = {**sample_template, "name": "Updated Template"}
    updated = template_crud.update_template(sample_template["id"], updated_template)

    assert updated == updated_template
    assert updated["name"] == "Updated Template"


def test_update_nonexistent_template(
    template_crud: TemplateCRUD,
    sample_template: dict[str, Any],
) -> None:
    """Test updating a non-existent template raises TemplateNotFoundError."""
    with pytest.raises(TemplateNotFoundError) as exc_info:
        template_crud.update_template("nonexistent-id", sample_template)
    assert str(exc_info.value) == " ❌ Template with ID nonexistent-id not found"


def test_delete_template(template_crud: TemplateCRUD, sample_template: dict[str, Any]) -> None:
    """Test deleting a template."""
    template_crud.create_template(sample_template["id"], sample_template)
    deleted = template_crud.delete_template(sample_template["id"])

    assert deleted == sample_template
    assert template_crud.read_template(sample_template["id"]) is None


def test_delete_nonexistent_template(template_crud: TemplateCRUD) -> None:
    """Test deleting a non-existent template raises TemplateNotFoundError."""
    with pytest.raises(TemplateNotFoundError) as exc_info:
        template_crud.delete_template("nonexistent-id")
    assert str(exc_info.value) == " ❌ Template with ID nonexistent-id not found"


def test_list_templates(template_crud: TemplateCRUD, sample_template: dict[str, Any]) -> None:
    """Test listing all templates."""
    template_crud.create_template(sample_template["id"], sample_template)
    templates = template_crud.list_templates()

    assert len(templates) == 1
    assert templates[0] == sample_template


def test_bulk_create_templates(
    template_crud: TemplateCRUD,
    sample_template: dict[str, Any],
) -> None:
    """Test bulk creating templates."""
    templates = {
        sample_template["id"]: sample_template,
        "another-template": {**sample_template, "id": "another-template"},
    }

    created = template_crud.bulk_create_templates(templates)
    assert len(created) == 2
    assert all(template in created for template in templates.values())


def test_bulk_create_with_existing_template(
    template_crud: TemplateCRUD,
    sample_template: dict[str, Any],
) -> None:
    """Test bulk creating templates with an existing template raises TemplateBulkCreateError."""
    template_crud.create_template(sample_template["id"], sample_template)

    templates = {
        sample_template["id"]: sample_template,
        "another-template": {**sample_template, "id": "another-template"},
    }

    with pytest.raises(TemplateBulkCreateError) as exc_info:
        template_crud.bulk_create_templates(templates)
    expected_ids = {sample_template["id"]}
    assert str(exc_info.value) == f" ❌ Templates with IDs {expected_ids} already exist"
