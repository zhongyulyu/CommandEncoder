# CommandEncoder

## 模块结构

### `src/CommandEncoder/AIbasic.py`

#### 类 `AI`
**功能**: AI聊天接口封装，支持DeepSeek API调用

**方法：**
- **`__init__(self, initial_command: str, api: str)`**  
  **功能**: 初始化AI聊天实例，设置系统角色和API配置  
  **参数**:
  - `initial_command`: 系统提示词，定义AI的角色和功能
  - `api`: DeepSeek API密钥

- **`chat(self, message: str, role="user", content=[], temp=0.7, stream=False)`**  
  **功能**: 向AI发送聊天请求并获取响应  
  **参数**:
  - `message`: 用户输入的消息内容
  - `role`: 消息角色，默认"user"
  - `content`: 对话历史记录，默认为空列表
  - `temp`: 温度参数，控制生成文本的随机性，范围0.0-2.0
  - `stream`: 是否使用流式输出，默认为False
  **返回**: OpenAI API响应对象

- **`premanage()`**  
  **功能**: 预留方法，暂无实现

---

### `src/CommandEncoder/premanage.py`

#### 类 `Premanage`
**功能**: 自然语言指令解析器，将中文指令转换为结构化向量

**方法：**
- **`match_pattern(cmd, *pattern_lists)`**  
  **功能**: 通用字符串模式匹配器，支持特殊标记  
  **参数**:
  - `cmd`: 待匹配的命令字符串
  - `*pattern_lists`: 可变数量的模式列表，支持嵌套模式
  **特殊标记**:
  - `%f`: 匹配数字（阿拉伯数字或中文数字）
  - `%s`: 匹配任意字符串（非贪婪）
  - `%k`: 匹配任意符号
  **返回**: 匹配成功的模式元组 或 None

- **`match(command: str) -> tuple[Actions, list]`**  
  **功能**: 解析复合移动指令，包含多个子指令  
  **参数**:
  - `command`: 复合移动指令字符串，可包含中文标点分隔
  **返回**: 元组(Actions对象, 编码列表)，Actions包含所有解析结果

- **`match_single(command: str) -> tuple[SingleAction, tuple]`**  
  **功能**: 解析单个移动指令  
  **参数**:
  - `command`: 单个移动指令字符串
  **返回**: 元组(SingleAction对象, (移动编码, 旋转编码))

- **`movematch(command: str) -> tuple[Offset|Setabs, list]`**  
  **功能**: 解析移动指令，返回移动向量  
  **参数**:
  - `command`: 单个移动指令字符串
  **处理流程**:
  1. 清理命令字符串
  2. 尝试匹配方向+距离+单位模式
  3. 失败则尝试匹配默认方向模式
  4. 计算移动向量
  **返回**: 元组(Offset或Setabs向量, 匹配编码列表)

- **`rotatematch(command: str) -> tuple[Offset|Setabs, list]`**  
  **功能**: 解析旋转指令，返回欧拉角向量  
  **参数**:
  - `command`: 旋转指令字符串
  **处理流程**:
  1. 清理命令字符串
  2. 尝试匹配旋转方向+角度+单位模式
  3. 失败则尝试匹配默认旋转模式
  4. 计算旋转向量
  **返回**: 元组(Offset或Setabs向量, 匹配编码列表)

- **`parseInt(num_str: str) -> float`**  
  **功能**: 数字字符串解析，支持阿拉伯数字和中文数字  
  **参数**:
  - `num_str`: 数字字符串
  **返回**: 解析后的浮点数，失败返回None

- **`_tryParseChineseInt(num_str: str) -> float`**  
  **功能**: 中文数字解析内部方法，支持中文数字和单位  
  **参数**:
  - `num_str`: 中文数字字符串
  **返回**: 解析后的浮点数 或 None

**静态属性：**
- `MOV_DIRECTION_MAP: Mapping` - 移动方向映射字典
- `ROT_DIRECTION_MAP: Mapping` - 旋转方向映射字典
- `MOV_DIRECTION_DEFULT: Mapping` - 默认移动方向映射
- `ROT_DIRECTION_DEFULT: Mapping` - 默认旋转方向映射
- `DISTANCE_UNIT_MAP: Mapping` - 距离单位映射
- `ANGLE_UNIT_MAP: Mapping` - 角度单位映射
- `CHINESE_MAPPING: dict` - 中文数字映射集合
- `CHINESE_BASIC_MAPPING: Mapping` - 基础中文数字映射
- `enabledebug: bool` - 调试模式开关

---

### `src/CommandEncoder/action.py`

#### 类 `Vector3`
**功能**: 三维向量类，扩展numpy.ndarray功能  
**继承自**: `numpy.ndarray`

**方法：**
- **`__new__(cls, data: Union[Tuple[float, float, float], List[float], np.ndarray] = (0, 0, 0))`**  
  **功能**: 创建Vector3实例  
  **参数**:
  - `data`: 三维向量数据，可以是元组、列表或numpy数组
  **返回**: Vector3实例

- **`length() -> float`**  
  **功能**: 计算向量的模长  
  **返回**: 向量的模长

- **`normalize() -> Vector3`**  
  **功能**: 计算单位向量  
  **返回**: 单位化后的Vector3

