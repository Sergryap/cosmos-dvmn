import asyncio
import curses
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size

MIN_COORD = 1


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, start_row, start_column, frame1, frame2):
    row, column = start_row, start_column
    height, width = canvas.getmaxyx()
    for frame in cycle([frame1, frame2]):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        rows_direction, columns_direction, __ = read_controls(canvas)
        size_row, size_column = get_frame_size(frame1)
        row, column = row + rows_direction, column + columns_direction
        row = (
            MIN_COORD if row < MIN_COORD
            else height - size_row - MIN_COORD
            if row > height - size_row - MIN_COORD
            else row
        )
        column = (
            MIN_COORD if column < MIN_COORD
            else width - size_column - MIN_COORD
            if column > width - size_column - MIN_COORD
            else column
        )
