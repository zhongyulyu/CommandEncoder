import numpy as np
from typing import Union, Tuple, List

class Vector3(np.ndarray):
    """
    3d vector
    """
    
    def __new__(cls, 
                data: Union[Tuple[float, float, float], List[float], np.ndarray] = (0, 0, 0)):
        if isinstance(data, (tuple, list)):
            if len(data) != 3:
                raise ValueError("Vector3 requires exactly 3 elements")
            arr = np.array(data, dtype=np.float64)
        elif isinstance(data, np.ndarray):
            if data.shape != (3,):
                raise ValueError("Vector3 requires shape (3,)")
            arr = data.astype(np.float64)
        else:
            raise TypeError("Data must be tuple, list or ndarray")
        
        obj = arr.view(cls)
        return obj
    
    def __init__(self, data=(0, 0, 0)):
        # 为方便访问，添加x,y,z属性
        self._update_xyz()
    
    def _update_xyz(self):
        """更新x,y,z属性"""
        self.x = self[0]
        self.y = self[1]
        self.z = self[2]
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._update_xyz()
    
    # 向量运算方法
    def length(self) -> float:
        """向量的模长"""
        return np.sqrt(self.dot(self))
    
    def normalize(self) -> 'Vector3':
        """单位化向量"""
        l = self.length()
        if l > 0:
            return Vector3(self / l)
        return Vector3([0, 0, 0])
    
    def dot(self, other: 'Vector3') -> float:
        """点积"""
        if not isinstance(other, Vector3):
            other = Vector3(other)
        return np.dot(self, other)
    
    def cross(self, other: 'Vector3') -> 'Vector3':
        """叉积"""
        if not isinstance(other, Vector3):
            other = Vector3(other)
        return Vector3(np.cross(self, other))
    
    # 特殊方法
    def __str__(self) -> str:
        return f"Vector3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
    def __repr__(self) -> str:
        return f"Vector3([{self.x}, {self.y}, {self.z}])"
    
    # 运算重载
    def __add__(self, other: 'Vector3') -> 'Vector3':
        if not isinstance(other, Vector3):
            other = Vector3(other)
        return Vector3(super().__add__(other))
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        if not isinstance(other, Vector3):
            other = Vector3(other)
        return Vector3(super().__sub__(other))
    
    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(super().__mul__(scalar))
    
    def __truediv__(self, scalar: float) -> 'Vector3':
        return Vector3(super().__truediv__(scalar))
    
    # 工厂方法
    @classmethod
    def zero(cls) -> 'Vector3':
        """零向量 (0, 0, 0)"""
        return cls([0, 0, 0])
    
    @classmethod
    def one(cls) -> 'Vector3':
        """(1, 1, 1)"""
        return cls([1, 1, 1])
    
    @classmethod
    def up(cls) -> 'Vector3':
        """上向量 (0, 1, 0)"""
        return cls([0, 1, 0])
    
    @classmethod
    def right(cls) -> 'Vector3':
        """右向量 (1, 0, 0)"""
        return cls([1, 0, 0])
    
    @classmethod
    def forward(cls) -> 'Vector3':
        """前向量 (0, 0, 1)"""
        return cls([0, 0, 1])

class Offset(Vector3):
    def __init__(self, data=(0, 0, 0)):
        super().__init__(data)
    def __add__(self, other):
        if (isinstance(other, Offset)):
            return Offset(super().__add__(other))
        elif (isinstance(other, Setabs)):
            return Offset(Vector3.zero())
    def __mul__(self, scalar: float):
        return Offset(super().__mul__(scalar))
    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"
    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"
        

class Setabs(Vector3):
    def __init__(self, data=(0, 0, 0)):
        super().__init__(data)
    
    def __add__(self, other):
        if (isinstance(other, Offset)):
            return Offset(super().__add__(other))
        elif (isinstance(other, Setabs)):
            return Offset(Vector3.zero())

    def __radd__(self, other):
        return Offset(Vector3.zero())

    def __mul__(self, scalar: float):
        return Setabs(super().__mul__(scalar))
    
    def __str__(self):
        return f"abs pos: [{self.x}, {self.y}, {self.z}]"
    def __repr__(self):
        return f"abs pos: [{self.x}, {self.y}, {self.z}]"

if __name__ == '__main__':
    a = Offset([0,1,1])
    b = Setabs([0,1,0])
    print(a+b)