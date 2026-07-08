#!/usr/bin/env python3
"""
§4.3 线性映射与矩阵 — 配音生成脚本（SAPI5 + wave 拼接）
快速版：用 win32com 生成各段，用 Python wave 模块直接拼接，避免 ffmpeg amix bug。

用法:
    python generate_voiceover.py              # 生成配音 + 合成视频
    python generate_voiceover.py --audio-only # 只生成配音
    python generate_voiceover.py --dry-run    # 只打印旁白文本
"""

import subprocess
import sys
import struct
import os
from pathlib import Path

import win32com.client

# ============================================================
# 配音脚本
# ============================================================
VOICE_NAME = "Microsoft Huihui Desktop"
SPEECH_RATE = 1          # -10 ~ 10
SAMPLE_RATE = 22050      # SAPI5 默认采样率
TOTAL_DURATION = 318.7   # 视频总时长（秒）

SCRIPT = [
    # ===== Scene 01: 片头 + 引入 =====
    (0.5,   "高等代数学，第四版，谢启鸿。第四章，线性映射。"),
    (5.0,   "第四节三点三，线性映射与矩阵。从几何到代数的桥梁。"),
    (10.0,  "回顾一下，我们已经定义了线性空间之间的线性映射及其运算。"),
    (14.5,  "但是，线性映射是一个抽象的几何概念，不便于具体计算。"),
    (18.5,  "我们的目标是，把这个抽象概念代数化。"),
    (21.5,  "回顾第三章，取定基之后，线性空间与坐标空间是同构的。"),
    # ===== Scene 02: 引理 4.3.1 =====
    (25.5,  "借助基，把线性映射转化为矩阵运算。线性映射等价于矩阵。"),
    (30.0,  "引理四点三点一，线性映射由基向量的像完全确定。"),
    (34.0,  "设V、U是数域K上的线性空间，V的一组基为e一到en。"),
    (37.5,  "第一，若两个线性映射在基上取值相同，则它们处处相等。"),
    (41.5,  "第二，任意指定基向量的像，就存在唯一的线性映射满足条件。"),
    (45.5,  "来看几何演示。左边V空间中，alpha由基向量表出。右边U空间，一旦基向量的像给定，"),
    (51.0,  "phi of alpha就被强行唯一确定了。"),
    (54.5,  "严格证明。唯一性：展开psi of alpha，利用线性性和已知条件，得到psi等于phi。"),
    (62.5,  "存在性：定义phi of alpha为坐标与beta的线性组合，验证良定义、线性和边界条件。唯一性由前一部分立得。"),
    # ===== Scene 03: 表示矩阵的构造 =====
    (70.0,  "现在构造表示矩阵。设V是n维、U是m维，问题是phi of alpha的坐标是什么？"),
    (75.0,  "四点三点一式给出了基向量的像。关键想法：把phi of ei的坐标竖着排成一列。"),
    (80.0,  "系数竖排得到矩阵A。第i列就是phi of ei的坐标向量。这个m乘n矩阵就是表示矩阵。"),
    (86.0,  "四点三点二式给出坐标变换公式，写成矩阵形式就是mu向量等于A乘lambda向量。"),
    (91.0,  "注意，A恰好是系数表的转置。"),
    # ===== Scene 04: 定义 =====
    (94.0,  "定义四点三。矩阵A称为phi在给定基下的表示矩阵，记号T of phi等于A。"),
    (98.0,  "T从L of V,U到M m乘n of K。phi取定基之后，就被一个矩阵编码了。"),
    # ===== Scene 05: 定理 4.3.1 =====
    (103.0, "定理四点三点一。T是线性同构，即L of V,U同构于M m乘n of K，且交换图成立。"),
    (109.5, "交换图中，从V出发两条路径：先做phi再到eta二，与先做eta一再做phi A，结果相同。"),
    (116.5, "证明。T是线性映射可直接验证。T是双射：单射性由引理推得，满射性也由引理保证。"),
    # ===== Scene 06: 定理 4.3.2 =====
    (123.0, "定理四点三点二。再引入空间W和映射psi，结论是T of psi phi等于T of psi乘T of phi等于BA。"),
    (130.0, "矩阵乘法BA的几何意义：先做phi再做psi。"),
    (134.0, "证明。phi of alpha坐标为Alambda，psi of phi of alpha坐标为BAlambda，因此复合映射的表示矩阵为BA。"),
    # ===== Scene 07: L(V) =====
    (141.0, "特殊情形V等于U，取同一组基。考察线性变换空间L of V和n阶矩阵空间。"),
    (147.0, "定理四点三点三：T是线性同构，还保持乘法。证明由前两个定理立得。"),
    (153.0, "推论四点三点一：恒等映射对应单位矩阵。phi可逆当且仅当T of phi可逆，逆映射对应逆矩阵。"),
    # ===== Scene 08: 推论汇总 =====
    (161.0, "本节结论的桥梁意义：线性映射对应矩阵，加法对应加法，数乘对应数乘，复合对应乘积，可逆对应逆矩阵。"),
    (170.0, "映射复合对应矩阵乘积，这就是矩阵乘法定义的几何动机！"),
    # ===== Scene 09: 基变换动机 =====
    (175.0, "核心问题：同一个线性变换phi，在不同基下，表示矩阵会不同吗？"),
    (180.0, "一般地，A不等于B。那么它们之间有什么关系？提示：两组基之间有过渡矩阵P。"),
    # ===== Scene 10: 定理 4.3.4 =====
    (186.5, "几何演示。蓝色是标准e基，金色是旋转的f基。phi是关于y轴的反射。"),
    (192.0, "在e基下矩阵A为负一零零一；在f基下矩阵B为零一一零。同一个变换，两个不同的矩阵。"),
    (199.5, "定理四点三点四。过渡矩阵为P，则B等于P逆AP。这是本节的核心定理。"),
    (207.0, "证明思路。坐标关系图中，横箭头是A和B，纵箭头是P。lambda等于Pmu，xi等于Peta。"),
    (214.0, "Peta等于xi等于Alambda等于APmu，因此PB等于AP，最终B等于P逆AP。"),
    # ===== Scene 11: 相似矩阵 =====
    (224.0, "定义四点三点一。若存在可逆矩阵P使B等于P逆AP，则称A与B相似。"),
    (230.0, "几何意义：A和B表示同一个线性变换在不同基下的矩阵。"),
    # ===== Scene 12: 命题 4.3.1 =====
    (236.0, "命题四点三点一，相似是等价关系：自反性，对称性，传递性。"),
    (244.5, "定理四点三点四告诉我们，同一线性变换在不同基下的表示矩阵必然相似。"),
    # ===== Scene 13: 总结 =====
    (252.0, "本节小结。引理：线性映射由基向量的像唯一确定。定义：表示矩阵。"),
    (257.5, "定理一：T是线性同构。定理二：T保持乘法。定理三：L of V与Mn保持加法乘法。"),
    (264.0, "推论：phi可逆当且仅当T of phi可逆。核心：B等于P逆AP，相似矩阵。"),
    (271.5, "展望。能否找到一组好的基，使表示矩阵尽量简单？"),
    (277.0, "第六章研究特征值和对角化，第七章研究Jordan标准型。"),
    (283.0, "第四节三点三，是连接几何与代数最重要的桥梁章节。"),
]


