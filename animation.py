import asyncio
import curses
import random
from curses_tools import draw_frame
from itertools import cycle
from curses_tools import read_controls, get_frame_size
from physics import update_speed
import time

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
    max_row, max_column = rows - MIN_COORD, columns - MIN_COORD

    curses.beep()

    while MIN_COORD < row < max_row and MIN_COORD < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, start_row, start_column, cors, frame1, frame2):
    row, column = start_row, start_column
    size_row, size_column = get_frame_size(frame1)
    height, width = canvas.getmaxyx()
    max_row = height - size_row - MIN_COORD
    max_column = width - size_column - MIN_COORD
    row_speed = column_speed = 0
    for frame in cycle([frame1, frame1, frame2, frame2]):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        rows_direction, columns_direction, space_bar = read_controls(canvas)
        if space_bar:
            cors.append(fire(canvas, row, column + size_column // 2, rows_speed=-1))
        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction,
            row_speed_limit=5, column_speed_limit=5
        )
        row += row_speed
        column += column_speed
        row = MIN_COORD if row < MIN_COORD else min(max_row, row)
        column = MIN_COORD if column < MIN_COORD else min(max_column, column)


def get_coroutine_list(canvas, coroutine, count, *args, **kwargs):
    coroutines = []
    for _ in range(count):
        coroutines.append(coroutine(canvas, *args, **kwargs))
    return coroutines


async def fill_orbit_with_garbage(canvas, width, trashes, min_speed, max_speed):
    while True:
        trash = random.choice(trashes)
        column = random.randrange(width)
        speed = round(random.uniform(min_speed, max_speed), 1)
        await fly_garbage(canvas, column, trash, speed)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        canvas.border()

