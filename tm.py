import os
import time
import psutil
import distro
import platform

apps = {}
pids = {}


class Process:
    def __init__(self, proc):
        self.pid = proc.pid
        self.name = proc.name()
        self.cpu = proc.cpu_percent()
        self.mem = proc.memory_percent()
        self.status = proc.status()
        self.prio = proc.nice()
        self.threads = proc.threads()
        self.children = proc.children()
        self.type = proc.username()
        self.parent = proc.parent()
        try:
            io = proc.io_counters()
            storage = psutil.disk_usage('/')[0] / 1073741824
            self.disk = (((io[2] + io[3]) / 1073741824) / storage) * 100
        except psutil.AccessDenied:
            self.disk = 0


def prog_bar(i, done=False):
    n = int(i / 2)
    bars = f"|{'=' * n}{' ' * (50 - n)}|"
    print(f"\rLoading all process information: {bars} {i:.0f}%", end="")
    if done: print(" Completed")


def bar(arg="-"):
    print(arg * 100)


def generate_procs(reload=False):
    if reload:
        globals()["apps"] = {}
        globals()["pids"] = {}

    n = len(list(psutil.process_iter()))
    for prog, proc in enumerate(psutil.process_iter()):
        prog_bar((prog / n) * 100)
        pids[proc.pid] = proc.name()
        p = Process(proc)
        if p.name in apps:
            update(p)
        else:
            apps[p.name] = p
    prog_bar(100, True)
    time.sleep(0.25)
    if not reload: bar()


def update(p):
    proc = apps.get(p.name)
    proc.mem += p.mem
    proc.cpu += p.cpu
    proc.disk += p.disk
    proc.threads.extend(p.threads)
    proc.children.extend(p.children)


def print_procs(procs=None):
    if not procs:
        procs = list(apps.values())

    indent = "{:<25} {:<8} {:<8} {:<8} {:<7} {:<9} {:<11} {:<10} {}"
    print(indent.format(
        "Name", "CPU", "Memory", "Disk", "PID", "Type", "Status", "Priority", "Thread")
    )

    for p in procs:
        name = f"{p.name[:18]}..." if len(p.name) > 22 else f"{p.name}"
        name += f"({len(p.children) + 1})" if len(p.children) > 0 else ""
        mem = f"{p.mem:.2f}%"
        cpu = f"{p.cpu:.2f}%"
        disk = f"{p.disk:.2f}%"
        p_type = f"{p.type[:6]}.." if len(p.type) > 8 else p.type
        prio = "High" if p.prio < -10 else ("Low" if p.prio > 10 else "Medium")
        print(indent.format(name, cpu, mem, disk, p.pid, p_type, p.status, prio, len(p.threads)))
        time.sleep(0.05)


def print_sorted(arg, procs=None):
    if not procs:
        procs = list(apps.values())

    if "cpu" in arg:
        procs = sorted(procs, key=lambda p: p.cpu)
    elif "mem" in arg:
        procs = sorted(procs, key=lambda p: p.mem)
    elif "disk" in arg:
        procs = sorted(procs, key=lambda p: p.disk)
    elif "thread" in arg:
        procs = sorted(procs, key=lambda p: len(p.threads))
    elif "prio" in arg:
        procs = sorted(procs, key=lambda p: p.prio, reverse=True)
    else:
        print("invalid parameter")
        return
    if arg[-1] == "^":
        procs.reverse()
    print_procs(procs)


def print_type(arg):
    procs = list(apps.values())

    if "root" in arg:
        procs = list(filter(lambda p: "root" in p.type, procs))
    elif "usr" in arg:
        procs = list(filter(lambda p: os.getlogin() in p.type, procs))
    elif "other" in arg:
        procs = list(filter(lambda p: "root" not in p.type and os.getlogin() not in p.type, procs))
    else:
        print("invalid parameter")
        return
    if "sorted" in arg:
        print_sorted(arg, procs)
    else:
        print_procs(procs)


def print_stat(arg):
    procs = list(apps.values())

    if "idle" in arg:
        procs = list(filter(lambda p: p.status == "idle", procs))
    elif "sleeping" in arg:
        procs = list(filter(lambda p: p.status == "sleeping", procs))
    elif "running" in arg:
        procs = list(filter(lambda p: p.status == "running", procs))
    else:
        print("invalid parameter")
        return
    if len(procs) == 0:
        print(f"No {arg[0]} process available")
        return
    if "sorted" in arg:
        print_sorted(arg, procs)
    else:
        print_procs(procs)


