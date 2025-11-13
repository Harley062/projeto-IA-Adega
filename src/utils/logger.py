"""
Módulo para configuração de logging
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = 'adega_ml', log_dir: str = 'logs', level: int = logging.INFO) -> logging.Logger:
    """
    Configura e retorna um logger

    Args:
        name: Nome do logger
        log_dir: Diretório para salvar logs
        level: Nível de logging

    Returns:
        Logger configurado
    """
    # Criar diretório de logs se não existir
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_path / f'{name}_{timestamp}.log'

    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remover handlers existentes para evitar duplicação
    if logger.handlers:
        logger.handlers.clear()

    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Adicionar handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logger inicializado. Logs salvos em: {log_file}")

    return logger
