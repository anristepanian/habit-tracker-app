from habit_track import DbHabit
from db import DB


class PredefinedHabits:
    """The PredefinedHabits class is used to create predefined habits.

    Methods:
        documenting_code(db): Creates a habit called "Documenting code" and inserts data of checking-off the habit for
        a period of 4 weeks.
        naming_variables_properly(db): Creates a habit called "Naming variables properly" and inserts data of
        checking-off the habit for a period of 4 weeks.
        not_drinking_coffee(db): Creates a habit called "Not drinking coffee" and inserts data of checking-off the
        habit for a period of 4 weeks.
        not_skipping_leg_day(db): Creates a habit called "Not skipping leg day" and inserts data of checking-off the
        habit for a period of 4 weeks.
        writing_oop_code(db): Creates a habit called "Writing OOP code" and inserts data of checking-off the habit for
        a period of 4 weeks.
    """
    @staticmethod
    def documenting_code(db):
        """
        Creates a habit called "Documenting code" and inserts data of checking-off the habit for a period of 4 weeks.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DbHabit("Documenting code",
                        "Code documenting is essential to make your code more cleaner, yet programmers hate "
                        "documenting their code!",
                        "2024-12-23",
                        "2025-02-10", "Weekly")
        habit.store(db)
        habit.add_habit_check(db, True, "2024-12-23")
        habit.add_habit_check(db, True, "2024-12-30")
        habit.add_habit_check(db, True, "2025-01-06")
        habit.add_habit_check(db, True, "2025-01-13")
        habit.add_habit_check(db, True, "2025-01-29")

    @staticmethod
    def naming_variables_properly(db):
        """
        Creates a habit called "Naming variables properly" and inserts data of checking-off the habit for a period of 4
        weeks.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DbHabit("Naming variables properly",
                        "Naming variables properly is essential to make your code more cleaner, yet programmers hate "
                        "documenting their code!",
                        "2024-12-24",
                        "2025-02-04", "Weekly")
        habit.store(db)
        habit.add_habit_check(db, True, "2024-12-30")
        habit.add_habit_check(db, True, "2024-12-31")
        habit.add_habit_check(db, True, "2025-01-20")
        habit.add_habit_check(db, True, "2025-02-04")

    @staticmethod
    def not_drinking_coffee(db):
        """
        Creates a habit called "Not drinking coffee" and inserts data of checking-off the habit for a period of 4 weeks.

        param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DbHabit("Not drinking coffee",
                        "Regular coffee consumption causes addiction!",
                        "2024-12-25",
                        "2025-01-22", "Daily")
        habit.store(db)
        habit.add_habit_check(db, True, "2024-12-26")
        habit.add_habit_check(db, True, "2024-12-27")
        habit.add_habit_check(db, True, "2024-12-28")
        habit.add_habit_check(db, True, "2024-12-29")
        habit.add_habit_check(db, True, "2024-12-30")
        habit.add_habit_check(db, False, "2024-12-31")
        habit.add_habit_check(db, True, "2025-01-01")
        habit.add_habit_check(db, True, "2025-01-02")
        habit.add_habit_check(db, True, "2025-01-03")
        habit.add_habit_check(db, True, "2025-01-04")
        habit.add_habit_check(db, True, "2025-01-05")
        habit.add_habit_check(db, True, "2025-01-06")
        habit.add_habit_check(db, True, "2025-01-07")
        habit.add_habit_check(db, True, "2025-01-08")
        habit.add_habit_check(db, True, "2025-01-09")
        habit.add_habit_check(db, True, "2025-01-10")
        habit.add_habit_check(db, True, "2025-01-11")
        habit.add_habit_check(db, True, "2025-01-12")
        habit.add_habit_check(db, True, "2025-01-13")
        habit.add_habit_check(db, True, "2025-01-14")
        habit.add_habit_check(db, True, "2025-01-15")
        habit.add_habit_check(db, True, "2025-01-16")
        habit.add_habit_check(db, True, "2025-01-17")
        habit.add_habit_check(db, True, "2025-01-18")
        habit.add_habit_check(db, True, "2025-01-19")
        habit.add_habit_check(db, True, "2025-01-20")
        habit.add_habit_check(db, True, "2025-01-21")
        habit.add_habit_check(db, True, "2025-01-22")

    @staticmethod
    def not_skipping_leg_day(db):
        """
        Creates a habit called "Not skipping leg day" and inserts data of checking-off the habit for a period of 4
        weeks.

        param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DbHabit("Not skipping leg day",
                        "Most of those who work out hate the leg days in the gym, however training legs is important "
                        "for building a strong body!",
                        "2024-12-26",
                        "2025-01-30", "Weekly")
        habit.store(db)
        habit.add_habit_check(db, True, "2025-01-10")
        habit.add_habit_check(db, True, "2025-01-16")
        habit.add_habit_check(db, True, "2025-01-29")
        habit.add_habit_check(db, True, "2025-01-31")

    @staticmethod
    def writing_oop_code(db):
        """
        Creates a habit called "Writing OOP code" and inserts data of checking-off the habit for a period of 4 weeks.

        param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DbHabit("Writing OOP code",
                        "Python allows users to write linear code, however it is better practice to write OOP code!",
                        "2024-12-27",
                        "2025-02-28", "Weekly")
        habit.store(db)
        habit.add_habit_check(db, True, "2025-01-02")
        habit.add_habit_check(db, True, "2025-01-08")
        habit.add_habit_check(db, True, "2025-01-10")
        habit.add_habit_check(db, True, "2025-01-17")
        habit.add_habit_check(db, True, "2025-02-05")


my_db = DB.get_db()
PredefinedHabits.documenting_code(my_db)
PredefinedHabits.naming_variables_properly(my_db)
PredefinedHabits.not_drinking_coffee(my_db)
PredefinedHabits.not_skipping_leg_day(my_db)
PredefinedHabits.writing_oop_code(my_db)
