#!/usr/bin/env python3
"""
§4.3 线性映射与矩阵 — 全场景渲染 & 合并脚本
用法:
    python3 render_all.py              # 低质量预览 (480p15)
    python3 render_all.py --hq         # 高清输出 (1080p60)
    python render_all.py --4k         # 4K (2160p60)
    python3 render_all.py --scene 10   # 只渲染第 10 个场景
"""

import subprocess, sys, os, shutil
from pathlib import Path

SCENES = [
    "Scene01_Title",
    "Scene02_Lemma",
    "Scene03_BuildMatrix",
    "Scene04_Definition",
    "Scene05_Theorem1",
    "Scene06_Theorem2",
    "Scene07_LVCase",
    "Scene08_Corollary",
    "Scene09_Bridge",
    "Scene10_Theorem4",
    "Scene11_SimilarDef",
    "Scene12_Proposition",
    "Scene13_Summary",
]

QUALITY_PRESETS = {
    "low":  ("-ql", "480p15"),
    "mid":  ("-qm", "720p30"),
    "high": ("-qh", "1080p60"),
    "4k":   ("-qk", "2160p60"),
}


def run_manim(scene: str, qflag: str, extra_args: list[str] = []) -> bool:
    cmd = ["manim", qflag, "--disable_caching", "section_4_3.py", scene] + extra_args
    print(f"\n>> 渲染 {scene}  [{' '.join(cmd)}]")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def get_mp4(scene: str, subdir: str) -> Path:
    return Path(f"media/videos/section_4_3/{subdir}/{scene}.mp4")


def concat_videos(paths: list[Path], output: Path) -> bool:
    temp_dir = Path("media/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    list_file = temp_dir / "concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in paths), encoding="utf-8")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(output),
    ]
    print(f"\n[merge]  合并 {len(paths)} 个场景 → {output}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg 错误:", result.stderr[-500:])
    return result.returncode == 0


def main():
    args = sys.argv[1:]
    preset = "high" if "--hq" in args else ("4k" if "--4k" in args else "low")
    only_scene = None
    if "--scene" in args:
        idx = args.index("--scene")
        only_scene = int(args[idx + 1]) - 1

    qflag, subdir = QUALITY_PRESETS[preset]
    print(f"质量预设: {preset} ({subdir})")

    scenes_to_render = [SCENES[only_scene]] if only_scene is not None else SCENES
    failed = []

    for scene in scenes_to_render:
        ok = run_manim(scene, qflag)
        if not ok:
            failed.append(scene)
            print(f"  X {scene} 渲染失败！")
        else:
            print(f"  [OK] {scene}")

    if failed:
        print(f"\n[WARN]  失败场景: {failed}")
    else:
        print("\n[OK] 全部场景渲染完毕")

    if only_scene is None and not failed:
        paths = [get_mp4(s, subdir) for s in SCENES]
        missing = [p for p in paths if not p.exists()]
        if missing:
            print(f"[WARN]  缺少文件: {missing}")
        else:
            out = Path(f"section43_complete_{preset}.mp4")
            if concat_videos(paths, out):
                size_mb = out.stat().st_size / 1_048_576
                print(f"\n[DONE]  完成！输出文件: {out}  ({size_mb:.1f} MB)")
            else:
                print("[WARN]  合并失败，请手动检查 ffmpeg 日志")

    # Print scene durations
    print("\n场景时长统计:")
    total = 0.0
    for scene in SCENES:
        mp4 = get_mp4(scene, subdir)
        if mp4.exists():
            r = subprocess.run(
                ["ffprobe","-v","error","-show_entries","format=duration",
                 "-of","default=noprint_wrappers=1:nokey=1", str(mp4)],
                capture_output=True, text=True
            )
            dur = float(r.stdout.strip() or 0)
            total += dur
            idx = SCENES.index(scene) + 1
            print(f"  场景{idx:02d} {scene:<25} {dur:6.1f}s")
    m, s = divmod(int(total), 60)
    print(f"\n  总时长: {m}分{s:02d}秒 ({total:.0f}秒)")


if __name__ == "__main__":
    main()
