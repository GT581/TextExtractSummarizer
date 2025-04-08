import os
from typing import Optional
from fastapi import UploadFile, HTTPException

from app.core.config import get_settings
from app.core.logging import get_logger


logger = get_logger(__name__)


def save_upload_file(
    upload_file: UploadFile, 
    directory: Optional[str] = None, 
    filename: Optional[str] = None
) -> str:
    """
    Save an uploaded file to disk with error handling.
    
    Args:
        upload_file (UploadFile): The uploaded file
        directory (Optional[str]): Directory to save the file (uses settings if None)
        filename (Optional[str]): Filename to use (generates UUID if None)
        
    Returns:
        str: Path to the saved file
        
    Raises:
        HTTPException: If the file cannot be saved
    """
    # Get the upload directory
    settings = get_settings()
    save_dir = directory or settings.UPLOAD_DIR
    
    # Create full file path
    file_path = os.path.join(save_dir, filename)
    
    try:
        # Make sure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write file content
        with open(file_path, "wb") as f:
            contents = upload_file.file.read()
            f.write(contents)
            
        # Reset file cursor for future reads if needed
        upload_file.file.seek(0)
        
        logger.info(f"File saved successfully: {file_path}")

        return file_path
        
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

def handle_file_upload(file: UploadFile) -> str:
    """
    Handle file uploads and saving.
    
    Args:
        file (UploadFile): The uploaded file
        
    Returns:
        str: Path to the saved temporary file
        
    Raises:
        HTTPException: If uploaded file cannot be saved
    """
    # Save and return file path
    settings = get_settings()
    filename = f"{file.filename}"
    
    try:
        temp_file_path = save_upload_file(
            upload_file=file,
            directory=settings.UPLOAD_DIR,
            filename=filename
        )
        
        logger.info(f"File saved successfully: {temp_file_path}")

        return temp_file_path
    
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving uploaded file: {str(e)}")

def clean_temp_file(file_path: str) -> None:
    """
    Safely remove a temporary file if it exists.
    
    Args:
        file_path (str): Path to the file to remove
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            logger.debug(f"Temporary file removed: {file_path}")
        except Exception as e:
            logger.warning(f"Error removing temporary file: {str(e)}")