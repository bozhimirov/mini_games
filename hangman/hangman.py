import random
import string
from tkinter import *
from tkinter import ttk


def new_game():
    global used_letters
    global searched_letters
    global searched_word_w_spaces
    global guesses
    guesses = 0
    remove_grid()
    word_entry['foreground'] = 'black'
    end_label.grid_remove()
    w_label.grid(column=2, row=1, sticky='news')
    searched_letters = get_letters_from_word()
    used_letters = [searched_letters[0], searched_letters[-1]]
    searched_word_w_spaces = '    '.join([letter if letter in used_letters else '*' for letter in searched_letters])
    word_entry.config(text=searched_word_w_spaces)
    enable_letters(string.ascii_lowercase)
    disable_letters(used_letters)


def get_letters_from_word():
    with open('words.txt', 'r') as wordlist:
        f = wordlist.readlines()
        searched_word = random.choice(f).lower()
        while len(searched_word) < 6:
            searched_word = random.choice(f)
        return [x for x in searched_word if x != '\n']


def disable_letters(source):
    for letter in source:
        buttons_hash_table[letter].state(['disabled'])


def enable_letters(source):
    for letter in source:
        buttons_hash_table[letter].state(['!disabled'])


def make_buttons():
    inner_counter = 0
    for i in string.ascii_lowercase:
        buttons_hash_table[i] = ttk.Button(fr3, text=i, command=lambda ltr=i: handle_letter(ltr), width=5, padding=3)
        buttons_hash_table[i].grid(column=(inner_counter % 10), row=inner_counter // 10, sticky='news', padx=2, pady=2)
        inner_counter += 1
    ng = ttk.Button(fr3, text='New Game', command=new_game, padding=3)
    ng.grid(
        column=inner_counter % 10, row=inner_counter // 10, columnspan=10 - ((inner_counter - 1) % 10), sticky='news',
        padx=2, pady=2
    )


def check_progress():
    check_hanger()
    if '*' not in word_entry['text']:
        word_entry['foreground'] = 'blue'
        remove_grid()
        image_file['image'] = photos[0]
        image_file.grid(column=1, row=2)
        disable_letters(string.ascii_lowercase)
        w_label.grid_remove()
        end_label['text'] = '    You are the'
        end_label['foreground'] = 'blue'
        end_label.grid(column=2, row=1, sticky='news')
        # print('winner')
    elif guesses == 9:
        word_entry['foreground'] = 'red'
        disable_letters(string.ascii_lowercase)
        remove_grid()
        w_label.grid_remove()
        end_label['text'] = '      You are a'
        end_label['foreground'] = 'red'
        end_label.grid(column=2, row=1, sticky='news')
        image_file['image'] = photos[1]
        image_file['background'] = root['background']
        image_file.grid(column=1, row=2, sticky='news')
        # print('hanged')


def remove_grid():
    for i in ascii_art:
        i.grid_remove()
    image_file.grid_remove()


def check_hanger():
    if guesses == 0:
        pass
    elif guesses == 1:
        for i in grid_values_picture[guesses]:
            i[0].grid(
                column=i[1][0],
                row=i[1][1],
                sticky='s', pady=0, padx=0
            )
            i[0]['foreground'] = 'red'
        hidden = grid_values_picture[guesses + 1][0]
        hidden.grid(
            column=grid_values_picture[guesses + 1][1][0],
            row=grid_values_picture[guesses + 1][1][1],
            sticky='sw'
        )
        hidden['foreground'] = 'SystemButtonFace'
    elif guesses <= 9:
        grid_values_picture[guesses][0]['foreground'] = 'red'
        grid_values_picture[guesses][0].grid(
            column=grid_values_picture[guesses][1][0],
            row=grid_values_picture[guesses][1][1],
            sticky='sw'
        )


def handle_letter(letr):
    global searched_word_w_spaces
    global guesses
    guesses += 1
    used_letters.append(letr)
    buttons_hash_table[letr].state(['disabled'])
    searched_word_with_spaces = '    '.join(
        [letter if letter in used_letters else '*' for letter in searched_letters]
    )
    if searched_word_with_spaces != searched_word_w_spaces:
        guesses -= 1
        word_entry.config(text=searched_word_with_spaces)
        check_progress()
    searched_word_w_spaces = searched_word_with_spaces
    word_entry.config(text=searched_word_w_spaces)
    check_progress()


root = Tk()
root.geometry("620x155")
root.title('hangman by SB')

fr0 = ttk.Frame(root, width=20)
fr0.grid(column=0, row=1, sticky='news')
fr1 = ttk.Frame(root)
fr1.grid(column=1, row=1, sticky='news')
fr2 = ttk.Frame(root, width=20)
fr2.grid(column=0, row=3, sticky='news')
fr3 = ttk.Frame(root)
fr3.grid(column=1, row=3, sticky='news')
fr4 = ttk.Frame(root, height=5)
fr4.grid(column=0, columnspan=2, row=2, sticky='news')
fr01 = ttk.Frame(root, height=10)
fr01.grid(column=0, columnspan=2, row=0, sticky='news')

buttons_hash_table = {}
word_entry = ttk.Label(fr1, text='', font=('Arial', 12))
word_entry.grid(column=2, row=1, sticky='wn')
ttk.Label(fr1, width=20).grid(column=0, row=1, sticky='nw')
w_label = ttk.Label(fr0, text='Guess the word:', width=18, foreground='darkgreen')
end_label = ttk.Label(fr0, text='', width=18)
ttk.Label(fr0, width=2).grid(column=1, row=1, sticky='news')
w_label.grid(column=2, row=1, sticky='news')

ttk.Label(fr2, width=2).grid(column=0, row=2, rowspan=4)
shown1_0 = ttk.Label(fr2, text='|', padding=0)
shown1_1 = ttk.Label(fr2, text='|', padding=0)
shown1_2 = ttk.Label(fr2, text='|', padding=0)
shown1_3 = ttk.Label(fr2, text='|', padding=0)
shown1_4 = ttk.Label(fr2, text='|', padding=0)
shown2 = ttk.Label(fr2, text='________')
shown3 = ttk.Label(fr2, text='|')
shown4 = ttk.Label(fr2, text='o')
shown5 = ttk.Label(fr2, text='|')
shown6 = ttk.Label(fr2, text='         /')
shown7 = ttk.Label(fr2, text="\\")
shown8 = ttk.Label(fr2, text='         /')
shown9 = ttk.Label(fr2, text="\\")

image_file = ttk.Label(fr2)
photos = [PhotoImage(file="images/winner.png"), PhotoImage(file="images/hanged1-removebg-preview.png")]
ascii_art = (
    shown1_0, shown1_1, shown1_2, shown1_3, shown1_4, shown2, shown3, shown4, shown5, shown6, shown7, shown8, shown9
)

grid_values_picture = {
    0: [],
    1: [[shown1_0, (1, 2)], [shown1_1, (1, 3)], [shown1_2, (1, 4)], [shown1_3, (1, 5)], [shown1_4, (1, 6)]],
    2: [shown2, (2, 1)],
    3: [shown3, (3, 2)],
    4: [shown4, (3, 3)],
    5: [shown5, (3, 4)],
    6: [shown6, (2, 4)],
    7: [shown7, (4, 4)],
    8: [shown9, (4, 5)],
    9: [shown8, (2, 5)],
}
searched_word_w_spaces = ''
guesses = 0
make_buttons()
new_game()

root.mainloop()
