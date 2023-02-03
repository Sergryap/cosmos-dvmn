import asyncio
import curses
import random
from curses_tools import draw_frame, get_frame_size, read_controls, get_frame_size
from itertools import cycle
from physics import update_speed
from obstacles import Obstacle

MIN_COORD = 1


async def fire(canvas, start_row, start_column, obstacles, obstacles_in_last_collisions, rows_speed=-0.3, columns_speed=0):
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
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_in_last_collisions.append(obstacle)
                return
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, start_row, start_column, coroutines, obstacles, obstacles_in_last_collisions, frame1, frame2):
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
            coroutines.append(fire(canvas, row, column + size_column // 2, obstacles, obstacles_in_last_collisions, rows_speed=-1))
        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction,
            row_speed_limit=5, column_speed_limit=5
        )
        row += row_speed
        column += column_speed
        row = MIN_COORD if row < MIN_COORD else min(max_row, row)
        column = MIN_COORD if column < MIN_COORD else min(max_column, column)


def get_fly_garbage_flow(canvas, count, *args, **kwargs):
    coroutines = []
    rows_number, __ = canvas.getmaxyx()
    for _ in range(count):
        start_garbage_row = random.randrange(rows_number)
        coroutines.append(fly_garbage(canvas, start_row=start_garbage_row, *args, **kwargs))
    return coroutines


async def fly_garbage(
        canvas, coroutines, trashes, min_speed, max_speed,
        obstacles, obstacles_in_last_collisions, start_row
):

    trash = random.choice(trashes)
    rows_number, column_number = canvas.getmaxyx()
    rows_size, columns_size = get_frame_size(trash)
    column = random.randrange(column_number)
    speed = round(random.uniform(min_speed, max_speed), 1)

    while start_row < rows_number:
        obstacle = Obstacle(start_row, column, rows_size, columns_size)
        obstacles.append(obstacle)
        draw_frame(canvas, start_row, column, trash)
        await asyncio.sleep(0)
        draw_frame(canvas, start_row, column, trash, negative=True)
        start_row += speed
        if obstacle in obstacles_in_last_collisions:
            obstacles.remove(obstacle)
            obstacles_in_last_collisions.remove(obstacle)
            trash = random.choice(trashes)
            rows_size, columns_size = get_frame_size(trash)
            column = random.randrange(column_number)
            speed = round(random.uniform(min_speed, max_speed), 1)
            start_row = 0
            continue
        canvas.border()
        obstacles.remove(obstacle)
    else:
        coroutines.append(fly_garbage(canvas, coroutines, trashes, min_speed, max_speed, obstacles, obstacles_in_last_collisions, start_row=0))
