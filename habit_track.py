from db import DB
import datetime as date


class Habit:
    """The Habit class is used to track habits.

    Attributes:
        name (str): The name of a habit.
        description (str): The description of a habit.
        start_date (str): The start date of a habit.
        valid_till (str): The expiration date of a habit.
        periodicity (str): The periodicity of a habit (i.e. "Daily", "Weekly").
        current_streak (int): The current streak of a habit (default 0).
        longest_streak (int): The longest streak of a habit (default 0).
        break_count (int): The count of breaks of a habit (default 0).
        last_break (str): The date of last break of a habit (default "").

    Methods:
        streak_increase_ln_check(): Increases the current streak, and also increases the longest streak if needed.
        break_count_check(): Checks whether the break count is equal 3, if so changes "self.status" to "Broken".
    """
    def __init__(self, name: str, description: str, start_date: str, valid_till: str, periodicity: str,
                 current_streak=0, longest_streak=0, break_count=0, last_break=""):
        """
        Initializes a Habit instance.

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
        :param current_streak: The current streak of a habit (default 0).
        :type current_streak: int
        :param longest_streak: The longest streak of a habit (default 0).
        :type longest_streak: int
        :param break_count: The count of breaks of a habit (default 0).
        :type break_count: int
        :param last_break: The date of last break of a habit (default "").
        :type last_break: str
        """
        self.name = name
        self.description = description
        self.start_date = start_date
        self.valid_till = valid_till
        self.periodicity = periodicity
        self.status = "Still in progress"
        self.end_date = "Not ended"
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.break_count = break_count
        self.last_break = last_break

    def streak_increase_ln_check(self):
        """
        Increases the current streak, and also increases the longest streak if needed.

        :return: None
        """
        self.current_streak += 1
        if self.longest_streak < self.current_streak:
            self.longest_streak = self.current_streak

    def break_count_check(self):
        """
        Checks whether the break count is equal 3, if so changes "self.status" to "Broken".

        :return: None
        """
        if self.break_count >= 3:
            print(
                "\nUnfortunately you have broken your habit too many times!\n"
                "You have to start again!\nYou are free to create a habit, that has the same name!\n")
            self.status = "Broken"


