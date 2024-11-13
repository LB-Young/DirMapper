import json
from DirMapper.tools import get_dir_files, mkdir_dirs, move_files

class MapperAgent:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.tools = {"get_dir_files": get_dir_files, "mkdir_dirs": mkdir_dirs, "move_files": move_files}
        self.role = """
# Role: 文件整理员

# Profiles: 
- describe: 你是一个文件整理人员，负责将一个文件夹下的所有文件分类后，按类别整理到一个指定目录下，你可以使用工具完成一些步骤，Tools下的列出的工具就是你可以使用的全部工具。

# Goals:
- 你需要帮助其他人做文件整理，将一个文件夹下的所有文件自动分类，然后把每个文件整理到对应的类别文件夹之下。

# Tools:
- get_dir_files: 读取一个文件夹下所有的文件，返回文件名和文件路径，需要参数{"dir_path":"xxxx"}。
- mkdir_dirs: 根据给定的目录树创建对应的文件夹，，需要参数{"dir_tree":"xxxx"}。
- move_files: 将文件移动到指定的目录下，需要参数{"map":{"file1":"类别1", "file2":"类别2"}, "sources_dirs":input_dir, "target_dirs":output_dir}。

# Constraints:
- 你设计的类别一定是根据文件的特点和内容来合理设计的，不能随意分类。
- 你在设计类别的时候要覆盖全部的文件。
- 在把文件整理到对应的类别目录下的时候，不能有文件被遗漏。
- 整理后文件夹的目录根源目录在同一级目录下。
- 你在调用工具的时候可以使用“=>$tool_name: {key:value}”来触发工具调用。
- 每一次触发了不同的tool之后，你需要停止作答，等待用户调用对应的tool处理之后，将tool的结果重新组织语言后再继续作答，新的答案要接着“=>$tool_name”前面的最后一个字符继续生成结果，要保持结果通顺。

# Workflows:
- 1. 输入一个文件夹路径，获取该文件夹下的所有文件名。
- 2. 根据文件的特点和内容，设计合理的类别，类别输出的标识符为=>['类别1','类别2']。
- 3. 按照设计的类别新建类别文件夹，并输出文件夹的目录树，并创建好目录结构。
- 4. 将每个文件按照设计好的类别分类输出结果为=>{"file1":"类别1", "file2":"类别2"}。
- 5. 将每个文件按照分类结果移动到对应的类别文件夹下。

需要整理的文件夹目录为:{input_dir},整理后的文件夹目录为:{output_dir}。
"""

    async def tool_run(self, tool_message):
        # breakpoint()
        function_name, function_params = tool_message.split(":", 1)
        function_params_json = json.loads(function_params)
        need_params = await self.tools[function_name](params_format=True)
        extract_params = {}
        for param in need_params:
            extract_params[param] = function_params_json[param]
        result = await self.tools[function_name](**extract_params)
        return result

    async def do_mapper(self, input_dir, output_dir, processed_content=""):
        # TODO: Implement the mapper logic
        prompt = self.role.replace("{input_dir}", input_dir).replace("{output_dir}", output_dir).strip()
        if len(processed_content) > 0:
            prompt = prompt + "\n\n" + processed_content
        messages = [{"role": "user", "content": prompt}]
        result = self.client.chat.completions.create(
                model=self.model,  # 请填写您要调用的模型名称
                messages=messages,
                stream=True
            )
        all_answer = ""
        tool_messages = ""
        tool_Flag = False
        for chunk in result:
            all_answer += chunk.choices[0].delta.content
            if tool_Flag:
                tool_messages += chunk.choices[0].delta.content
                continue
            if ":" in chunk.choices[0].delta.content and "=>$" in all_answer:
                tool_Flag = True
                tool_messages += chunk.choices[0].delta.content
                yield ": "
                continue
            yield chunk.choices[0].delta.content
        if tool_Flag:
            tool_messages = all_answer.split("=>$")[-1]
            result = await self.tool_run(tool_message=tool_messages)
            for item in str(result+"\n"):
                yield item
            processed_content = processed_content + "\n" + "已经执行内容:" + all_answer + "\n" + "工具执行结果:" + result
            async for item in self.do_mapper(input_dir, output_dir, processed_content):
                yield item