from command import *


def out_azure(text):
    return "\033[36m {}\033[0m".format(text)


def get_instructions(function):
    def wrapped():
        print(f'COMMANDS:'
              f'\n {out_azure("add section")} --- add new section for expenses, '
              f'{out_azure("arguments")}: name of section'
              f'\n {out_azure("delete section")} --- delete one section, '
              f'{out_azure("arguments")}: name of section'
              f'\n {out_azure("delete expense")} --- delete expense with a comment and date, '
              f'{out_azure("arguments")}: name of section, comment on expense, date of expense'
              f'\n {out_azure("add expense")} --- add new expense in the section, '
              f'{out_azure("arguments")}: name of section, price of expense, comment on expense'
              f'\n {out_azure("clear section")} --- clear all expenses from, '
              f'{out_azure("arguments")}: name of section'
              f'\n {out_azure("get expenses from")} --- get expenses from one or more sections, '
              f'{out_azure("arguments")}: name or names of sections'
              f'\n {out_azure("get sections")} --- get all sections, {out_azure("arguments")}: none'
              f'\n {out_azure("get chart")} --- get chart for all expenses, '
              f'{out_azure("arguments")}: type of chart: bar or pie'
              f'\n {out_azure("add to moneybox")} --- add money to your moneybox,'
              f'{out_azure("arguments")}: money to add and comment'
              f'\n {out_azure("check moneybox")} --- check balance of the moneybox, '
              f'{out_azure("arguments")}: none')
        function()
    return wrapped


@get_instructions
def receive():
    while True:
        print('Please enter the command')
        cmd = input("pysh >> ").strip()
        if cmd == 'quit':
            print('Goodbye!')
            break
        try:
            try:
                if cmd == 'get expenses from':
                    args = input()
                    command = COMMANDS[cmd](args)
                else:
                    args = input().split()
                    command = COMMANDS[cmd](*args)
                command.execute()
            except TypeError:
                print("You have not entered any arguments")
        except KeyError:
            print(f'{cmd} is unknown command!')
            print(' Try another:')