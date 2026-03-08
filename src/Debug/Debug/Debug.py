import os
import sys
import inspect
from typing import Any
from datetime import datetime

class Debug:
    @staticmethod
    def _get_project_name() -> str:
        """获取项目文件夹名称（即当前工作目录的文件夹名）"""
        cwd = os.getcwd()
        return os.path.basename(cwd)
    
    @staticmethod
    def _get_script_name() -> str:
        """获取当前脚本文件名"""
        return os.path.basename(sys.argv[0])
    
    @staticmethod
    def _get_caller_info() -> str:
        """获取调用者的信息（文件名和行号）"""
        frame = inspect.currentframe()
        
        # 跳过Debug模块本身的帧
        while frame:
            # 获取当前帧的文件名
            filename = frame.f_code.co_filename
            if "debug" not in os.path.basename(filename):  # 找到第一个非Debug模块的帧
                return f"{os.path.basename(filename)}:{frame.f_lineno}"
            frame = frame.f_back
        
        return "unknown:0"
    
    @staticmethod
    def Log(obj: Any, timestamp: bool = True, caller_info: bool = True):
        """
        记录日志到文件
        
        Args:
            obj: 要记录的对象
            timestamp: 是否添加时间戳
            caller_info: 是否添加调用者信息
        """
        proj_name = Debug._get_project_name()
        
        # 确保Debug目录存在
        log_dir = "./debug"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = f"{log_dir}/{proj_name}.log"
        
        # 构建日志内容
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") if timestamp else ""
        
        if caller_info:
            caller = Debug._get_caller_info()
        else:
            caller = Debug._get_script_name()
        
        # 转换对象为字符串
        if isinstance(obj, (list, tuple, dict, set)):
            import pprint
            obj_str = pprint.pformat(obj, width=100, indent=2)
        else:
            obj_str = str(obj)
        
        # 构建完整的日志行
        log_parts = []
        if timestamp_str:
            log_parts.append(f"[{timestamp_str}]")
        
        log_parts.append(f"From {caller}:")
        log_parts.append(obj_str)
        
        log_line = " ".join(log_parts) + "\n" + "-" * 80 + "\n"
        
        # 写入文件
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)
    
    @staticmethod
    def ClearLog():
        """清空日志文件"""
        proj_name = Debug._get_project_name()
        log_dir = "./debug"
        log_file = f"{log_dir}/{proj_name}.log"
        
        if os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("")  # 清空文件
            print(f"已清空日志文件: {log_file}")
    
    @staticmethod
    def ReadLog() -> str:
        """读取整个日志文件内容"""
        proj_name = Debug._get_project_name()
        log_dir = "./debug"
        log_file = f"{log_dir}/{proj_name}.log"
        
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    @staticmethod
    def LogToConsole(obj: Any, level: str = "INFO"):
        """
        同时记录到日志和控制台
        
        Args:
            obj: 要记录的对象
            level: 日志级别 (INFO, WARNING, ERROR, DEBUG)
        """
        # 记录到文件
        Debug.Log(obj, timestamp=True, caller_info=True)
        
        # 打印到控制台
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_color = {
            "INFO": "\033[92m",    # 绿色
            "WARNING": "\033[93m",  # 黄色
            "ERROR": "\033[91m",    # 红色
            "DEBUG": "\033[94m",    # 蓝色
        }
        color = level_color.get(level, "\033[0m")
        reset = "\033[0m"
        
        print(f"{color}[{timestamp}][{level}]{reset} {obj}")
    
    @staticmethod
    def LogVariable(**kwargs):
        """记录多个变量及其值"""
        for var_name, var_value in kwargs.items():
            Debug.Log(f"{var_name} = {var_value}", timestamp=True, caller_info=True)
    
    @staticmethod
    def LogException(e: Exception, context: str = ""):
        """记录异常信息"""
        import traceback
        
        error_msg = f"异常发生{f'在 {context}' if context else ''}: {type(e).__name__}: {str(e)}"
        traceback_msg = traceback.format_exc()
        
        Debug.LogToConsole(error_msg, "ERROR")
        Debug.Log(f"{error_msg}\n{traceback_msg}", timestamp=True, caller_info=True)


if __name__ == "__main__":
    # 测试示例
    Debug.ClearLog()  # 清空之前的日志
    
    Debug.Log("简单的日志信息")
    
    Debug.LogToConsole("这条信息会同时输出到控制台和日志文件", "INFO")
    
    Debug.LogToConsole("这是一个警告", "WARNING")
    
    data = {"name": "测试", "values": [1, 2, 3, 4, 5]}
    Debug.Log(data)  # 漂亮的格式化输出字典
    
    x = 10
    y = 20
    Debug.LogVariable(x=x, y=y, result=x+y)  # 记录多个变量
    
    # 读取并显示日志
    print("\n=== 日志内容 ===")
    print(Debug.ReadLog())
    
    # 测试异常记录
    try:
        result = 1 / 0
    except Exception as e:
        Debug.LogException(e, "除法运算")