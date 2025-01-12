import os
import yaml
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "templates")

@router.get("/templates")
async def list_templates() -> Dict[str, List[Dict[str, str]]]:
    """
    List all available templates.
    """
    try:
        if not os.path.exists(TEMPLATES_DIR):
            os.makedirs(TEMPLATES_DIR)
            logger.info(f"Created templates directory at {TEMPLATES_DIR}")
            return {"templates": []}

        templates = []
        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith('.yaml'):
                template_id = filename[:-5]  # Remove .yaml extension
                try:
                    with open(os.path.join(TEMPLATES_DIR, filename), 'r') as f:
                        template_data = yaml.safe_load(f)
                        templates.append({
                            "id": template_id,
                            "name": template_data.get("name", template_id),
                            "description": template_data.get("description", "")
                        })
                except Exception as e:
                    logger.error(f"Error loading template {filename}: {str(e)}")
                    continue
        
        logger.info(f"Found {len(templates)} templates")
        return {"templates": templates}
    except Exception as e:
        logger.error(f"Error loading templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading templates: {str(e)}")

@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """
    Retrieve the template configuration for a specific template.
    """
    template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.yaml")
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail=f"Template {template_id} not found")
        
    try:
        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading template: {str(e)}") 