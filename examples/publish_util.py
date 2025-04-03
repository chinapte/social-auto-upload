import subprocess
import shlex
def call_cli(command):
    # 将命令分割成一个列表
    command_list = shlex.split(command)

    try:
        # 调用命令
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        print("Command Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)