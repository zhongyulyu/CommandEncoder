# 快速开始

## 安装

### 从源码安装

bash
git clone https://github.com/zhongyulyu/CommandEncoder.git
cd commandencoder
pip install -e .

### 创建项目

#### 创建项目文件

cd ~/path/to/your/project/
mkdir projectname && cd projectname

#### 配置库
mkdir .vscode && cd .vscode
cat > settings.json << 'EOF'
{
    "python.analysis.extraPaths": [
        "/home/imstop/Python/PythonProjects/CommandEncoder/src"
    ]
}
EOF

### 简单示例
touch exam.py
cat > exam.py << 'EOF'

from commandencoder.premanage import Premanage

print(Premanage.match(input()))

EOF


### 获取帮助

如果遇到问题：
1. 查看项目文档
2. 启用调试模式：`Premanage.enabledebug = True`
3. 检查日志文件：`debug/CommandEncoder.log`
4. 提交 Issue 到 GitHub 仓库

## 下一步

- [API 文档](api-reference.md)
- [示例代码](examples.md)
- [架构说明](docs/architecture.md) 
- [贡献指南](contributing.md) 
