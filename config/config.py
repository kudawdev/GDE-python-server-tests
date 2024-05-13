import configparser


class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    @property
    def server_host(self):
        return self.config.get('server', 'host')

    @property
    def server_port(self):
        return self.config.getint('server', 'port')

    @property
    def server_timeout_sec(self):
        return self.config.getint('server', 'timeout_sec')

    @property
    def client_num_client(self):
        return self.config.getint('client', 'num_client')

    @property
    def client_tasks(self):
        valid_tasks = ["io", "cpu", "fib"]
        tasks_str = self.config.get('client', 'tasks')
        tasks_list = tasks_str.split(',')
        validated_tasks = []

        for task in tasks_list:
            task = task.strip()
            if task in valid_tasks:
                validated_tasks.append(task)

        if not validated_tasks:
            validated_tasks = ["fib"]

        return validated_tasks

    @property
    def task_setting_fibonacci_limit(self):
        return self.config.getint('task_setting', 'fibonacci_limit')

    @property
    def task_setting_large_file_name(self):
        return self.config.get('task_setting', 'large_file_name')

    @property
    def other_asyn_semaphore(self):
        return self.config.getint('other', 'asyn_semaphore')

    @property
    def other_multiprocessing_processes(self):
        return self.config.getint('other', 'multiprocessing_processes')
