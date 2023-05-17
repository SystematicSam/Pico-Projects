"""
OLED Controller

This Micropython script acts as an interface for the PiicoDev SSD1306
OLED Display Module.

Main functionality is printing.  Calling print
functions will display text on the OLED Module line by line similar to a
terminal console.

This script is most useful for debugging information when using other
PiicoDev sensors.

Author: Sam Rogers

Created: 12/05/2023
"""
from time import sleep

from PiicoDev_SSD1306 import create_PiicoDev_SSD1306

__author__ = "Sam Rogers"
__version__ = "0.1"


class Console:
    def __init__(self):
        self.oled = create_PiicoDev_SSD1306()
        self.line_pos = [0, 12, 24, 36, 48]
        self.curr_line = 0
        self.data = []

    def print(self, line: str):
        self.data[self.curr_line - 1] += line

    def println(self, line: str):
        if self.curr_line < len(self.line_pos):
            self.data.insert(self.curr_line, line)
            self.curr_line += 1
        else:
            self.data.pop(0)
            self.data.insert(self.curr_line, line)

    def refresh(self):
        self.oled.fill(0)
        for i in range(len(self.data)):
            self.oled.text(self.data[i], 0, self.line_pos[i])
        self.oled.show()

    def clear(self):
        self.oled.fill(0)


def main():
    """
    Main Loop
    """
    display = Console()
    count = 0
    while True:
        display.println(str(count))
        if count % 2 == 0:
            display.print("even")
        display.refresh()
        count += 1
        sleep(0.5)


if __name__ == '__main__':
    main()