class DbHabit(Habit):
    """The DbHabit class that extends the Habit class.

    Inherits from:
        Habit

    Additional Attributes:
        streak (bool): The boolean value, that is needed to decide whether to insert streak data into Track table, or
        to update them in database (default False).
        last_check (str): The date of last check of a habit, if the periodicity is "Weekly" "last_check" actually shows
        the first day of a week and not the actual date of last check (default "").

    Additional Methods:
        store(db): Inserts Habit data into the Habit table in the database.
        add_habit_check(db, check: bool, check_date: str): Inserts the check-off data, checks the missed check-off
        dates by calling the missed_dates(), checks whether the user has broken the habit by increasing the
        break_count, checks weather the user completed a habit by calling the check_progress().
        check_progress(db, check_date: str): Checks weather the user has completed a habit by confirming that the
        check_date is greater than or equal to the valid_date.
        missed_dates(db, check_date, check_date_dt, start_date_dt): Checks the missed check-off dates.
        drop(db): Deletes certain habit data from the database.
    """
    def __init__(self, name: str, description: str, start_date: str, valid_till: str, periodicity: str,
                 current_streak=0, longest_streak=0, break_count=0, last_break="", streak=False, last_check="",
                 last_check_week="", last_check_day=""):
        """
        Initializes a Habit instance.

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
        :param current_streak: The current streak of a habit (default 0).
        :type current_streak: int
        :param longest_streak: The longest streak of a habit (default 0).
        :type longest_streak: int
        :param break_count: The count of breaks of a habit (default 0).
        :type break_count: int
        :param last_break: The date of last break of a habit (default "").
        :type last_break: str
        :param streak: The boolean value, that is needed to decide whether to insert streak data into Track table, or
        to update them in database (default False).
        :type streak: bool
        :param last_check: The date of last check of a habit, if the periodicity is "Weekly" "last_check" actually
        shows the first day of a week and not the actual date of last check (default "").
        :type last_check: str
        :param last_check_week: The last checked-off week.
        :type last_check: str
        :param last_check_day: The last checked-off day's date.
        :type last_check: str
        """
        super().__init__(name, description, start_date, valid_till, periodicity, current_streak, longest_streak,
                         break_count, last_break)
        self.streak = streak
        self.last_check = last_check
        self.last_check_week = last_check_week
        self.last_check_day = last_check_day
        # Int variable needed for the further calculations of missed days (default 0).
        self.weeks = 0
        # Int variable needed for the further calculations of missed days (default 0).
        self.days = 0

    def store(self, db):
        """
        Inserts the Habit data into the Habit table in the database.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        habit = DB.add_habit(db, self.name, self.description, self.start_date, self.valid_till, self.periodicity)
        if not habit:
            print(f"\nCongratulations!!!\nYou have just created a habit, which is valid till {self.valid_till}!\n"
                  "In order to complete a habit, you should check it off\n"
                  "Every day if the periodicity is \"Daily\", or every week if it is \"Weekly\"!\n"
                  "If you break your habit 3 times, the habit status will become \"Broken\"\n"
                  "And you will be forced to create a new habit!\n")

    def add_habit_check(self, db, check: bool, check_date: str):
        """
        Inserts the check-off data, checks the missed check-off dates by calling the missed_dates(), checks whether the
        user has broken the habit by increasing the break_count, checks weather the user completed a habit by calling
        the check_progress().

        :param db: The database, to which you are connected.
        :type db: class
        :param check: The check-off (i.e. True or False).
        :type check: bool
        :param check_date: The check-off date.
        :type check_date: str
        :return: None
        """
        if self.status == "Still in progress":  # Checks whether the status is "Still in progress".
            if not check_date:  # Checks whether the user has passed the check date.
                check_date = str(date.date.today())  # If the user didn't, creates check_date gets the present day.
            else:
                check_date = str(check_date)  # Converts the check date into string.
            check_date_dt = date.date.fromisoformat(check_date)  # Creates a check date of a "date" class type.
            start_date_dt = date.date.fromisoformat(self.start_date)  # Creates a start date of a "date" class type.
            x = self.missed_dates(db, check_date, check_date_dt, start_date_dt)  # Checks the missed check-offs.
            if x == ConnectionError:
                # Checks whether the user entered wrong check-off date.
                return ConnectionError
            DB.habit_check(db, self.name, check, check_date, self.status)
            # Inserts data into the Tracker table in the "main.db".
            if self.status == "Broken":
                print(f"\nUnfortunately you have broken the {self.name} habit"
                      f"\nSince you have missed many check-off dates!\n")
            if self.status != "Broken":
                if check == 0:  # Checks whether the user has checked-off the habit or no.
                    self.break_count += 1  # Increases the break count.
                    self.break_count_check()  # Checks whether the break count has exceeded or is equal 3.
                    self.last_break = check_date  # Changes the last break date.
                    self.current_streak = 0  # Current streak becomes 0.
                    if self.status == "Broken":
                        # If the status of the habit is changed, changes the status in the main.db.
                        self.end_date = check_date
                if check == 1:  # In case the user has checked-off the habit, increases the streak.
                    self.streak_increase_ln_check()
                if self.status != "Broken":
                    _ = self.check_progress(db, check_date)
                    if _:
                        return print("\nCongratulations!!!\nYou have completed your habit!\n")
            if self.streak:
                # Checks whether the habit has already been checked-off at least once, in order either to call the
                # INSERT INTO Streak table SQL clause, or to call UPDATE Streak table's values SQL clause.
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
            else:
                self.streak = True
                DB.add_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                              self.last_break)
            DB.update_habit(db, self.name, self.streak, self.last_check, self.status, check_date, self.last_check_week,
                            self.last_check_day)
        else:  # In case the habit's status isn't "Still in progress", prints next message.
            print(f"\nYou can't check this habit since it is {self.status}!\nPlease select another habit or add it!\n")

    def check_progress(self, db, check_date: str):
        """
        Checks weather the user has completed a habit by confirming that the check_date is greater than or equal to the
        valid_date.

        :param db: The database, to which you are connected.
        :type db: class
        :param check_date: The check-off date.
        :type check_date: str
        :return: None
        """
        check_date_dt = date.date.fromisoformat(check_date)
        valid_till_dt = date.date.fromisoformat(self.valid_till)
        if check_date_dt >= valid_till_dt:  # Checks whether the check date has exceeded the expiration date.
            self.status = "Completed"
            self.end_date = check_date
            DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count, self.last_break)
            DB.update_habit(db, self.name, self.streak, self.last_check, self.status, check_date, self.last_check_week,
                            self.last_check_day)
            # Updates the main.db.
            return True
        else:
            # In case the check date hasn't yet exceeded the expiration date, prints motivational message.
            print(f"Still {valid_till_dt - check_date_dt} left!\nKeep it up!\n")

    def missed_dates(self, db, check_date, check_date_dt, start_date_dt):
        """
        Checks the missed check-off dates.

        :param db: The database, to which you are connected.
        :type db: class
        :param check_date: The check-off date.
        :type check_date: str
        :param check_date_dt: The check-off date.
        :type check_date_dt: class
        :param start_date_dt: The date of start.
        :type start_date_dt: class
        :return: None
        """
        """Variables "weeks" and "days" are needed, in order to calculate whether the check date comes after the start 
        date, or after the last check date, and how many days or weeks has passed after the start date, or after the
        last check date."""
        if self.periodicity == "Daily":
            self.weeks = 0
            self.days = 1
        elif self.periodicity == "Weekly":
            self.weeks = 1
            self.days = 0
        """If the periodicity is "Daily", the weeks becomes 0, and the days becomes 1, otherwise the weeks becomes 1,
        and the days becomes 0. It is all done because when calling date.timedelta, the program multiplies the weeks and
        the days variables with integer value. For example, in order to check, whether the user has missed more than 3
        days or weeks of checking-off the habit from the beginning, called next if statement:
        if check_date_dt >= start_date_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3).
        Now it's clear, that if the periodicity is "Daily", the weeks becomes 0 since 3 * 0 = 0."""
        if not self.last_check:
            if check_date_dt >= start_date_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3):
                self.last_break = str(start_date_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3))
                self.status = "Broken"
                self.break_count = 3
                self.current_streak = 0
                self.end_date = str(start_date_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3))
                self.last_check_day = check_date
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                DB.update_habit(db, self.name, self.streak, self.last_check, self.status, check_date,
                                self.last_check_week, self.last_check_day)
                self.last_check = str(start_date_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3))
            elif check_date_dt >= start_date_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2):
                self.last_break = str(start_date_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2))
                self.break_count = 2
                self.current_streak = 0
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                self.last_check = str(start_date_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2))
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = (f"{start_date_dt + date.timedelta(weeks=self.weeks * 2)} : "
                                            f"{start_date_dt + date.timedelta(days=20)}")
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            elif check_date_dt >= start_date_dt + date.timedelta(weeks=self.weeks, days=self.days):
                self.last_break = str(start_date_dt + date.timedelta(weeks=self.weeks, days=self.days))
                self.break_count = 1
                self.current_streak = 0
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                self.last_check = str(start_date_dt + date.timedelta(weeks=self.weeks, days=self.days))
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = (f"{start_date_dt + date.timedelta(weeks=self.weeks)} : "
                                            f"{start_date_dt + date.timedelta(days=13)}")
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            elif check_date_dt >= start_date_dt:
                self.last_check = self.start_date
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = f"{start_date_dt} : {start_date_dt + date.timedelta(days=6)}"
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            else:
                print("\nCheck-off date can't be earlier than the start date!\n")
                return ConnectionError
        else:
            last_check_dt = date.date.fromisoformat(self.last_check)
            if check_date_dt >= last_check_dt + date.timedelta(weeks=self.weeks * 4, days=self.days * 4):
                self.last_break = str(last_check_dt + date.timedelta(weeks=self.weeks * 4, days=self.days * 4))
                self.status = "Broken"
                self.break_count = 3
                self.current_streak = 0
                self.end_date = str(last_check_dt + date.timedelta(weeks=self.weeks * 4, days=self.days * 4))
                self.last_check_day = check_date
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                DB.update_habit(db, self.name, self.streak, self.last_check, self.status, check_date,
                                self.last_check_week, self.last_check_day)
                self.last_check = str(last_check_dt + date.timedelta(weeks=self.weeks * 4, days=self.days * 4))
            elif check_date_dt >= last_check_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3):
                self.last_break = str(last_check_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3))
                self.break_count += 2
                self.current_streak = 0
                self.break_count_check()
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                self.last_check = str(last_check_dt + date.timedelta(weeks=self.weeks * 3, days=self.days * 3))
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = (f"{last_check_dt + date.timedelta(weeks=self.weeks * 3)} : "
                                            f"{last_check_dt + date.timedelta(days=27)}")
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            elif check_date_dt >= last_check_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2):
                self.last_break = str(last_check_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2))
                self.break_count += 1
                self.current_streak = 0
                self.break_count_check()
                DB.update_streak(db, self.name, self.current_streak, self.longest_streak, self.break_count,
                                 self.last_break)
                self.last_check = str(last_check_dt + date.timedelta(weeks=self.weeks * 2, days=self.days * 2))
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = (f"{last_check_dt + date.timedelta(weeks=self.weeks * 2)} : "
                                            f"{last_check_dt + date.timedelta(days=20)}")
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            elif check_date_dt >= last_check_dt + date.timedelta(weeks=self.weeks, days=self.days):
                self.last_check = str(last_check_dt + date.timedelta(weeks=self.weeks, days=self.days))
                if self.weeks == 1:
                    # For habits with "Weekly" periodicity type, the program inserts the last checked week.
                    self.last_check_week = (f"{last_check_dt + date.timedelta(weeks=self.weeks)} : "
                                            f"{last_check_dt + date.timedelta(days=13)}")
                    self.last_check_day = check_date
                if self.days == 1:
                    # For habits with "Daily" periodicity type, the program inserts the last checked day's date.
                    self.last_check_day = check_date
            else:
                print("\nWrong check-off date!\n"
                      "Either the date you entered is earlier than your last check-off day,\n"
                      "Or you have already checked-off the habit during the period!\n")
                return ConnectionError

    def drop(self, db):
        """
        Deletes certain habit data from the database.

        :param db: The database, to which you are connected.
        :type db: class
        :return: None
        """
        DB.delete_habit(db, self.name)