def sapi5_generate_wav(text: str, output_path: str):
    """用 SAPI5 生成单个 WAV 文件"""
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voice = speaker.GetVoices(f"Name={VOICE_NAME}").Item(0)
    speaker.Voice = voice
    speaker.Rate = SPEECH_RATE

    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(output_path, 3)  # SSFMCreateForWrite
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()


def read_wav_pcm(path: str):
    """读取 WAV 文件，返回 (sample_rate, channels, bits_per_sample, pcm_data_bytes)"""
    import wave as _wave
    with _wave.open(path, 'rb') as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        bps = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())
    return sr, ch, bps, frames


def assemble_audio(segment_info, output_path: str):
    """
    用 Python wave 模块直接拼接音频。
    segment_info: [(start_sec, wav_path, duration_sec), ...]
    """
    import wave as _wave

    total_samples = int(TOTAL_DURATION * SAMPLE_RATE)
    # 16-bit mono
    total_bytes = total_samples * 2
    # 初始化全零缓冲区
    buffer = bytearray(total_bytes)

    for start, wav_path, dur in segment_info:
        sr, ch, bps, pcm = read_wav_pcm(str(wav_path))
        # 如果不是 22050Hz 16bit mono，需要转换
        if sr != SAMPLE_RATE or ch != 1 or bps != 2:
            # 用 ffmpeg 转换到标准格式
            converted = str(wav_path) + ".norm.wav"
            subprocess.run([
                "ffmpeg", "-y", "-i", str(wav_path),
                "-ar", str(SAMPLE_RATE), "-ac", "1", "-sample_fmt", "s16",
                converted
            ], capture_output=True)
            sr, ch, bps, pcm = read_wav_pcm(converted)
            os.remove(converted)

        offset_bytes = int(start * SAMPLE_RATE) * 2
        # 混合（叠加）到缓冲区，避免溢出做简单钳位
        for j in range(min(len(pcm), total_bytes - offset_bytes)):
            # 只处理 16-bit 对齐位置
            if j % 2 == 1:
                continue
            if j + 1 >= len(pcm):
                break
            # 读取新样本
            new_val = struct.unpack_from('<h', pcm, j)[0]
            # 读取已有样本
            if offset_bytes + j + 1 < total_bytes:
                old_val = struct.unpack_from('<h', buffer, offset_bytes + j)[0]
            else:
                old_val = 0
            # 叠加并钳位
            mixed = max(-32768, min(32767, old_val + new_val))
            struct.pack_into('<h', buffer, offset_bytes + j, mixed)

    # 写出最终 WAV
    with _wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(bytes(buffer))

    return True


