from django.contrib.auth import authenticate

import getpass


class InteractiveHandler(object):
    """负责与用户在命令行端所有的交互"""

    def __init__(self, *args, **kwargs):
        # print(models.Host.objects.all())
        if self.authenticate():
            self.interactive()

    def authenticate(self):
        """用户认证"""
        retry_count = 0
        while retry_count < 3:
            username = input("Username:").strip()
            if len(username) == 0: continue
            password = getpass.getpass("Password:")
            user = authenticate(username=username, password=password)
            if user is not None:
                print("\033[32;1mwelcome %s\033[0m".center(50, '-') % user)
                self.user = user
                return True
            else:
                print("wrong username or password!")
                retry_count += 1

        else:
            exit("too many attempts.")

    def select_hosts(self, bind_host_list):
        # exit_flag = False
        while True:
            # bind_host_list = host_groups[user_choice].bind_hosts.select_related()
            for index, host_obj in enumerate(bind_host_list):
                print("%s.\t%s" % (index, host_obj))

            user_choice2 = input("[%s]>>>" % self.user).strip()
            if user_choice2.isdigit():
                user_choice2 = int(user_choice2)
                if user_choice2 >= 0 and user_choice2 < len(bind_host_list):
                    print("---host>", bind_host_list[user_choice2])
            else:
                if user_choice2 == 'b':
                    break
                if user_choice2 == 'exit':
                    exit("bye")

    def interactive(self):
        '''用户SHELL'''

        exit_flag = False

        while not exit_flag:
            try:
                host_groups = self.user.host_groups.select_related()
                for index, group_obj in enumerate(host_groups):
                    print("%s.\t%s[%s]" % (index,
                                           group_obj,
                                           group_obj.bind_hosts.select_related().count()))
                print("z.\t未分组主机列表[%s]" % self.user.bind_hosts.select_related().count())

                user_choice = input("[%s]>>>" % self.user).strip()
                if len(user_choice) == 0: continue
                if user_choice.isdigit():
                    user_choice = int(user_choice)
                    if user_choice >= 0 and user_choice < len(host_groups):
                        self.select_hosts(host_groups[user_choice].bind_hosts.select_related())

                # print(self.user.bind_hosts.select_related())
                else:
                    if user_choice == 'z':
                        self.select_hosts(self.user.bind_hosts.select_related())

                    if user_choice == 'exit':
                        exit("bye.")
            except KeyboardInterrupt as e:
                pass