- **`dot(other: Vector3) -> float`**  
  **功能**: 计算与另一个向量的点积  
  **参数**:
  - `other`: 另一个Vector3向量
  **返回**: 点积结果

- **`cross(other: Vector3) -> Vector3`**  
  **功能**: 计算与另一个向量的叉积  
  **参数**:
  - `other`: 另一个Vector3向量
  **返回**: 叉积结果Vector3

**工厂方法：**
- `zero() -> Vector3` - 创建零向量 (0, 0, 0)
- `one() -> Vector3` - 创建单位向量 (1, 1, 1)
- `up() -> Vector3` - 创建上向量 (0, 1, 0)
- `right() -> Vector3` - 创建右向量 (1, 0, 0)
- `forward() -> Vector3` - 创建前向量 (0, 0, 1)

#### 类 `Offset`
**功能**: 相对移动向量，表示相对于当前位置的偏移  
**继承自**: `Vector3`

**方法：**
- **`__add__(self, other) -> Offset`**  
  **功能**: 向量加法  
  **参数**:
  - `other`: 另一个Offset或Setabs向量
  **规则**: Offset + Offset = Offset, Offset + Setabs = Offset(0,0,0)
  **返回**: Offset对象

- **`__mul__(self, scalar: float) -> Offset`**  
  **功能**: 标量乘法  
  **参数**:
  - `scalar`: 标量值
  **返回**: Offset对象

#### 类 `Setabs`
**功能**: 绝对位置向量，表示目标绝对坐标  
**继承自**: `Vector3`

**方法：**
- **`__add__(self, other) -> Offset`**  
  **功能**: 向量加法  
  **参数**:
  - `other`: 另一个Offset或Setabs向量
  **规则**: Setabs + Offset = Offset, Setabs + Setabs = Offset(0,0,0)
  **返回**: Offset对象

- **`__radd__(self, other) -> Offset`**  
  **功能**: 右加操作  
  **参数**:
  - `other`: 另一个向量
  **返回**: Offset对象

- **`__mul__(self, scalar: float) -> Setabs`**  
  **功能**: 标量乘法  
  **参数**:
  - `scalar`: 标量值
  **返回**: Setabs对象

#### 类 `SingleAction`
**功能**: 单个动作指令容器，包含位置和旋转信息  
**继承自**: `dict`

**方法：**
- **`__init__(self, iterable)`**  
  **功能**: 初始化单个动作  
  **参数**:
  - `iterable`: 可迭代对象
  **数据结构**:
    python
    {
      'pos': {
      'offset': Offset, # 相对位置偏移
      'absolute': Setabs # 绝对位置
      },
      'rot': {
      'offset': Offset, # 相对旋转偏移
      'absolute': Setabs # 绝对旋转角度
      }
    }

#### 类 `Actions`
**功能**: 动作序列容器，管理多个SingleAction  
**继承自**: `list[SingleAction]`

**方法：**
- **`__init__(self, iterable)`**  
**功能**: 初始化动作序列  
**参数**:
- `iterable`: 可迭代的SingleAction对象
**返回**: Actions对象

---

### `src/CommandEncoder/mapping.py`

#### 类 `Mapping`
**功能**: 更好的映射字典，可读性与扩展性更高，支持一对多映射  
**继承自**: `dict`

**方法：**
- **`__init__(self, map_data: dict)`**  
**功能**: 初始化映射字典  
**参数**:
- `map_data`: 映射数据字典，键可以是单个值或元组
**特点**: 支持多个键映射到同一个值

---

### `src/Debug/Debug/Debug.py`

#### 类 `Debug`
**功能**: 调试日志工具类，提供多级别日志记录

**公开方法：**
- **`Log(obj: Any, timestamp=True, caller_info=True)`**  
**功能**: 记录对象到日志文件  
**参数**:
- `obj`: 要记录的任何对象
- `timestamp`: 是否添加时间戳
- `caller_info`: 是否添加调用者信息
**输出位置**: 项目目录下的debug/项目名.log

- **`ClearLog()`**  
**功能**: 清空当前项目的日志文件  
**输出位置**: 控制台显示操作结果

- **`ReadLog() -> str`**  
**功能**: 读取当前项目的日志文件内容  
**返回**: 日志文件完整字符串内容

- **`LogToConsole(obj: Any, level="INFO")`**  
**功能**: 同时记录到日志和控制台  
**参数**:
- `obj`: 要记录的对象
- `level`: 日志级别，可选INFO/WARNING/ERROR/DEBUG
**特点**: 控制台输出带颜色，日志文件记录详细信息

- **`LogVariable(**kwargs)`**  
**功能**: 批量记录多个变量及其值  
**参数**:
- `**kwargs`: 变量名=变量值的键值对
**格式**: 每个变量单独一行，显示变量名和值

- **`LogException(e: Exception, context="")`**  
**功能**: 记录异常信息和堆栈跟踪  
**参数**:
- `e`: 异常对象
- `context`: 异常发生的上下文描述
**特点**: 同时记录到控制台(ERROR级别)和日志文件

**内部静态方法：**
- `_get_project_name() -> str` - 获取当前工作目录的文件夹名
- `_get_script_name() -> str` - 获取当前执行的脚本文件名
- `_get_caller_info() -> str` - 获取调用者的文件名和行号