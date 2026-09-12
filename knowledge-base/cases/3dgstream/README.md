# 3DGStream: On-the-Fly Training of 3D Gaussians for Efficient Streaming of Photo-Realistic Free-Viewpoint Videos

![实际生成图](figure.png)

- **大类**：三维表示、重建与分子空间 (`three-d-reconstruction`)
- **来源**：[CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/html/Sun_3DGStream_On-the-Fly_Training_of_3D_Gaussians_for_Efficient_Streaming_of_CVPR_2024_paper.html)
- **参考切入点**：neural transformation cache and adaptive Gaussian addition
- **核心图意**：A compact neural transformation cache updates persistent 3D Gaussians frame by frame, while adaptive additions represent newly emerging content.
- **完整生产 prompt**：[prompt.txt](prompt.txt)（20,876 个非空白字符）
- **低空白筛查**：通过；内容网格占用 79.8%，最大连续空区 10.0%
- **人工目视检查**：通过

这是依据论文机制重新组织的 ImageGen 概念示意，不是论文原图、实验结果或人工 gold。生成时未输入原论文图像像素。使用时应借鉴信息组织、对象密度、分区和连线方式，并依据目标论文重新核验科学关系。
