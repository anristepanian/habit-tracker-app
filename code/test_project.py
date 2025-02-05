from habit_track import DbHabit
from db import DB
from analyse import Analysis
import os

# remove_db is needed to remove the previously created test.db, in case the teardown_method wasn't called itself.
remove_db = False

if remove_db:
    # if the remove_db is True, os will remove the "test.db".
    os.remove("test.db")
else:
    class TestHabit:
        """The TestHabit class is used to test the program.

        The Methods:
            setup_method(): Creates the "test.db", inserts data about habit to the "test.db" directly without calling
            the DbHabit class.
            test_habit(): Creates a habit through DbHabit class, inserts and analysis data.
            teardown_method(): Closes and removes the "test.db".
        """
        def setup_method(self):
            """
            Creates the "test.db", inserts data about habit to the "test.db" directly without calling the DbHabit class.

            :return: None
            """
            self.db_title = "test.db"
            self.db = DB.get_db(name=self.db_title)

            DB.add_habit(self.db, "test_habit", "test_description", "2025-01-20", "2025-01-30", "Daily")
            DB.habit_check(self.db, "test_habit", True, "2025-01-20")

        def test_habit(self):
            """
            Creates a habit through DbHabit class, inserts and analysis data.

            :return: None
            """
            habit = DbHabit("test_habit_1", "test_description_1", "2025-01-20", "2025-02-02", "Daily")
            habit.store(db=self.db)
            # The first break is on "2025-01-20" because the user is supposed to check-off the habit on the start date.
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-21")  # streak = 1
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-22")  # streak = 2
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-23")  # streak = 3
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-24")  # streak = 4
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-25")  # streak = 5
            # The second break is here! There are no more breaks left!
            longest_streak = Analysis.given_habits_longest_streak(self.db, "test_habit_1")[0][2]
            assert longest_streak == 5
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-27")  # streak = 1
            # The longest streak equals 5, while the current streak now equals 1!
            current_streak = DB.get_cur_streak(self.db, "test_habit_1")
            assert current_streak == 1
            longest_streak = Analysis.given_habits_longest_streak(self.db, "test_habit_1")[0][2]
            assert longest_streak == 5
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-28")  # streak = 2
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-29")  # streak = 3
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-30")  # streak = 4
            habit.add_habit_check(db=self.db, check=True, check_date="2025-01-31")  # streak = 5
            habit.add_habit_check(db=self.db, check=True, check_date="2025-02-01")  # streak = 6
            habit.add_habit_check(db=self.db, check=True, check_date="2025-02-02")  # streak = 7

            longest_streak = Analysis.given_habits_longest_streak(self.db, "test_habit_1")[0][2]
            assert longest_streak == 7  # Now the longest streak is 7.
            current_streak = DB.get_cur_streak(self.db, "test_habit_1", "Completed")
            assert current_streak == 7  # Despite the habit is completed, the current streak changed on the last day.

            status = habit.status
            # The habit is completed now since it has passed the expiration date and hasn't broken the habit 3 times.
            assert status == "Completed"

            count = DB.get_habit_data(self.db)  # There are 2 habits in the Habit table.
            assert len(count) == 2
            habit.drop(self.db)  # Delete a habit.
            count = DB.get_habit_data(self.db)  # There are now just 1 habit in the Habit table.
            print(count)
            assert len(count) == 1

        def teardown_method(self):
            """
            Closes and removes the "test.db".

            :return: None
            """
            DB.db_close(self.db)
            os.remove(self.db_title)
