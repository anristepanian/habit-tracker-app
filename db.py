import sqlite3
import datetime as date


class DB:
    """The DB class consists of essential methods for interacting with database.

    Methods:
        get_db(name="main.db"): Creates a connection with a database.
        create_tables(db): Creates the Habit, Streak and Track tables in the database, if they don't exist already.
        add_habit(db, name, description, start_date, valid_till, periodicity): Inserts the habit's data into the Habit
        table.
        habit_check(db, name, check, check_date): Inserts the habit's data into the Tracker table.
        add_streak(db, name, current_streak, longest_streak, break_count, last_break): Inserts the habit's data
        into the Streak table.
        update_habit(db, name, streak, last_check, status, end_date): Updates the habit's data in the Habit table.
        update_streak(db, name, current_streak, longest_streak, break_count, last_break): Updates the habit's data
        in the Streak table.
        get_habit_data(db, status="Still in progress"): Returns all necessary data from Habit table.
        def get_cur_streak(cls, db, name, status="Still in progress"): Returns the current streak of a habit.
        delete_habit(db, name): Deletes certain habit data from the Habit table.
        delete_streak(db, name): Deletes the certain habit data from the Streak table.
        delete_tracker(db, name): Deletes the certain habit data from the Tracker table.
        name_to_id(db, name): Returns the habit's id, when the habit's name is passed and the habit's status is "Still
        in progress".
        db_close(db): Closes the database.
    """
    @classmethod
    def get_db(cls, name="main.db"):
        """
        Creates a connection with a database.

        :param name: Name of a database.
        :type name: str
        :return: Returns the database.
        :rtype: class
        """
        db = sqlite3.connect(name, timeout=5)
        cls.create_tables(db)
        return db

    @staticmethod
    def create_tables(db):
        """
        Creates the Habit, Streak and Track tables in the database, if they don't exist already.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        cur = db.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS habit (
            habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            start_date TEXT,
            valid_till TEXT,
            periodicity TEXT,
            status TEXT,
            streak INTEGER,
            last_check TEXT,
            end_date TEXT,
            last_check_week TEXT,
            last_check_day TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            habit_id INTEGER PRIMARY KEY,
            current_streak INTEGER,
            longest_streak INTEGER,
            break_count INTEGER,
            last_break TEXT,
            FOREIGN KEY (habit_id) REFERENCES habit(habit_id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS tracker (
            tracker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            checked_off INTEGER,
            date TEXT,
            FOREIGN KEY (habit_id) REFERENCES habit(habit_id)
        )
        """)

        db.commit()

    @staticmethod
    def add_habit(db, name, description, start_date, valid_till, periodicity):
        """
        Inserts the habit's data into the Habit table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param description: The description of a habit.
        :type description: str
        :param start_date: The start date of a habit.
        :type start_date: str
        :param valid_till: The expiration date of a habit.
        :type valid_till: str
        :param periodicity: The periodicity of a habit (i.e. "Daily", "Weekly").
        :type periodicity: str
        :return: None
        """
        cur = db.cursor()
        if not start_date:
            start_date = str(date.date.today())
        try:
            cur.execute("""
            INSERT INTO
            habit(name, description, start_date, valid_till, periodicity, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, start_date, valid_till, periodicity, "Still in progress"))
        except sqlite3.IntegrityError:
            print(f"\nYou can't create a habit with name: {name}\nBecause it already exists!\nBefore creating a new"
                  f"habit with {name} name\nYou should delete the previous one!\n")
            return True
        db.commit()

    @classmethod
    def habit_check(cls, db, name, check, check_date, status="Still in progress"):
        """
        Inserts the habit's data into the Tracker table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param check: The check-off (i.e. True or False).
        :type check: bool
        :param check_date: The check date.
        :type check_date: str
        :param status: The status of a habit.
        :type status: str
        :return:
        """
        cur = db.cursor()
        habit_id = cls.name_to_id(db, name, status)
        if not check_date:
            check_date = str(date.date.today())
        cur.execute("""
            INSERT INTO
            tracker(habit_id, checked_off, date)
            VALUES (?, ?, ?)
            """, (habit_id, check, check_date))
        db.commit()

    @classmethod
    def add_streak(cls, db, name, current_streak, longest_streak, break_count, last_break):
        """
        Inserts the habit's data into the Streak table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param current_streak: The current streak of a habit.
        :type current_streak: int
        :param longest_streak: The longest streak of a habit.
        :type longest_streak: int
        :param break_count: The count of breaks of a habit.
        :type break_count: int
        :param last_break: The date of last break of a habit.
        :type last_break: str
        :return: None
        """
        cur = db.cursor()
        if not last_break:
            last_break = "Not broken"
        try:
            cur.execute("""
            INSERT INTO
            streak(habit_id)
            SELECT habit_id FROM habit
            WHERE name = ?
            """, (name,))
            cur.execute("""
            UPDATE streak
            SET current_streak = ?, longest_streak = ?, break_count = ?, last_break = ?
            WHERE habit_id IN (
                SELECT habit_id FROM habit
                WHERE name = ?
            );
            """, (current_streak, longest_streak, break_count, last_break, name))
        except sqlite3.IntegrityError:
            print("\n You are trying to interact with habit, that doesn't exist!\n")
        db.commit()

    @classmethod
    def update_habit(cls, db, name, streak, last_check, status, end_date, last_check_week, last_check_day):
        """
        Updates the habit's data in the Habit table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param streak: The boolean value.
        :type streak: bool
        :param last_check: The date of last check of a habit.
        :type last_check: str
        :param status: The status of the habit.
        :type status: str
        :param end_date: The date when the habit's status has become "Completed" or "Broken".
        :type end_date: str
        :param last_check_week: The last checked-off week.
        :type last_check_week: str
        :param last_check_day: The last checked-off day's date.
        :type last_check_day: str
        :return: None
        """
        cur = db.cursor()
        try:
            cur.execute("""
                UPDATE habit
                SET streak = ?, last_check = ?, status = ?, end_date = ?, last_check_week = ?, last_check_day = ?
                WHERE habit_id IN (
                    SELECT habit_id FROM habit
                    WHERE name = ?
                );
                """, (streak, last_check, status, end_date, last_check_week, last_check_day, name))
        except sqlite3.IntegrityError:
            print("\n You are trying to interact with habit, that doesn't exist!\n")
        db.commit()

    @classmethod
    def update_streak(cls, db, name, current_streak, longest_streak, break_count, last_break):
        """
        Updates the habit's data in the Streak table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param current_streak: The current streak of a habit.
        :type current_streak: int
        :param longest_streak: The longest streak of a habit.
        :type longest_streak: int
        :param break_count: The count of breaks of a habit.
        :type break_count: int
        :param last_break: The date of last break of a habit.
        :type last_break: str
        :return: None
        """
        cur = db.cursor()
        try:
            cur.execute("""
            UPDATE streak
            SET current_streak = ?, longest_streak = ?, break_count = ?, last_break = ?
            WHERE habit_id IN (
                SELECT habit_id FROM habit
                WHERE name = ?
            );
            """, (current_streak, longest_streak, break_count, last_break, name))
        except sqlite3.IntegrityError:
            print("\n You are trying to interact with habit, that doesn't exist!\n")
        db.commit()

    @staticmethod
    def get_habit_data(db):
        """
        Returns all necessary data from Habit table.

        :param db: The database, to which you are connected.
        :type db: class
        :return: Returns all necessary data from Habit table.
        :rtype: list
        """
        cur = db.cursor()
        cur.execute("""SELECT habit.name, habit.start_date, habit.valid_till, habit.periodicity, habit.status, 
        streak.current_streak, streak.longest_streak, streak.break_count, streak.last_break, habit.last_check_day,
        habit.last_check_week
        FROM habit
        LEFT JOIN streak on habit.habit_id = streak.habit_id""")
        return cur.fetchall()

    @classmethod
    def get_cur_streak(cls, db, name, status="Still in progress"):
        """
        Returns the current streak of a habit.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param status: The status of a habit.
        :type status: str
        :return: Returns the current streak of a habit.
        :rtype: int
        """
        habit_id = cls.name_to_id(db, name, status)
        cur = db.cursor()
        cur.execute("""SELECT current_streak FROM streak
        WHERE habit_id = ?""", (habit_id,))
        select = cur.fetchall()
        return select[0][0]

    @classmethod
    def delete_habit(cls, db, name):
        """
        Deletes certain habit data from the Habit table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :return: None
        """
        cls.delete_tracker(db, name)
        cls.delete_streak(db, name)
        cur = db.cursor()
        cur.execute("""
        SELECT * FROM habit
        WHERE name = ?
        """, (name,))
        if not cur.fetchall():
            return print(f"\nThere is no such a habit called {name}\n")
        cur.execute("""
        DELETE FROM habit
        WHERE name = ?
        """, (name,))
        db.commit()
        print(f"\nYou just deleted the {name} habit!\n")

    @classmethod
    def delete_streak(cls, db, name):
        """
        Deletes the certain habit data from the Streak table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :return: None
        """
        cur = db.cursor()
        cur.execute("""
        DELETE FROM streak
        WHERE habit_id IN (
            SELECT habit_id FROM habit
            WHERE name = ?
        );
        """, (name,))
        db.commit()

    @classmethod
    def delete_tracker(cls, db, name):
        """
        Deletes the certain habit data from the Tracker table.

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :return: None
        """
        cur = db.cursor()
        cur.execute("""
        DELETE FROM tracker
        WHERE habit_id IN (
            SELECT habit_id FROM habit
            WHERE name = ?
        );
        """, (name,))
        db.commit()
        cur.close()

    @staticmethod
    def name_to_id(db, name, status="Still in progress"):
        """
        Returns the habit's id, when the habit's name is passed and the habit's status is "Still in progress".

        :param db: The database, to which you are connected.
        :type db: class
        :param name: The name of a habit.
        :type name: str
        :param status: The status of a habit.
        :type status: str
        :return: returns the habit's id
        :rtype: int
        """
        cur = db.cursor()
        cur.execute("""
        SELECT habit_id
        FROM habit 
        WHERE name = ? AND status = ?""", (name, status))
        try:
            return cur.fetchone()[0]
        except TypeError:
            print("\nThe name of a habit is wrong, or it is currently not in progress\n"
                  "Please try to write the name of a habit correctly,\n"
                  "Or select a habit, that is currently in progress!\n")
            return "Error"

    @staticmethod
    def db_close(db):
        """
        Closes the database.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        db.close()
