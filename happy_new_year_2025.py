import time
import random
import os
from colorama import Fore, Back, Style, init
import math
import threading

# Inicializa o Colorama
init()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_color():
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

def get_terminal_size():
    try:
        columns = os.get_terminal_size().columns
        rows = os.get_terminal_size().lines
    except:
        columns, rows = 80, 24
    return columns, rows

def print_2025_centered():
    art = [
        "███████╗███████╗██╗     ██╗███████╗    ██████╗  ██████╗ ██████╗ ███████╗██╗",
        "██╔════╝██╔════╝██║     ██║╚══███╔╝    ╚════██╗██╔═████╗╚════██╗██╔════╝██║",
        "█████╗  █████╗  ██║     ██║  ███╔╝      █████╔╝██║██╔██║ █████╔╝███████╗██║",
        "██╔══╝  ██╔══╝  ██║     ██║ ███╔╝      ██╔═══╝ ████╔╝██║██╔═══╝ ╚════██║╚═╝",
        "██║     ███████╗███████╗██║███████╗    ███████╗╚██████╔╝███████╗███████║██╗",
        "╚═╝     ╚══════╝╚══════╝╚═╝╚══════╝    ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝"
    ]
    
    columns, rows = get_terminal_size()
    bottom_position = rows - len(art) - 3

    print(f"\033[{bottom_position};0H", end="")
    
    color = get_random_color()
    for line in art:
        padding = (columns - len(line)) // 2
        print(" " * padding + color + line + Style.RESET_ALL)

def print_firework(x_pos, height):
    trail_chars = [".", "•", "*", "⋆", "✦", "✺"]
    
    explosion_frames = [
        [
            "    *    ",
            "   ***   ",
            "  *****  ",
            "   ***   ",
            "    *    "
        ],
        [
            "  * * *  ",
            " *  *  * ",
            "*   *   *",
            " *  *  * ",
            "  * * *  "
        ],
        [
            " ✺  *  ✺ ",
            "✺ ✺ * ✺ ✺",
            "* * ✺ * *",
            "✺ ✺ * ✺ ✺",
            " ✺  *  ✺ "
        ],
        [
            "⋆  ✺  ⋆",
            " ⋆ * ⋆ ",
            "✺ ⋆ ⋆ ✺",
            " ⋆ * ⋆ ",
            "⋆  ✺  ⋆"
        ],
        [
            ".  *  .",
            " . ⋆ . ",
            "*  .  *",
            " . ⋆ . ",
            ".  *  ."
        ],
        [
            ".  .  .",
            " .   . ",
            ".     .",
            " .   . ",
            ".  .  ."
        ]
    ]
    
    columns, rows = get_terminal_size()
    color = get_random_color()
    
    working_area_height = (rows - 10)
    
    start_y = working_area_height - 5 
    end_y = 3 
    
    print_lock = threading.Lock()
    
    current_y = start_y
    while current_y > end_y:
        with print_lock:
            for i in range(working_area_height):
                print(f"\033[{i+1};{max(1, x_pos-5)}H" + " " * 10)
            
            trail_length = 8
            for i in range(trail_length):
                y = current_y + i
                if y < start_y:
                    x = x_pos + int(3 * math.sin((start_y - y) * 0.2))
                    char = trail_chars[min(trail_length - i - 1, len(trail_chars)-1)]
                    print(f"\033[{y};{x}H{color}{char}{Style.RESET_ALL}")
        
        current_y -= 1
        time.sleep(0.03)
    
    for frame in explosion_frames:
        with print_lock:
            for i in range(7):
                print(f"\033[{end_y+i-1};{x_pos-6}H" + " " * 15)
            
            y = end_y
            for i, line in enumerate(frame):
                print(f"\033[{y+i};{x_pos-4}H{color}{line}{Style.RESET_ALL}")
        
        time.sleep(0.1)
    
    with print_lock:
        for i in range(working_area_height):
            print(f"\033[{i+1};{max(1, x_pos-10)}H" + " " * 25)
    
    time.sleep(0.05)

def main():
    clear_terminal()
    print("\033[?25l") 
    
    try:
        columns, rows = get_terminal_size()
        
        print(f"\033[{rows-8};1H") 
        print_2025_centered()
        
        while True:
            firework_positions = [
                random.randint(5, 25),      # Esquerda
                random.randint(40, 60),     # Centro
                random.randint(75, 100),    # Direita
            ]
            

            threads = []
            for x_pos in firework_positions:
                thread = threading.Thread(target=print_firework, args=(x_pos, 5))
                threads.append(thread)
                thread.start()
                time.sleep(0.3)  
            
            for thread in threads:
                thread.join()
            
            time.sleep(0.5) 
            
    except KeyboardInterrupt:
        clear_terminal()
        print("\033[?25h")
        print("\nPrograma encerrado!")

if __name__ == "__main__":
    main()