def print_parent(arg):
    try:
        pid = int(arg)
    except ValueError:
        print("invalid input")
        return
    if pid not in pids:
        print(f"No process available with pid {pid}")
        return
    indent = "{:<12} {:<20} {}"
    name = pids.get(pid)
    p = apps.get(name)
    name = f"Name: {p.name[:12]}.." if len(p.name) > 16 else p.name
    print(indent.format("Process", name, f"pid: {p.pid}"))
    if p.parent:
        name = f"Name: {p.parent.name()[:12]}.." if len(p.parent.name()) > 16 else p.parent.name()
        print(indent.format("Parent", name, f"pid: {p.parent.pid}"))
    else:
        print(indent.format("Parent", "None", ""))


def print_child(arg):
    try:
        pid = int(arg)
    except ValueError:
        print("invalid input")
        return
    if pid not in pids:
        print(f"No process available with pid {pid}")
        return
    indent = "{} {:<24} {:<16} {}"
    name = pids.get(pid)
    p = apps.get(name)
    if len(p.children) > 0:
        print(f"{p.name}: ")
        for ch in p.children:
            try:
                name = f"{ch.name()[:14]}.." if len(ch.name()) > 15 else ch.name()
                print(indent.format(" |->", name, f"pid = {ch.pid}", f"status = {ch.status()}"))
                time.sleep(0.05)
            except Exception:
                pass
    else:
        print(f"{p.name} has no child")


def print_threads(arg):
    try:
        pid = int(arg)
    except ValueError:
        print("invalid input")
        return
    if pid not in pids:
        print(f"No process available with pid {pid}")
        return
    name = pids.get(pid)
    p = apps.get(name)
    indent = "{:<2} {:<14} {:<20} {}"
    print(f"{p.name}: ")
    for tid, ut, st in p.threads:
        print(indent.format(" |->", f"id: {tid}", f"user time: {ut}", f"system time: {st}"))


def overall_usage():
    indent = "{:<18} {:<8} {:<9} {:<8} {:<4} {:<9} {:<7} {:<11} {:<10} {}"
    print(indent.format(
        "Platform", "CPU", "Memory", "Disk", "|", "RAM", "Core", "Storage", "Distro", "Version")
    )
    to_gb = 1073741824
    cpu = f"{psutil.cpu_percent(0.5)}%"
    mem = f"{psutil.virtual_memory()[2]}%"
    ram = f"{psutil.virtual_memory()[0] / to_gb:.2f}GB"
    storage = psutil.disk_usage('/')[0] / to_gb
    cores = psutil.cpu_count()
    io = psutil.disk_io_counters()
    disk = f"{(((io[2] + io[3]) / to_gb) / storage) * 100:.2f}%"
    pl = f"{platform.system()} {platform.release().split('-')[0]}"
    print(indent.format(
        pl, cpu, mem, disk, "|", ram, cores, f"{storage:.2f}GB", distro.name(), distro.version())
    )
    bar()


def options():
    indent = "{:<32} {:<26} {}"
    print(indent.format("Action(s)", "Command(s)", "Example(s)"))
    print(indent.format("Print all processes", "all", "all"))
    print(indent.format("print all in sorted order", "sorted 'arg' ''/'^'", "sorted mem, sorted disk ^"))
    print(indent.format("Print type wise", "type 'arg'", "type root, type usr sorted disk"))
    print(indent.format("Print status wise", "stat 'arg'", "stat idle, stat sleeping sorted mem ^"))
    print(indent.format("Print child of a process", "childof 'pid'", "childof 2, childof 1287"))
    print(indent.format("Print parent of a process", "parentof 'pid'", "parentof 580, parentof 3543"))
    print(indent.format("Print threads of a process", "threads 'pid'", "threads 582, threads 1287"))
    print(indent.format("Print process tree", "pstree", "pstree"))
    print(indent.format("Update process information", "update, update info", "update"))
    print(indent.format("Terminate program", "exit, terminate", "exit, terminate"))
    bar()


def header():
    bar(arg="=")
    print(44 * " " + "Task Manager")
    bar(arg="=")
    overall_usage()
    generate_procs()


if __name__ == '__main__':
    header()
    while True:
        options()
        try:
            command = input("Enter command: ").lower()
        except KeyboardInterrupt:
            print("\nInvalid command")
            continue
        if command in ["exit", "terminate"]:
            print(44 * "-", "Terminated", 44 * "-")
            break
        elif command == "all":
            print_procs()
        elif command.startswith("sorted"):
            print_sorted(command.split(" ")[1:])
        elif command.startswith("type"):
            print_type(command.split(" ")[1:])
        elif command.startswith("stat"):
            print_stat(command.split(" ")[1:])
        elif command == "pstree":
            os.system("pstree")
        elif command.startswith("childof"):
            print_child(command.split(" ")[1])
        elif command.startswith("parentof"):
            print_parent(command.split(" ")[1])
        elif command.startswith("threads"):
            print_threads(command.split(" ")[1])
        elif command in ["update", "update info"]:
            generate_procs(reload=True)
        else:
            print("Invalid command")
        bar()
        overall_usage()
