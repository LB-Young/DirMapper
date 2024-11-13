from DirMapper.agents.mapper_agent.mapper_agent import MapperAgent


class DirMapper:
    def __init__(self, input_dir, out_put_dir, client, model):
        self.client = client
        self.input_dir = input_dir
        self.out_put_dir = out_put_dir
        self.model = model
        self.mapper_agent = MapperAgent(self.client, self.model)
    
    async def mapper(self):
        async for item in self.mapper_agent.do_mapper(self.input_dir, self.out_put_dir):
            yield item
    
    async def unmapper(self):

        return
    
    async def search_file(self, file_name):
        file_path = ""
        return file_path
    
    async def fuzzy_search_file(self, dedscribe):
        file_path = ""
        return file_path

