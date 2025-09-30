# ISDIP C++ Implementation

C++版本的ISDIP（Image Saliency Detection using Iterative Scanning and Directional Propagation）算法实现。

## 构建要求

- CMake 3.10+
- OpenCV 4.0+
- C++17编译器

## 构建步骤

```bash
mkdir build
cd build
cmake ..
make
```

## 使用方法

```bash
./isdip_demo
```

## 文件结构

- `include/` - 头文件
- `src/` - 源代码实现
- `src/utils/` - 工具类实现

## 算法特性

- 超像素分割（SLIC）
- 四方向扫描
- 多颜色空间特征（RGB+LAB+XYZ）
- 高效的C++实现