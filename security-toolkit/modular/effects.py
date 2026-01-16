import sys
import time

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    PINK= '\033[38;5;218m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def type_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def show_banner():
    banner = f"""{Colors.PINK}{Colors.BOLD}
    
 ██ ███ ███ █ █ ██  ███ ███ █ █     ███  █  █   █ █ ███ ███ 
█   █   █   █ █ █ █  █   █  █ █      █  █ █ █   █ █  █   █  
█   ██  █   █ █ ██   █   █   █       █  █ █ █   ██   █   █  
 █  █   █   █ █ █ █  █   █   █       █  █ █ █   █ █  █   █  
  █ █   █   █ █ █ █  █   █   █       █  █ █ █   █ █  █   █  
██  ███ ███  █  █ █ ███  █   █       █   █  ███ █ █ ███  █  
                                                           
    {Colors.MAGENTA}[*] For Educational Purposes Only... {Colors.RESET}
    
    """
    print()
    print(banner)
    time.sleep(1)