import os


async def mkdir_dir(dir_tree=""):
    print("dir_tree:", dir_tree)
    all_need_dirs = dir_tree.replace("\\\\", "\\").split("\n")
    for dir in all_need_dirs:
        os.makedirs(dir, exist_ok=True)
    return "dir_tree: “{dir_tree}” have make success!"

async def mkdir_dirs(dir_tree="", params_format=False):
    if params_format:
        return ['dir_tree']
    else:
        return await mkdir_dir(dir_tree)
    
async def ut():
    return await mkdir_dirs("F:\\\\test_files_out\\\\文档指南\\nF:\\\\test_files_out\\\\研究论文\\nF:\\\\test_files_out\\\\技术报告\\nF:\\\\test_files_out\\\\其他")
if __name__ == '__main__':
    import asyncio
    asyncio.run(ut())