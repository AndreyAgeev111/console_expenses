from command import *


def receive():
    get_instructions()
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


def out_azure(text):
    return "\033[36m {}".format(text)


def get_instructions():
    print(f'COMMANDS:'
          f'\n {out_azure("add section")}\033[0m --- add new section for expenses, '
          f'{out_azure("arguments")}\033[0m: name of section'
          f'\n {out_azure("delete section")}\033[0m --- delete one section, '
          f'{out_azure("arguments")}\033[0m: name of section'
          f'\n {out_azure("delete expense")}\033[0m --- delete expense with a comment and date, '
          f'{out_azure("arguments")}\033[0m: name of section, comment on expense, date of expense'
          f'\n {out_azure("add expense")}\033[0m --- add new expense in the section, '
          f' {out_azure("arguments")}\033[0m: name of section, price of expense, comment on expense'
          f'\n {out_azure("clear section")}\033[0m --- clear all expenses from, '
          f'{out_azure("arguments")}\033[0m: name of section'
          f'\n {out_azure("get expenses from")}\033[0m --- get expenses from one or more sections, '
          f'{out_azure("arguments")}\033[0m: name or names of sections'
          f'\n {out_azure("get sections")}\033[0m --- get all sections, {out_azure("arguments")}\033[0m: none\033[0m'
          f'\n {out_azure("get chart")}\033[0m --- get chart for all expenses, '
          f'{out_azure("arguments")}\033[0m: type of chart: bar or pie\033[0m')
