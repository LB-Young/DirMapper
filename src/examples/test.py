import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import asyncio
from llm_client import client, model
from DirMapper.DirMapper import DirMapper


input_dir = r"F:\test_files"
output_dir = r"F:\test_files_out"


async def main():
    mapper = DirMapper(input_dir, output_dir, client, model)
    async for item in mapper.mapper():
        print(item, end="", flush=True)
    return


if __name__ == '__main__':
    asyncio.run(main())


