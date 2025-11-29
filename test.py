import os
import glob
import nibabel as nib
import numpy as np

# 指向你的【处理后】文件夹
output_root = r"E:\MedicalData_Preprocessed"

# 搜索所有 .nii.gz 文件
processed_files = sorted(glob.glob(os.path.join(output_root, "**", "*.nii.gz"), recursive=True))

print(f"正在验证 {len(processed_files)} 个文件...\n")
print(f"{'文件名':<50} | {'最小值 (期望 -50)':<15} | {'最大值 (期望 250)':<15} | {'状态':<10}")
print("-" * 100)

error_count = 0

for filepath in processed_files:
    try:
        # 使用 nibabel 快速读取 (不经过 MONAI pipeline，直接看原始数据)
        nii = nib.load(filepath)
        data = nii.get_fdata()

        curr_min = np.min(data)
        curr_max = np.max(data)

        # 获取短文件名用于显示
        filename = os.path.basename(filepath)

        # 判断是否合格 (考虑到浮点数误差，用近似比较)
        # 注意：有时候背景填充值可能会被设为 -50 以外的值，但你的 Clampd 应该覆盖所有。
        is_valid = (curr_min >= -50.0) and (curr_max <= 250.0)

        status = "✅ 正常" if is_valid else "❌ 异常"
        if not is_valid:
            error_count += 1

        print(f"{filename:<50} | {curr_min:<15.2f} | {curr_max:<15.2f} | {status}")

    except Exception as e:
        print(f"读取文件失败: {filepath} - {e}")

print("-" * 100)
if error_count == 0:
    print("🎉 完美！所有文件的数值都在 [-50, 250] 范围内。")
else:
    print(f"⚠️ 警告：发现 {error_count} 个文件数值超出范围，请检查上表。")