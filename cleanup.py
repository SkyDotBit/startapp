import sys
import subprocess
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    script_name = sys.argv[1]
    print(script_name)
    subprocess.call(['pkill', '-f', script_name])