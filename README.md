# CommandEncoder

## 模块结构

### `src/CommandEncoder/AIbasic.py`

#### 类 `AI`

**方法：**
- **`__init__(self, initial_command: str, api: str)`**  
  - `initial_command`: 系统提示词
  - `api`: API密钥

- **`chat(self, message: str, role="user", content=[], temp=0.7, stream=False)`**  
  - `message`: 用户消息
  - `role`: 角色（默认"user"）
  - `content`: 对话历史
  - `temp`: 温度参数（默认0.7）
  - `stream`: 是否流式输出（默认False）
  - **返回**: AI响应对象

- **`premanage()`**  
  预留方法，无参数

---

### `src/CommandEncoder/premanage.py`

#### 类 `Premanage`

**方法：**
- **`match_pattern(cmd, *pattern_lists)`**  
  - `cmd`: 待匹配的命令字符串
  - `*pattern_lists`: 可变数量的模式列表
  - **返回**: 匹配结果元组 或 None

- **`match(command: str) -> dict`**  
  - `command`: 复合移动指令字符串
  - **返回**: 移动向量总和字典

- **`movematch(command: str) -> np.array`**  
  - `command`: 单个移动指令字符串
  - **返回**: 三维移动向量

- **`rotatematch(command: str)`**  
  - `command`: 旋转指令字符串
  - **返回**: 预留接口，待实现

- **`parseInt(num_str: str) -> float`**  
  - `num_str`: 数字字符串
  - **返回**: 解析后的浮点数

- **`_tryParseChineseInt(num_str: str) -> float`**  
  - `num_str`: 中文数字字符串
  - **返回**: 解析后的浮点数 或 None

**属性：**
- `mov_direction_map: Mapping` - 移动方向映射字典
- `unit_map: Mapping` - 单位映射字典
- `chinese_mapping: dict` - 中文数字映射
- `chinese_basic_mapping: Mapping` - 基础中文数字映射
- `enabledebug: bool` - 调试模式开关

---

### `src/CommandEncoder/mapping.py`

#### 类 `Mapping`

**方法：**
- **`__init__(self, map_data: dict)`**  
  - `map_data`: 映射数据字典
  - 支持键为元组的映射

---

### `src/Debug/Debug/Debug.py`

#### 类 `Debug`

**公开方法：**
- **`Log(obj: Any, timestamp=True, caller_info=True)`**  
  - `obj`: 要记录的对象
  - `timestamp`: 是否添加时间戳
  - `caller_info`: 是否添加调用者信息

- **`ClearLog()`**  
  无参数，清空日志文件

- **`ReadLog() -> str`**  
  - **返回**: 日志文件完整内容

- **`LogToConsole(obj: Any, level="INFO")`**  
  - `obj`: 要记录的对象
  - `level`: 日志级别（INFO/WARNING/ERROR/DEBUG）

- **`LogVariable(**kwargs)`**  
  - `**kwargs`: 变量名=变量值的键值对

- **`LogException(e: Exception, context="")`**  
  - `e`: 异常对象
  - `context`: 异常发生的上下文描述

**内部静态方法：**
- `_get_project_name() -> str` - 获取项目名称
- `_get_script_name() -> str` - 获取脚本文件名
- `_get_caller_info() -> str` - 获取调用者信息