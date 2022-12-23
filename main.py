import time
import curses
import asyncio

TIC_TIMEOUT = 0.1


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    coroutine_1 = blink(canvas, 5, 20)
    coroutine_2 = blink(canvas, 5, 22)
    coroutine_3 = blink(canvas, 5, 24)
    coroutine_4 = blink(canvas, 5, 26)
    coroutine_5 = blink(canvas, 5, 28)
    coroutines = [coroutine_1, coroutine_2, coroutine_3, coroutine_4, coroutine_5]
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


# def star(canvas):
#     curses.curs_set(False)
#     row, column = (5, 20)
#     canvas.border()
#     while True:
#         canvas.addstr(row, column, '*', curses.A_DIM)
#         canvas.refresh()
#         time.sleep(2)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)
#         canvas.addstr(row, column, '*', curses.A_BOLD)
#         canvas.refresh()
#         time.sleep(0.5)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
