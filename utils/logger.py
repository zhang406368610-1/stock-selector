"""
日志配置模块
"""
import logging
import os
from datetime import datetime


class LoggerConfig:
    """日志配置类"""
    
    def __init__(self, log_dir='./logs'):
        self.log_dir = log_dir
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志系统"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 创建logger
        self.logger = logging.getLogger('StockSelector')
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件处理器
        log_file = os.path.join(
            self.log_dir,
            f"stock_selector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 添加格式化器到处理器
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """获取logger对象"""
        return self.logger


def get_logger(name='StockSelector'):
    """获取全局logger"""
    return logging.getLogger(name)