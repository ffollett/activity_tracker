from ctypes import windll, create_unicode_buffer
from time import sleep
from datetime import datetime
import sqlite3
conn = sqlite3.connect('windows.db')
c = conn.cursor()

def get_foreground_window_title():
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    if buf.value:
        return buf.value
    else:
        return 'blank'

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS windowtracking(title TEXT, start TEXT)')

def add_data(title, start):
	c.execute('INSERT INTO windowtracking(title, start) VALUES (?,?)',(title, start))
	conn.commit()

def delete_data(title):
	c.execute(f'DELETE FROM windowtracking WHERE title="{title}"')
	conn.commit()

def get_latest_window():
    c.execute('SELECT * FROM windowtracking ORDER BY start DESC LIMIT 1')
    return c.fetchone()

window = ''
last_window = ''
create_table()
window = get_latest_window()

while True:
    if window:
        # there was an observation already
        last_window = window
        window = get_foreground_window_title()
        if last_window == window:
            sleep(1)
        else:
            print(f"{datetime.now()}, {window}")
            add_data(window, datetime.now())
    else:
        # first run
        print("Starting a new table")
        window = get_foreground_window_title()
        add_data(window, datetime.now())
        sleep(1)