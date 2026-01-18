import logging
from datetime import datetime
import os

def setup_logger():
    """Set up logging"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create log filename with timestamp
    log_filename = f"logs/donna_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('DonnaAI')
    logger.info("=" * 70)
    logger.info("Donna AI Session Started")
    logger.info("=" * 70)
    
    return logger

# Global logger instance
logger = setup_logger()