def generate_audio(output_path: str, dry_run: bool = False):
    if dry_run:
        print("=" * 60)
        print("配音脚本预览（dry-run）")
        print("=" * 60)
        for start, text in SCRIPT:
            mins, secs = divmod(int(start), 60)
            print(f"  [{mins:02d}:{secs:02d}] {text}")
        print(f"\n最后一段起始: {SCRIPT[-1][0]:.1f}s, 视频总时长: {TOTAL_DURATION}s")
        return

    print(f"语音: {VOICE_NAME}, 语速: {SPEECH_RATE}")
    print(f"共 {len(SCRIPT)} 段旁白\n")

    segments_dir = Path(output_path).parent / "voice_segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

    # 逐段生成 WAV
    segment_files = []
    for i, (start, text) in enumerate(SCRIPT):
        seg_path = segments_dir / f"seg_{i:03d}.wav"
        print(f"  [{i+1:02d}/{len(SCRIPT)}] {text[:30]}...", end=" ", flush=True)
        sapi5_generate_wav(text, str(seg_path))
        # probe 时长
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(seg_path)],
            capture_output=True, text=True
        )
        dur = float(probe.stdout.strip() or 0)
        segment_files.append((start, seg_path, dur))
        print(f"{dur:.1f}s")

    print(f"\n拼接音频（wave 模块直接组装）...")
    wav_output = str(output_path).replace('.mp3', '.wav')
    assemble_audio(segment_files, wav_output)

    # 用 ffmpeg 转为 mp3（可选，减小体积）
    print("转换为 mp3...")
    result = subprocess.run([
        "ffmpeg", "-y", "-i", wav_output,
        "-ar", "22050", "-ac", "1", "-b:a", "128k",
        str(output_path)
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg 错误: {result.stderr[-500:]}")
        return False
    os.remove(wav_output)

    # 清理
    for _, seg_path, _ in segment_files:
        seg_path.unlink(missing_ok=True)
    try:
        segments_dir.rmdir()
    except OSError:
        pass

    size_mb = Path(output_path).stat().st_size / 1_048_576
    print(f"\n配音完成: {output_path} ({size_mb:.1f} MB)")
    return True


def merge_video_audio(video_path: str, audio_path: str, output_path: str):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(output_path)
    ]
    print(f"\n合并视频与配音...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg 错误: {result.stderr[-500:]}")
        return False
    size_mb = Path(output_path).stat().st_size / 1_048_576
    print(f"合并完成: {output_path} ({size_mb:.1f} MB)")
    return True


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    audio_only = "--audio-only" in args

    base_dir = Path(__file__).parent
    video_path = base_dir.parent.parent / "section43_complete_4k.mp4"
    audio_path = base_dir / "section43_voiceover.mp3"
    output_path = base_dir / "section43_with_voice.mp4"

    ok = generate_audio(str(audio_path), dry_run=dry_run)
    if not ok or dry_run or audio_only:
        return

    if not video_path.exists():
        print(f"视频文件不存在: {video_path}")
        return
    merge_video_audio(str(video_path), str(audio_path), str(output_path))


if __name__ == "__main__":
    main()
