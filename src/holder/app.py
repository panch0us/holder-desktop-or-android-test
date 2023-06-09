"""
Property accounting
"""
import toga
import sqlite3
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from holder.property import Property    # работа с имуществом


def db_create() -> None:
    #connection = sqlite3.connect("C:\\Users\\savkin\\Desktop\\home\\projects\\windows\\python\\holder\\holder\\src\\holder\\holder.db")
    connection = sqlite3.connect("/data/data/ru.panchous.holder/holder.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS property(title, kind)")
    cursor.close()
    connection.close()


def db_property_add(property: Property) -> None:
    #connection = sqlite3.connect("C:\\Users\\savkin\\Desktop\\home\\projects\\windows\\python\\holder\\holder\\src\\holder\\holder.db")
    connection = sqlite3.connect("/data/data/ru.panchous.holder/holder.db")
    connection = connection
    property = property
    cursor = connection.cursor()
    rows = [(property.title, property.kind)]
    cursor.executemany("INSERT INTO property(title, kind) VALUES(?,?)", rows)
    connection.commit()
    cursor.close()

def db_property_look():
    #connection = sqlite3.connect("C:\\Users\\savkin\\Desktop\\home\\projects\\windows\\python\\holder\\holder\\src\\holder\\holder.db")
    connection = sqlite3.connect("/data/data/ru.panchous.holder/holder.db")
    connection = connection
    cursor = connection.cursor()
    result = cursor.execute("SELECT title, kind FROM property")
    result = result.fetchall()
    cursor.close()
    return result

connection = db_create()


class Holder(toga.App):

    def startup(self):
        self.menu_box = toga.Box(style=Pack(direction=COLUMN))

        button_add = toga.Button("ДОБАВЛЕНИЕ", on_press=self.property_add, style=Pack(padding=(5, 5)))
        button_look = toga.Button("ПРОСМОТР", on_press=self.property_look, style=Pack(padding=5))
        button_export = toga.Button("ВЫГРУЗКА", on_press=self.property_add, style=Pack(padding=5))
        button_help = toga.Button("ПОМОЩЬ", on_press=self.property_add, style=Pack(padding=5))
        button_support = toga.Button("ОБРАТНАЯ СВЯЗЬ", on_press=self.property_add, style=Pack(padding=5))

        self.menu_box.add(button_add)
        self.menu_box.add(button_look)
        self.menu_box.add(button_export)
        self.menu_box.add(button_help)
        self.menu_box.add(button_support)


        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.menu_box
        self.main_window.show()

    def back_menu(self, widget):
        self.main_window.content = self.menu_box

    def add_property_in_db(self, widget):
        self.property = Property(self.title_input.value, self.kind_input.value)
        db_property_add(self.property)
        print(f"Property: '{self.property.title}' add!")
        self.title_input.value = ''
        self.kind_input.value = ''


    def property_add(self, widget):
        self.add_box = toga.Box(style=Pack(direction=COLUMN))

        # Блок добавления названия имущества (title)
        title_label = toga.Label("Название: ", style=Pack(padding=(3, 0)))
        self.title_input = toga.TextInput(style=Pack(flex=1))  # flex - растягивает во всю длинну
        self.add_box.add(title_label)
        self.add_box.add(self.title_input)

        # Блок добавления вида имущества (kind)
        kind_label = toga.Label("Вид: ", style=Pack(padding=(3, 0)))
        self.kind_input = toga.TextInput(style=Pack(flex=1))  # flex - растягивает во всю длинну
        self.add_box.add(kind_label)
        self.add_box.add(self.kind_input)


        button = toga.Button("Добавить", on_press=self.add_property_in_db, style=Pack(padding=5))
        button_home = toga.Button("На главную", on_press=self.back_menu, style=Pack(padding=5))

        self.add_box.add(title_label)
        self.add_box.add(kind_label)
        self.add_box.add(button)
        self.add_box.add(button_home)

        self.main_window.content = self.add_box # Вместо главного меню показываем окно добавления имущества

    def property_look(self, widget):
        result = db_property_look()

        self.look_box = toga.Box(style=Pack(direction=COLUMN))
        title_label = toga.Label("Список всего имущества: ", style=Pack(padding=(3, 0)))
        table = toga.Table(['Название', 'Вид', 'id'])
        #for el in result:
        #    table.data.append(el[0], el[1])

        self.look_box.add(title_label)
        self.look_box.add(table)

        self.main_window.content = self.look_box # Вместо главного меню показываем окно добавления имущества


def main():
    return Holder()