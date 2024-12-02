import os
import shutil


async def move_files(map={}, sources_dirs="", target_dirs="", params_format=False):
    if params_format:
        return ['map', 'sources_dirs', 'target_dirs']
    else:
        for file_name, category in map.items():
            source_file_path = sources_dirs + "\\" + file_name
            source_file_path = source_file_path.replace("\\\\","\\").replace("/", "\\")
            if os.path.exists(source_file_path):
                target_full_dir = target_dirs + "\\" + category
                target_full_dir = target_full_dir.replace("\\\\","\\").replace("/", "\\")
                shutil.copy2(source_file_path, target_full_dir)
            else:
                print(f"File {source_file_path} does not exist.")
    return "files have been copied!"
