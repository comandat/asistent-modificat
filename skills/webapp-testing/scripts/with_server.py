import argparse, subprocess, time, socket, sys, os, signal

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0

def wait_for_port(port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(port): return True
        time.sleep(0.5)
    return False

def start_process(cmd):
    # setsid ensures we can kill the whole process tree later
    return subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

def kill_process(proc):
    try: os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except: pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='append', default=[], help='Server start command')
    parser.add_argument('--port', action='append', default=[], help='Port to wait for')
    args, rest = parser.parse_known_args()

    # Functional pipeline: Start all servers
    procs = list(map(start_process, args.server))
    
    try:
        # Wait for all ports to be ready
        ready = all(map(wait_for_port, args.port))
        if not ready:
            print("❌ Timeout waiting for servers.")
            sys.exit(1)

        # Execute the automation script (command after --)
        command = rest[1:] if rest and rest[0] == '--' else rest
        if command:
            subprocess.run(command, check=True)
            
    finally:
        # Cleanup: Kill all servers
        list(map(kill_process, procs))

if __name__ == '__main__':
    main()
