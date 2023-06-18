# run export LC_ALL=C to avoid locale errors
import tkinter as tk
import ttkbootstrap as ttk
import sqlite3

db = sqlite3.connect('kjv.sqlite')

conn = db.cursor()

books_of_bible = [
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
    'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings',
    '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah',
    'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
    'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea',
    'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
    'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark',
    'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
    'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
    '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
    'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
    '3 John', 'Jude', 'Revelation'
]
chapter_list = []
verse_list = []

def set_chapters(event):
    global chapter_list
    book = books_of_bible.index(book_var.get()) + 1
    conn.execute(
f"""
SELECT chapter FROM verses WHERE book = {book}
"""

    )
    chapter_list  = conn.fetchall()
    last_chapter: int = chapter_list[-1][0]
    chapter_list = [i for i in range(1, last_chapter+1)]
    chapter_['values'] = chapter_list
    set_verse(1)
    chapter_var.set(1)

def set_verse(event):
    book = books_of_bible.index(book_var.get())+1
    chapter = chapter_var.get()
    conn.execute(
f"""
SELECT verse FROM verses WHERE book = {book} AND chapter = {chapter}
"""

    )
    verse_list = conn.fetchall()
    last_verse:int = verse_list[-1][0]
    verse_list = [i for i in range(1, last_verse+1)]
    verse_['values'] = verse_list
    verse_var.set(1)

def print_verse():
    book= books_of_bible.index(book_var.get())+1
    chapter = chapter_var.get()
    verse = verse_var.get()
    conn.execute(
f"""
SELECT text FROM verses WHERE book = {book} AND chapter = {chapter} AND verse = {verse}
"""
    )
    text = conn.fetchall()[0][0]
    text_var.set(text)
    print(text)
# Setup
window = ttk.Window(themename='vapor')
window.title('app')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry('600x300')

# widgets
book_var = tk.StringVar(value=books_of_bible[0])
book_ = ttk.Combobox(window, textvariable=book_var)
book_['values'] = books_of_bible
book_.pack()
book_.bind('<<ComboboxSelected>>', set_chapters)

chapter_var = tk.StringVar(value=1)
chapter_ =ttk.Combobox(window, textvariable=chapter_var)
chapter_.pack()
chapter_.bind('<<ComboboxSelected>>', set_verse)

verse_var = tk.StringVar(value=1)
verse_ = ttk.Combobox(window, textvariable=verse_var)
verse_.pack()

btn = ttk.Button(window, command=print_verse, text="search")
btn.pack()

text_var = tk.StringVar(value='')
text = ttk.Label(window, textvariable=text_var, wraplength=550)
text.pack()
set_chapters(1)


# Security event
window.bind('<Escape>', lambda event: window.quit())
# Run
window.mainloop()