#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图片压缩工具，支持 PNG、JPG、WEBP、BMP、GIF、TIFF 等常见格式"""

import argparse
import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

# 支持的格式
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff'}

# 格式对应的输出扩展名
FORMAT_EXT_MAP = {
    'jpg': '.jpg',
    'jpeg': '.jpg',
    'png': '.png',
    'webp': '.webp',
}


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def get_output_path(input_path, output_path, target_format=None):
    """计算输出路径"""
    if output_path and os.path.isdir(output_path):
        # 输出到目录
        filename = os.path.basename(input_path)
        if target_format:
            name, _ = os.path.splitext(filename)
            filename = f"{name}{FORMAT_EXT_MAP.get(target_format, os.path.splitext(filename)[1])}"
        return os.path.join(output_path, filename)
    elif output_path:
        return output_path
    else:
        # 默认：原目录 + _compressed 后缀
        dirname, filename = os.path.split(input_path)
        name, ext = os.path.splitext(filename)
        if target_format:
            ext = FORMAT_EXT_MAP.get(target_format, ext)
        return os.path.join(dirname or '.', f"{name}_compressed{ext}")


def compress_single(input_path, output_path, args, stats):
    """压缩单个图片"""
    start_time = time.time()

    # 检查文件
    if not os.path.exists(input_path):
        if not args.Q:
            print(f"[错误] 文件不存在: {input_path}")
        stats['failed'] += 1
        return False

    # 检查格式
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        if not args.Q:
            print(f"[跳过] 不支持的格式: {input_path}")
        stats['skipped'] += 1
        return False

    # 计算输出路径
    final_output = get_output_path(input_path, output_path, args.F)

    # 覆盖保护
    if os.path.exists(final_output) and not args.f:
        if not args.Q:
            print(f"[跳过] 输出文件已存在: {final_output} (使用 -f 强制覆盖)")
        stats['skipped'] += 1
        return False

    # Dry run 模式
    if args.n:
        if not args.Q:
            print(f"[预览] {input_path} → {final_output}")
        stats['processed'] += 1
        return True

    try:
        input_size = os.path.getsize(input_path)

        with Image.open(input_path) as img:
            original_size = img.size

            # EXIF 自动旋转
            if not args.R:
                try:
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass  # 忽略 EXIF 处理错误

            # 转换模式（JPG 不支持透明通道）
            target_ext = ext
            if args.F:
                target_ext = '.' + args.F

            if img.mode in ('RGBA', 'P', 'LA') and target_ext in {'.jpg', '.jpeg'}:
                img = img.convert('RGB')

            # 尺寸缩放
            if args.s:
                new_width = int(img.width * args.s / 100)
                new_height = int(img.height * args.s / 100)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            elif args.m:
                if img.width > args.m or img.height > args.m:
                    ratio = min(args.m / img.width, args.m / img.height)
                    new_width = int(img.width * ratio)
                    new_height = int(img.height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 构建保存参数
            save_kwargs = {}

            if target_ext in {'.jpg', '.jpeg'}:
                save_kwargs['quality'] = args.q
                save_kwargs['optimize'] = True
                if args.p:
                    save_kwargs['progressive'] = True
                # 剥离 EXIF
                if args.e:
                    save_kwargs['exif'] = b''

            elif target_ext == '.webp':
                save_kwargs['quality'] = args.q
                save_kwargs['method'] = 4  # 更好的压缩
                if args.e:
                    save_kwargs['exif'] = b''

            elif target_ext == '.png':
                # quality 映射到 compress_level (反向)
                save_kwargs['compress_level'] = 9 - (args.q * 9 // 100)
                save_kwargs['optimize'] = True
                if args.p:
                    save_kwargs['interlace'] = True  # 隔行扫描
                # 低质量时量化颜色
                if args.q < 50:
                    img = img.quantize(colors=256)

            elif target_ext == '.gif':
                save_kwargs['optimize'] = True
                if args.q < 50:
                    img = img.quantize(colors=128)

            # 确保输出目录存在
            output_dir = os.path.dirname(final_output)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 保存图片
            img.save(final_output, **save_kwargs)

            # 输出结果
            output_size = os.path.getsize(final_output)
            ratio = (1 - output_size / input_size) * 100
            elapsed = time.time() - start_time

            if not args.Q:
                print(f"[OK] {os.path.basename(input_path)}")
                print(f"   {format_size(input_size)} -> {format_size(output_size)} (压缩率: {ratio:.1f}%)")
                if img.size != original_size:
                    print(f"   尺寸: {original_size[0]}x{original_size[1]} -> {img.size[0]}x{img.size[1]}")
                print(f"   耗时: {elapsed:.2f}s")

            stats['processed'] += 1
            stats['saved_bytes'] += (input_size - output_size)
            return True

    except Exception as e:
        if not args.Q:
            print(f"[错误] 压缩失败 {input_path}: {e}")
        stats['failed'] += 1
        return False


def collect_files(input_path, recursive=False):
    """收集要处理的文件列表"""
    input_path = Path(input_path)

    if input_path.is_file():
        return [str(input_path)]

    if input_path.is_dir():
        files = []
        pattern = '**/*' if recursive else '*'
        for f in input_path.glob(pattern):
            if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS:
                files.append(str(f))
        return files

    return []


def main():
    parser = argparse.ArgumentParser(
        description='图片压缩工具 - 支持批量、缩放、格式转换',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  -i img.jpg                      # 压缩单文件 (质量 80)
  -i img.jpg -q 50                # 质量 50
  -i ./imgs/ -o ./out/            # 批量处理目录
  -i ./imgs/ -r -q 70             # 递归处理
  -i img.jpg -s 50                # 缩小 50%
  -i img.jpg -m 1920              # 最大边 1920px
  -i img.png -F jpg               # PNG 转 JPG
  -i img.jpg -p -e                # Web优化 + 移除EXIF
        '''
    )

    # 输入输出
    parser.add_argument('-i', required=True, dest='input_file', metavar='PATH',
                        help='输入文件或目录')
    parser.add_argument('-o', dest='output_path', default=None, metavar='PATH',
                        help='输出路径 (默认: 原目录)')
    parser.add_argument('-r', action='store_true',
                        help='递归处理子目录 (仅目录有效)')

    # 压缩参数
    parser.add_argument('-q', type=int, default=80, metavar='N',
                        help='质量 0-100 (默认: 80)')

    # 尺寸控制
    parser.add_argument('-s', type=int, metavar='%',
                        help='缩放百分比')
    parser.add_argument('-m', type=int, metavar='PX',
                        help='最大尺寸(像素)')

    # 格式与优化
    parser.add_argument('-F', choices=['jpg', 'png', 'webp'], metavar='FMT',
                        help='转换格式')
    parser.add_argument('-p', action='store_true',
                        help='渐进式/隔行扫描 (Web优化)')
    parser.add_argument('-e', action='store_true',
                        help='移除 EXIF 元数据')
    parser.add_argument('-R', action='store_true',
                        help='禁用 EXIF 自动旋转')

    # 行为控制
    parser.add_argument('-f', action='store_true',
                        help='强制覆盖输出文件')
    parser.add_argument('-n', action='store_true',
                        help='预览模式 (不实际处理)')
    parser.add_argument('-Q', action='store_true',
                        help='静默模式')
    parser.add_argument('-j', type=int, default=4, metavar='N',
                        help='线程数 (默认: 4)')

    args = parser.parse_args()

    # 验证参数
    if not 0 <= args.q <= 100:
        print("错误: 质量参数必须在 0-100 之间")
        sys.exit(1)

    if args.s and (args.s <= 0 or args.s > 100):
        print("错误: 缩放百分比必须在 1-100 之间")
        sys.exit(1)

    if args.m and args.m <= 0:
        print("错误: 最大尺寸必须大于 0")
        sys.exit(1)

    # 收集文件
    input_path = Path(args.input_file)
    if args.r and input_path.is_file():
        if not args.Q:
            print("提示: -r 对文件输入无效")

    files = collect_files(args.input_file, args.r)

    if not files:
        print(f"未找到支持的图片文件: {args.input_file}")
        sys.exit(1)

    if not args.Q:
        print(f"找到 {len(files)} 个文件")
        if args.n:
            print("[预览模式]\n")

    # 处理统计
    stats = {'processed': 0, 'failed': 0, 'skipped': 0, 'saved_bytes': 0}
    start_time = time.time()

    # 单文件直接处理，多文件并行处理
    if len(files) == 1:
        compress_single(files[0], args.output_path, args, stats)
    else:
        with ThreadPoolExecutor(max_workers=args.j) as executor:
            futures = {
                executor.submit(compress_single, f, args.output_path, args, stats): f
                for f in files
            }
            for future in as_completed(futures):
                pass  # 结果已在 compress_single 中处理

    # 输出统计
    elapsed = time.time() - start_time
    if not args.Q:
        print(f"\n{'='*40}")
        print(f"完成! 成功:{stats['processed']} 失败:{stats['failed']} 跳过:{stats['skipped']}")
        if stats['saved_bytes'] > 0:
            print(f"节省: {format_size(stats['saved_bytes'])}")
        print(f"耗时: {elapsed:.2f}s")


if __name__ == '__main__':
    main()
