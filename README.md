# DirMapper
DirMapper is an agent-based tool for automatic document organization.


# USE
1、you have to set zhipuai api_key in src/llm_client.py;
2、if you want to change the zhipuai client to others, you can init other client in the file, and install the sdk of your client;
3、src/examples/test.py is a test file, you can run it to test the function of DirMapper; you need change the below two params:
```
input_dir = "path to your input dir"
output_dir = "path to your output dir"
```
4、run
```
cd src/examples
python test.py
```

# TODO
1、add fuzzy search capabilities


# Illustrate
if you change the client there may be some errors, you can change the code in "src/DirMapper/agents/mapper_agent/mapper_agent.py" to adapt to your client.