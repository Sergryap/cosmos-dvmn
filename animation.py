import asyncio
import curses
import random
import os
from curses_tools import draw_frame, get_frame_size, read_controls, get_frame_size
from itertools import cycle
from physics import update_speed
from obstacles import Obstacle
from explosion import explode

MIN_COORD = 1
START_YEAR = 1957
END_YEAR = 2023
YEAR_SPEED_INDEX = 10
GUNS_APPEARANCE_YEAR = 1985
current_year = START_YEAR
additional_garbage_flag = True


async def fire(
        canvas, start_row, start_column, obstacles, obstacles_in_last_collisions, rows_speed=-0.3, columns_speed=0
):
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


async def animate_spaceship(
        canvas, start_row, start_column, coroutines, obstacles,
        obstacles_in_last_collisions, frame1, frame2
):
    row, column = start_row, start_column
    size_row, size_column = get_frame_size(frame1)
    rows_number, column_number = canvas.getmaxyx()
    max_row = rows_number - size_row - MIN_COORD
    max_column = column_number - size_column - MIN_COORD
    row_speed = column_speed = 0
    global current_year
    for frame in cycle([frame1, frame1, frame2, frame2]):
        for obstacle in obstacles:
            if obstacle.has_collision(row, column, size_row, size_column):
                coroutines.append(show_gameover(canvas))
                return
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        rows_direction, columns_direction, space_bar = read_controls(canvas)
        if space_bar and current_year >= GUNS_APPEARANCE_YEAR:
            coroutines.append(
                fire(canvas, row, column + size_column // 2, obstacles, obstacles_in_last_collisions, rows_speed=-1)
            )
        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction,
            row_speed_limit=5, column_speed_limit=5
        )
        row += row_speed
        column += column_speed
        row = MIN_COORD if row < MIN_COORD else min(max_row, row)
        column = MIN_COORD if column < MIN_COORD else min(max_column, column)


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
            explosion_row = start_row + rows_size // 2
            explosion_column = column + columns_size // 2
            await explode(canvas, explosion_row, explosion_column)
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
        start_garbage_row = random.randrange(rows_number) - rows_number
        coroutines.append(
            fly_garbage(
                canvas, coroutines, trashes, min_speed, max_speed,
                obstacles, obstacles_in_last_collisions, start_row=start_garbage_row
            )
        )


async def show_gameover(canvas):
    with open(os.path.join('frames', 'game_over', 'game_over.txt'), 'r', encoding='utf-8') as frame:
        game_over_frame = frame.read()
    rows_number, column_number = canvas.getmaxyx()
    rows_size, columns_size = get_frame_size(game_over_frame)
    rows_position = (rows_number - rows_size) // 2
    columns_position = (column_number - columns_size) // 2
    while True:
        draw_frame(canvas, rows_position, columns_position, game_over_frame)
        await asyncio.sleep(0)


async def show_year(canvas, row, column):
    global current_year
    global additional_garbage_flag
    count = 0
    while True:
        count += 1
        canvas.addstr(row, column, str(current_year))
        await asyncio.sleep(0)
        if count % YEAR_SPEED_INDEX == 0 and count > YEAR_SPEED_INDEX and current_year < END_YEAR:
            current_year = current_year + 1
            additional_garbage_flag = True
        canvas.addstr(row, column, str(current_year))


async def fill_orbit_with_garbage(
        canvas, coroutines, trashes, min_speed, max_speed, obstacles, obstacles_in_last_collisions
):
    global current_year
    global additional_garbage_flag
    rows_number, column_number = canvas.getmaxyx()
    interval_garbage_quantity = {(START_YEAR, 1985): 1, (1985, 1995): 2, (1995, 2015): 3, (2015, END_YEAR + 1): 4}
    year_garbage_quantity = {}
    for year in range(START_YEAR, END_YEAR + 1):
        quantity = [qty for interval, qty in interval_garbage_quantity.items() if interval[0] <= year < interval[1]][0]
        year_garbage_quantity.update({year: quantity})

    while True:
        await asyncio.sleep(0)
        if additional_garbage_flag:
            additional_garbage_flag = False
            additional_garbage_quantity = year_garbage_quantity[current_year]
            for _ in range(additional_garbage_quantity):
                start_garbage_row = random.randrange(rows_number) - rows_number
                coroutines.append(
                    fly_garbage(
                        canvas, coroutines, trashes, min_speed, max_speed,
                        obstacles, obstacles_in_last_collisions, start_row=start_garbage_row
                    )
                )
