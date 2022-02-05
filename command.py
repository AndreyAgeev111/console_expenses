import datetime
from abc import ABC, abstractmethod
import pandas as pd
import psycopg2 as ps
import matplotlib.pyplot as plt

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

    def execute(self):
        try:
            cursor.execute(f'INSERT INTO sections (section) VALUES (\'{self.section}\')')
            connection.commit()
        except ps.errors.UniqueViolation:
            print(f'Section {self.section} already exists')
            connection.rollback()

    @staticmethod
    def name():
        return 'add section'


class DeleteSection(Command):

    def __init__(self, section: str):
        self.section = section

    def execute(self):
        ClearSection(self.section).execute()
        cursor.execute(f'DELETE FROM sections WHERE section = \'{self.section}\'')
        connection.commit()

    @staticmethod
    def name():
        return 'delete section'


class AddNewExpense(Command):

    def __init__(self, section: str, price: float, comment: str):
        self.section = section
        self.price = price
        self.comment = comment.replace('-', ' ')

    def execute(self):
        cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
        id_section = cursor.fetchone()[0]
        cursor.execute(f'INSERT INTO expenses (price, comment, date_of_day, id_section) '
                       f'VALUES ({self.price}, \'{self.comment}\', \'{current_date})\', {id_section})')
        connection.commit()

    @staticmethod
    def name():
        return 'add expense'


class DeleteExpense(Command):

    def __init__(self, section: str, comment: str, date: str):
        self.section = section
        self.comment = comment.replace('-', ' ')
        self.date = date

    def execute(self):
        cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
        id_section = cursor.fetchone()[0]
        cursor.execute(f'DELETE FROM expenses WHERE date_of_day = \'{self.date}\' '
                       f'AND comment = \'{self.comment}\' AND id_section = {id_section}')
        connection.commit()

    @staticmethod
    def name():
        return 'delete expense'


class ClearSection(Command):

    def __init__(self, section: str):
        self.section = section

    def execute(self):
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{self.section}\'')
            id_section = cursor.fetchone()[0]
            cursor.execute(f'DELETE FROM expenses * WHERE id_section = {id_section}')
            connection.commit()
        except TypeError:
            print(f'Section {self.section} does not exist')

    @staticmethod
    def name():
        return 'clear section'


class GetExpensesFromSection(Command):

    def __init__(self, sections: str):
        self.sections = sections

    @staticmethod
    def get_expenses_from_sections(section):
        try:
            cursor.execute(f'SELECT id FROM sections WHERE section = \'{section}\'')
            id_sect = cursor.fetchone()[0]
            expense_table = pd.read_sql(f'SELECT * FROM expenses WHERE id_section = \'{id_sect}\'', connection)
            print(pd.DataFrame(expense_table).drop(columns=['id', 'id_section']))
        except TypeError:
            print(f'Section {section} does not exist')

    def execute(self):
        self.sections = self.sections.split(", ")
        if len(self.sections) != 1:
            for section in self.sections:
                self.get_expenses_from_sections(section)
        else:
            self.get_expenses_from_sections(self.sections[0])


class GetSections(Command):

    def execute(self):
        sections_table = pd.read_sql('SELECT section FROM sections', connection)
        print(sections_table)


class GetPieChart(Command):

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
                expenses[j] += int(expense_table[i])

        flag = True
        while flag:
            try:
                zero_index = expenses.index(0)
                expenses.pop(zero_index)
                section_labels.pop(zero_index)
            except ValueError:
                flag = False
        plt.title('Total expenses')
        plt.pie(expenses, labels=section_labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()


COMMANDS = {'add section': AddNewSection,
            'delete section': DeleteSection,
            'delete expense': DeleteExpense,
            'add expense': AddNewExpense,
            'clear section': ClearSection,
            'get expenses from': GetExpensesFromSection,
            'get sections': GetSections,
            'get pie chart': GetPieChart
            }
