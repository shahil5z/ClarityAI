from deep_translator import GoogleTranslator
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class DocumentTranslator:
    def __init__(self):
        self.supported_languages = Config.SUPPORTED_LANGUAGES
    
    def translate(self, text: str, target_language: str) -> str:
        """Translate text to the target language."""
        try:
            if target_language.lower() == "en":
                return text
            
            logger.info(f"Translating text to {target_language}")
            
            # Map language codes
            lang_code = "de" if target_language.lower() == "german" else target_language.lower()
            
            # Translate text
            translated_text = GoogleTranslator(source='auto', target=lang_code).translate(text)
            
            logger.info("Translation completed successfully")
            return translated_text
        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            raise