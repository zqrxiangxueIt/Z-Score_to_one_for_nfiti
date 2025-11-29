import os
import glob
import torch
import numpy as np
from monai.transforms import (
    LoadImaged,
    EnsureChannelFirstd,
    Orientationd,
    ScaleIntensityRanged,
    Compose,
    SaveImage
)
from monai.data import Dataset, DataLoader

# 1. 设置路径 (请确认路径无误)
input_root = r"E:\MedicalData_Cleaned_NIfTI"
output_root = r"E:\MedicalData_Preprocessed"

# 2. 搜索文件
image_paths = sorted(glob.glob(os.path.join(input_root, "**", "*.nii.gz"), recursive=True))
print(f"共发现 {len(image_paths)} 个文件待处理。")

# 3. 定义预处理流水线
preprocess_transforms = Compose([
    LoadImaged(keys=["image"]),
    EnsureChannelFirstd(keys=["image"]),
    Orientationd(keys=["image"], axcodes="RAS"),

    # 截断数值到 -50 ~ 250
    ScaleIntensityRanged(
        keys=["image"],
        a_min=-50.0,
        a_max=250.0,
        b_min=-50.0,
        b_max=250.0,
        clip=True
    )
])

# 4. 创建数据集
ds = Dataset(data=[{"image": i} for i in image_paths], transform=preprocess_transforms)
loader = DataLoader(ds, batch_size=1, shuffle=False)

# 5. 定义保存器
saver = SaveImage(output_dir=output_root, output_postfix="", separate_folder=False, print_log=False)

print("\n--- 开始批量处理并保存 ---")

try:
    for i, batch_data in enumerate(loader):
        # 获取图像数据 (这是一个 MetaTensor，包含了元数据)
        img_tensor = batch_data["image"]

        # --- 修改点 1: 从 Tensor 内部获取路径 ---
        # 新版 MONAI 中，元数据在 .meta 属性里
        filename_or_obj = img_tensor.meta["filename_or_obj"]

        # 处理 batch 维度带来的列表包裹
        if isinstance(filename_or_obj, list):
            original_path = filename_or_obj[0]
        else:
            original_path = filename_or_obj

        # 计算保存路径 (保持目录结构)
        relative_path = os.path.relpath(original_path, input_root)
        target_folder = os.path.dirname(os.path.join(output_root, relative_path))

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # --- 修改点 2: 保存 ---
        saver.output_dir = target_folder

        # 直接传入 img_tensor[0]，因为它本身就携带了 metadata，不需要再传 meta_data参数
        saver(img_tensor[0])

        print(f"[{i + 1}/{len(image_paths)}] 已保存: {relative_path}")

    print("\n处理完成！所有文件已保存至:", output_root)

except Exception as e:
    print("\n运行出错详细信息:")
    import traceback

    traceback.print_exc()