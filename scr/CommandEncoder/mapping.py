"""
Mapping
"""
class Mapping(dict):
    def __init__(self, map_data: dict):
        data = {}
        for pre, the in map_data.items():
            if not isinstance(pre, (tuple, list)):
                pre = (pre,)
            for preimage in pre:
                data[preimage] = the
        super().__init__(data)
    
            


if __name__ == '__main__':
    # 测试字符串键
    a = Mapping({'a': 1})
    print(a['a'])  # 1
    
    # 测试列表键
    b = Mapping({('x', 'y'): 10})
    print(b['x'])  # 10
    print(b['y'])  # 10
    
    # 测试混合键
    c = Mapping({'a': 1, ('b', 'c'): 2})
    print(c)  # {'a': 1, 'b': 2, 'c': 2}