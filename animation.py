import asyncio
import curses
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size


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
        canvas.refresh()
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        delta_coord = read_controls(canvas)
        size_row = get_frame_size(frame1)[0]
        size_column = get_frame_size(frame1)[1]
        row, column = row + delta_coord[0], column + delta_coord[1]
        row = 1 if row < 1 else height - size_row - 1 if row > height - size_row - 1 else row
        column = 1 if column < 1 else width - size_column - 1 if column > width - size_column - 1 else column
