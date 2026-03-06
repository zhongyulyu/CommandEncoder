import re
import numpy as np
from typing import Optional, Tuple
from Debug.Debug import Debug
from mapping import Mapping


class Premanage:
    mov_direction_map = Mapping({
        ('前', '前进', '向前', '往前'): np.array([1, 0, 0]),
        ('后', '后退', '向后', '往后'): np.array([-1, 0, 0]),
        ('左', '向左', '往左', '左移'): np.array([0, -1, 0]),
        ('右', '向右', '往右', '右移'): np.array([0, 1, 0]),
        
        
        ('左前', '左前方', '左前向', 'front left', '往左前', '向左前'): 
            np.array([-0.7071, 0.7071, 0]),
        ('右前', '右前方', '右前向', 'front right', '往右前', '向右前'): 
            np.array([0.7071, 0.7071, 0]),
        ('左后', '左后方', '左后向', 'back left', '往左后', '向左后'): 
            np.array([-0.7071, -0.7071, 0]),
        ('右后', '右后方', '右后向', 'back right', '往右后', '向右后'): 
            np.array([0.7071, -0.7071, 0]),
        
        
        ('上', '向上', '上升', 'up', 'upward'): np.array([0, 0, 1]),
        ('下', '向下', '下降', 'down', 'downward'): np.array([0, 0, -1]),
    })

    unit_map = Mapping({
        ('厘米', '公分', 'cm', 'centimeter'): 0.01,
        ('米', '公尺', 'm', 'meter'): 1.0,
    })

    chinese_mapping = {
        "digits": Mapping({
            ("零", "〇"): 0,
            ("一", "壹", "幺"): 1,
            ("二", "贰", "两"): 2,
            ("三", "叁"): 3,
            ("四", "肆"): 4,
            ("五", "伍"): 5,
            ("六", "陆"): 6,
            ("七", "柒"): 7,
            ("八", "捌"): 8,
            ("九", "玖"): 9,
            ("洞",): 0,
            ("幺",): 1,  
            ("拐",): 7,
            ("勾",): 9,
        }),
        "units": Mapping({
            ("十", "拾"): 10,
            ("百", "佰"): 100,
            ("千", "仟"): 1000,
            ("万", "萬"): 10000,
            ("亿", "億"): 100000000,
            ("兆",): 1000000000000,
        }),
        "special": Mapping({
            ("半", "一半"): 0.5,
            ("廿",): 20,
            ("卅",): 30,
            ("卌",): 40,
            ("对", "双"): 2,
        }),
        "separators": Mapping({
            ("点", "."): ".",  
        })
    }

    chinese_basic_mapping = Mapping({
        ("零", "〇"): 0,
        ("一", "壹", "幺"): 1,
        ("二", "贰", "两"): 2,
        ("三", "叁"): 3,
        ("四", "肆"): 4,
        ("五", "伍"): 5,
        ("六", "陆"): 6,
        ("七", "柒"): 7,
        ("八", "捌"): 8,
        ("九", "玖"): 9,
        ("洞",): 0,
        ("幺",): 1,  
        ("拐",): 7,
        ("勾",): 9,
        ("十",): 10,
        ("十一",): 11,
        ("十二",): 12,
        ("十三",): 13,
        ("十四",): 14,
        ("十五",): 15,
        ("十六",): 16,
        ("十七",): 17,
        ("十八",): 18,
        ("十九",): 19,
    })

    enabledebug = False
    

    @staticmethod
    def match_pattern(cmd, *pattern_lists):
        """
        匹配命令字符串与模式列表
        
        参数:
            cmd: 待匹配的命令字符串
            *pattern_lists: 可变数量的模式列表
            
        特殊标记:
            %f: 匹配数字（包括小数）
            %s: 匹配任意字符串（包括空字符串，非贪婪）
            %k: 匹配任意符号
            
        返回格式:
            按照匹配顺序返回结果
        """
        
        
        all_patterns = []
        
        def generate_combinations(current_pattern, depth, current_indices):
            if depth >= len(pattern_lists):
                all_patterns.append((current_pattern, current_indices.copy()))
                return
            
            for i, pattern in enumerate(pattern_lists[depth]):
                if pattern in ['%f', '%s', '%k']:
                    new_pattern = current_pattern + pattern
                    new_indices = current_indices + [(depth, i, pattern)]
                    generate_combinations(new_pattern, depth + 1, new_indices)
                else:
                    new_pattern = current_pattern + pattern
                    new_indices = current_indices + [(depth, i, pattern)]
                    generate_combinations(new_pattern, depth + 1, new_indices)
        
        generate_combinations("", 0, [])
        
        
        def get_pattern_priority(indices):
            """
            计算模式优先级：
            1. 普通文本长的优先
            2. 特殊标记少的优先
            3. 在列表前面的优先匹配更具体的模式
            """
            normal_text_len = 0
            special_count = 0
            
            for depth, idx, pattern in indices:
                if pattern in ['%f', '%s', '%k']:
                    special_count += 1
                else:
                    normal_text_len += len(pattern)
            return (-normal_text_len, special_count, indices)
        
        all_patterns.sort(key=lambda x: get_pattern_priority(x[1]))
        
        for pattern_str, indices in all_patterns:
            regex_parts = []
            
            for depth, idx, pattern in indices:
                if pattern == '%f':
                    regex_parts.append(r'([零一二三四五六七八九十百千万亿两0-9]+(?:\.[0-9]+)?)')
                elif pattern == '%s':
                    regex_parts.append(r'(.*?)')
                elif pattern == '%k':
                    regex_parts.append(r'([^\w\s]+)')
                else:
                    regex_parts.append(re.escape(pattern))
            
            regex_pattern = '^' + ''.join(regex_parts) + '$'
            
            match = re.match(regex_pattern, cmd)
            if match:
                matched_groups = match.groups()
                result = []
                group_idx = 0
                
                for depth, idx, pattern in indices:
                    if pattern in ['%f', '%s', '%k']:
                        if group_idx < len(matched_groups):
                            result.append(matched_groups[group_idx] or '')
                            group_idx += 1
                    else:
                        result.append(idx)
                
                return tuple(result)
        
        return None

    @staticmethod
    def match(command: str) -> dict:
        cmd = re.sub(r'(额|那个|\s+)', '', command)
        
        splited = re.split(r'[，。；,]', cmd)
        
        result = {}
        mov_sum = np.array([0,0,0])
        for s in splited:
            mov = Premanage.movematch(s)
            Debug.Log(s)
            mov_sum = mov + mov_sum
            
        
        return mov_sum
    
    @staticmethod
    def movematch(command: str) -> np.array:
        """
        match single move command
        return (x m,y m,z m)
        
        Args:
            command: cmd
            
        Returns:
            np.array: numpy array
        """
        
        if Premanage.enabledebug:
            Debug.Log(f"movematch 收到命令: '{command}'", timestamp=True, caller_info=True)
        
        cmd = command.strip().lower()
        
        if Premanage.enabledebug:
            Debug.Log(f"处理后命令: '{cmd}'", timestamp=True, caller_info=False)

        dir_key = list(Premanage.mov_direction_map.keys())
        unit_key = list(Premanage.unit_map.keys())

        raw_result = Premanage.match_pattern(cmd, ['%s'], dir_key, ['%s'], ['%f'], unit_key, ['%s'])
        if Premanage.enabledebug:
            Debug.LogVariable(raw_result=raw_result)

        if not raw_result:
            return np.array([0,0,0])
        dir_str = dir_key[raw_result[1]]
        unit_str = unit_key[raw_result[4]]

        dir_vec = Premanage.mov_direction_map[dir_str]
        unit = Premanage.unit_map[unit_str]
        distance = Premanage.parseInt(raw_result[3])

        return dir_vec * distance * unit




        
    
    @staticmethod
    def rotatematch(command: str):
        """
        匹配旋转指令
        预留接口，待实现
        """
        
        if Premanage.enabledebug:
            Debug.Log(f"rotatematch 收到命令: '{command}'", timestamp=True, caller_info=True)
        
        pass

    @staticmethod
    def parseInt(num_str: str) -> float:
        """
        解析字符串为浮点数
        目前只处理阿拉伯数字，后续可扩展支持汉字
        
        Args:
            num_str: 数字字符串
            
        Returns:
            Optional[float]: 解析后的浮点数，解析失败返回None
        """
        if Premanage.enabledebug:
            Debug.Log(f"parseInt 解析数字: '{num_str}'", timestamp=True, caller_info=True)
        
        try:
            result = float(num_str)
            if Premanage.enabledebug:
                Debug.LogVariable(parse_result=result)
            return result
        except ValueError:
            
            if Premanage.enabledebug:
                Debug.Log("尝试解析为阿拉伯数字失败，尝试中文数字解析", timestamp=False, caller_info=False)
            return Premanage._tryParseChineseInt(num_str)
    
    @staticmethod
    def _tryParseChineseInt(num_str: str) -> float:
        """
        尝试解析中文数字字符串
        
        Args:
            num_str: 中文数字字符串
            
        Returns:
            Optional[float]: 解析后的浮点数，解析失败返回None
        """

        try:
            return Premanage.chinese_basic_mapping[num_str]
        except KeyError:
            pass

        
            if Premanage.enabledebug:
                Debug.Log(f"_tryParseChineseInt 解析中文数字: '{num_str}'", timestamp=True, caller_info=True)
        
        
        try:
            decimals = 0
            unit = 1
            splited = num_str.split('点')
            if (len(splited) > 2):
                
                if Premanage.enabledebug:
                    Debug.LogToConsole(f"检测到多个小数点: '{num_str}'", "ERROR")
                raise TypeError("multiple decimal point detected.")
            
            if (len(splited) == 2):
                for i, c in enumerate(splited[1]):
                    try:
                        decimals += Premanage.chinese_mapping["digits"][c] * (10 ** -(i+1))
                    except KeyError:
                        
                        if Premanage.enabledebug:
                            Debug.LogToConsole(f"小数部分非中文字符: '{c}'", "WARNING")
            
            flat = ""
            if ('万' in splited[0]):
                
                if Premanage.enabledebug:
                    Debug.LogToConsole(f"无法解析大于10000的数字: '{num_str}'", "ERROR")
                raise ValueError("cannot decode value greater than 10000")
            
            try:
                inte = Premanage.chinese_basic_mapping[splited[0]]
            except KeyError:
                for c in splited[0]:
                    if (c in Premanage.chinese_mapping["digits"].keys()):
                        flat += c
                
                if (splited[0][-1] in Premanage.chinese_mapping["digits"]):
                    unit = Premanage.chinese_mapping["units"][splited[0][-2]] / 10
                else:
                    unit = Premanage.chinese_mapping["units"][splited[0][-1]]
                
                inte = 0.0
                for i, c in enumerate(flat[::-1]):
                    inte += Premanage.chinese_mapping["digits"][c] * (10 ** i)
                
                inte *= unit
            finally:
                
                result = inte + decimals
                
                
                if Premanage.enabledebug:
                    Debug.LogVariable(
                        chinese_input=num_str,
                        parsed_integer=inte,
                        parsed_unit=unit,
                        parsed_decimals=decimals,
                        final_result=result
                    )
                
                return result
            
        except Exception as e:
            
            if Premanage.enabledebug:
                Debug.LogException(e, f"解析中文数字时: '{num_str}'")
            return None

if __name__ == "__main__":
    Premanage.enabledebug = True
    print(Premanage.match("前进两米，然后下降100米，最后上升1000米"))