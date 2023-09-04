#!/usr/bin/env python3

import os
import subprocess
import fire


start_file_name: str = 'start.sh'
display_running_servers_command: str = 'tmux ls'
parent_directory = "/home/ubuntu/Minecraft/"


def make_path(parent: str, child: str):
    return parent + child


servers: dict[str, str] = {
    "lobby": make_path(parent_directory, "lobby"),

    "earth-spawn-1": make_path(parent_directory, "earth/spawn-1"),
    "earth-world-1": make_path(parent_directory, "earth/world-1"),
    "earth-nether-1": make_path(parent_directory, "earth/nether-1"),
    "earth-the-end-1": make_path(parent_directory, "earth/the-end-1")
}


def is_server_started(server_name: str) -> bool:
    running_servers_raw_format = subprocess.check_output(["tmux", "ls"], universal_newlines=True).splitlines()
    running_servers_formatted = []

    for raw_server in running_servers_raw_format:
        running_servers_formatted.append(raw_server.split(":")[0])

    return server_name in running_servers_formatted


class Main:
    def restart_server(name: str):
        os.system(f'tmux send-keys -t {name} "restart" C-m')


    def start_server(name: str):
        server_directory = servers.get(name)
        start_file = server_directory + "/" + start_file_name

        result = subprocess.check_output(["sh", start_file], cwd=server_directory, universal_newlines=True)
        print(result)


    def restart_running_servers(self):
        for server_name, _ in servers.items():
            if not is_server_started(server_name):
                print(f"Server {server_name} hasn't been turned on, skipping to next server...")
            else:
                self.restart_server(server_name)
                print(f"Server {server_name} is being restarted...")


    def start_all_servers(self):
        for server_name, _ in servers.items():
            if is_server_started(server_name):
                print(f"Server {server_name} had started, skipping to next server...")
            else:
                self.start_server(server_name)
                print(f"Server {server_name} is starting...")



if __name__ == '__main__':
    fire.Fire(Main)