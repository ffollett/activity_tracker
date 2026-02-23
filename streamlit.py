import sqlite3
import streamlit as st
import numpy as np
from datetime import datetime, date, time

#Constants
sql_types = ['INTEGER', 'REAL', 'TEXT', 'BLOB']

#DB
conn = sqlite3.connect('windows.db')
c = conn.cursor()

#Functions
def view_all(limit=100):
	c.execute('SELECT * FROM windowtracking ORDER BY start DESC LIMIT ?', (limit,))
	data = c.fetchall()
	return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM windowtracking')
	data = c.fetchall()
	return data

def view_today():
    #get date as string in format yyyy-mm-dd
    today = datetime.today().strftime('%Y-%m-%d')
    c.execute(f'SELECT * FROM windowtracking WHERE date(start)="{today}"')
    data = c.fetchall()
    return data

#search
def get_blog_by_title(title):
	c.execute(f'SELECT * FROM windowtracking WHERE title="{title}"')
	data = c.fetchall()
	return data

def add_data(title, start):
	c.execute('INSERT INTO windowtracking(title, start) VALUES (?,?)',(title, start))
	conn.commit()

# doesn't work currently
def add_col(name, dtype):
    c.execute('ALTER TABLE windowtracking ADD COLUMN ? ?',(name, dtype))
    conn.commit()

# untested but probably doesn't work for same reasons as add_col()
def rename_col(old_name, new_name):
    c.execute('ALTER TABLE windowtracking RENAME COLUMN ? TO ?', (old_name, new_name))
    conn.commit()

#delete
def delete_data():
	c.execute('DELETE FROM windowtracking')
	conn.commit()

# sidebar
menu = ['Home', 'Today', 'Add Record', 'Add Column']

choice = st.sidebar.selectbox("Menu",menu)
if st.sidebar.button("Purge db"):
    delete_data()

# Main Content
if choice == 'Home':
    st.subheader("Home")
    limit = st.number_input("Limit results", min_value=1, max_value=10000, value=100)
    result = view_all(limit)
        
    for i in result:
        st.write(f"{i[1]}: {i[0]}")
    
elif choice == 'Today':
    st.subheader("Today's Acitvity")
    result = view_today()
    
    for i in result:
        st.write(f"{i[1]}: {i[0]}")

elif choice == 'Add Record':
    st.subheader("Add a new record")
    new_title = st.text_input("New Title")
    new_date = st.date_input("Enter the Date")
    new_time = st.time_input("Enter the time")
    
    if st.button("Save Entry"):
        combined = datetime.combine(new_date, new_time)
        add_data(new_title, combined)
        
elif choice == 'Add Column':
    st.subheader("Add a new column to the database")
    new_col = st.text_input("Column name")
    new_col_type = st.selectbox("Column Type", sql_types)
    
    if st.button("Create Column"):
        add_col(new_col, new_col_type)
    