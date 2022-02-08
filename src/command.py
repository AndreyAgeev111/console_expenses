import datetime
from abc import ABC, abstractmethod
import pandas as pd
import psycopg2 as ps
import matplotlib.pyplot as plt
import numpy as np

connection = ps.connect(user="postgres",
                        password="superuser",
                        host="127.0.0.1",
                        port="5432",
                        dbname="expenses_app_db")
cursor = connection.cursor()
now = datetime.datetime.now()
current_date = f"{now.year}-{now.month}-{now.day}"


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class AddNewSection(Command):

    def __init__(self, section: str):
        self.section = section

    def execute(self) -> None:
        try:
            cursor.execute(f'INSERT INTO sections (section) VALUES (\'{self.section}\')')
            connection.commit()
        except ps.errors.UniqueViolation:
            print(f'Section {self.section} already exists')
            connection.rollback()

    @staticmethod
    def name() -> str:
        return 'add section'


class DeleteSection(Command):

    def __init__(self, section: str):
        self.section = section

    def execute(self) -> None:
        ClearSection(self.section).execute()
        cursor.execute(f'DELETE FROM sections WHERE section = \'{self.section}\'')
        connection.commit()

    @staticmethod
    def name() -> str:
        return 'delete section'


class AddNewExpense(Command):

    def __init__(self, section: str, price: float, comment: str):
        self.section = section
        self.price = price
        self.comment = comment.replace('-', ' ')

    def execute(self) -> None:
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
            id_section = cursor.fetchone()[0]
            cursor.execute(f'INSERT INTO expenses (price, comment, date_of_day, id_section) '
                           f'VALUES ({self.price}, \'{self.comment}\', \'{current_date})\', {id_section})')
            connection.commit()
        except TypeError:
            print(f'Section {self.section} does not exist')
        except ps.errors.CheckViolation:
            print('The price must be greater than 0!')
            connection.rollback()

    @staticmethod
    def name() -> str:
        return 'add expense'


class DeleteExpense(Command):

    def __init__(self, section: str, comment: str, date: str):
        self.section = section
        self.comment = comment.replace('-', ' ')
        self.date = date

    def execute(self) -> None:
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
            id_section = cursor.fetchone()[0]
            cursor.execute(f'DELETE FROM expenses WHERE date_of_day = \'{self.date}\' '
                           f'AND comment = \'{self.comment}\' AND id_section = {id_section}')
            connection.commit()
        except TypeError:
            print('This waste does not exist, please try another')
        except ps.errors.InvalidDatetimeFormat:
            print('The purchase date was entered incorrectly')

    @staticmethod
    def name() -> str:
        return 'delete expense'


class ClearSection(Command):

    def __init__(self, section: str):
        self.section = section

    def execute(self) -> None:
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
            id_section = cursor.fetchone()[0]
            cursor.execute(f'DELETE FROM expenses * WHERE id_section = {id_section}')
            connection.commit()
        except TypeError:
            print(f'Section {self.section} does not exist')

    @staticmethod
    def name() -> str:
        return 'clear section'


class GetExpensesFromSection(Command):

    def __init__(self, sections: str):
        self.sections = sections

    @staticmethod
    def get_expenses_from_sections(section) -> None:
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{section}\'')
            id_sect = cursor.fetchone()[0]
            expense_table = pd.read_sql(f'SELECT * FROM expenses WHERE id_section = \'{id_sect}\'', connection)
            print(pd.DataFrame(expense_table).drop(columns=['id', 'id_section']))
        except TypeError:
            print(f'Section {section} does not exist')

    def execute(self) -> None:
        self.sections = self.sections.split(", ")
        if len(self.sections) != 1:
            for section in self.sections:
                self.get_expenses_from_sections(section)
        else:
            self.get_expenses_from_sections(self.sections[0])


class GetSections(Command):

    def execute(self) -> None:
        sections_table = pd.read_sql('SELECT section FROM sections', connection)
        print(sections_table)


class GetChart(Command):

    def __init__(self, type_of_chart: str):
        self.type_of_chart = type_of_chart

    @staticmethod
    def get_chart() -> tuple:
        section_labels = list(pd.read_sql('SELECT section FROM sections', connection)['section'])
        length_of_labels = len(section_labels)
        expenses = [0] * length_of_labels

        for j in range(length_of_labels):
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{section_labels[j]}\'')
            id_sect = cursor.fetchone()[0]
            expense_table = list(pd.DataFrame(
                pd.read_sql(f'SELECT * FROM expenses WHERE id_section = \'{id_sect}\'', connection))['price'])
            for i in range(len(expense_table)):
                expenses[j] += float(expense_table[i])

        flag = True
        while flag:
            try:
                zero_index = expenses.index(0)
                expenses.pop(zero_index)
                section_labels.pop(zero_index)
            except ValueError:
                flag = False
        id_moneybox = section_labels.index('moneybox')
        expenses.pop(id_moneybox)
        section_labels.pop(id_moneybox)

        return expenses, section_labels

    def execute(self) -> None:
        expenses, section_labels = self.get_chart()
        if self.type_of_chart == 'pie':
            plt.title(f'Total expenses = {sum(expenses)}')
            plt.pie(expenses, labels=section_labels, autopct='%1.1f%%')
            plt.axis('equal')
            plt.show()
        elif self.type_of_chart == 'bar':
            index = np.arange(len(expenses))
            plt.title(f'Total expenses = {sum(expenses)}')
            plt.bar(index, expenses)
            plt.xticks(index, section_labels)
            plt.show()
        else:
            print('Unknown type of chart, please choose: pie or bar')


class AddCoinsToMoneybox(Command):

    def __init__(self, price: float, comment: str):
        self.price = price
        self.comment = comment.replace('-', ' ')

    def execute(self):
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'moneybox\'')
            id_section = cursor.fetchone()[0]
            cursor.execute(f'INSERT INTO expenses (price, comment, date_of_day, id_section) '
                           f'VALUES ({self.price}, \'{self.comment}\', \'{current_date})\', {id_section})')
            connection.commit()
        except ps.errors.CheckViolation:
            print('The money must be greater than 0!')
            connection.rollback()


class CheckMoneyBox(Command):

    def execute(self):
        section_labels = list(pd.read_sql('SELECT section FROM sections', connection)['section'])
        length_of_labels = len(section_labels)
        expenses = [0] * length_of_labels

        for j in range(length_of_labels):
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{section_labels[j]}\'')
            id_sect = cursor.fetchone()[0]
            expense_table = list(pd.DataFrame(
                pd.read_sql(f'SELECT * FROM expenses WHERE id_section = \'{id_sect}\'', connection))['price'])
            for i in range(len(expense_table)):
                expenses[j] += float(expense_table[i])
        id_moneybox = section_labels.index('moneybox')
        moneybox = expenses.pop(id_moneybox)
        print(f'There are now {moneybox - sum(expenses)} in the moneybox')


COMMANDS = {'add section': AddNewSection,
            'delete section': DeleteSection,
            'delete expense': DeleteExpense,
            'add expense': AddNewExpense,
            'clear section': ClearSection,
            'get expenses from': GetExpensesFromSection,
            'get sections': GetSections,
            'get chart': GetChart,
            'add to moneybox': AddCoinsToMoneybox,
            'check moneybox': CheckMoneyBox
            }
