import os


async def get_files(dir_path):
        files = []
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                files.append(file_path)
            elif os.path.isdir(file_path):
                files.extend(await get_files(file_path))
        return "文件夹下的文件为：" + "\n".join(files)

async def get_dir_files(dir_path="", params_format=False):
    if params_format:
        return ['dir_path']
    else:
        return await get_files(dir_path)