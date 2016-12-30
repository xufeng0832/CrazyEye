from backend import interactive


class ManagementUtily(object):
    """分发用户命令"""

    def __init__(self, sys_args):
        self.sys_args = sys_args
        self.argv_verify()  # 验证并调用用户指令对应的功能

    def show_help_msg(self):
        msg = '''
        run     启动堡垒机用户终端
        '''
        print(msg)
    def argv_verify(self):
        if len(self.sys_args) < 2:
            self.show_help_msg()
            return
        if hasattr(self, self.sys_args[1]):
            func = getattr(self, self.sys_args[1])
            func(self.sys_args)
        else:
            self.show_help_msg()

    def run(self, *args, **kwargs):
        """启动用户交互程序"""

        print("run...", args, kwargs)

        interactive.InteractiveHandler(*args, **kwargs)
