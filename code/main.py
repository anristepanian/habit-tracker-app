import questionary
from db import DB
from habit_track import DbHabit
from analyse import Analysis
import datetime


def cli():
    """
    The Command-Line Interface.

    :return: None
    """
    # The "main.py" database, to which you are connecting.
    db = DB.get_db()
    # Asks the user whether is he ready?
    questionary.confirm("Are you ready?").ask()

    # Boolean variable is needed to stop the program loop if user chooses "Exit".
    stop = False
    # The program loop.
    while not stop:
        # The user is given a choice of actions.
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Check-off", "Delete", "Analyse", "Exit"]
        ).ask()

        if choice == "Create":
            # If the user chooses "Create", he should insert all the necessary data needed to create a habit.
            name = questionary.text("What's the name of a habit?").ask()
            desc = questionary.text("What's the description of the habit?").ask()
            print("Important: Please enter the date in format YYYY-MM-DD")
            start = questionary.text("What's the starting date of the habit?\nKeep in mind that if you don't"
                                     "choose a start date,\nThe start date will be the present day!").ask()
            try:
                if start:
                    datetime.date.fromisoformat(start)
            except ValueError:
                print("You have written the start date wrong! Please try again!")
                continue
            print("Important: Please enter the date in format YYYY-MM-DD")
            till = questionary.text("Until what date will this habit be valid?").ask()
            try:
                datetime.date.fromisoformat(till)
            except ValueError:
                print("You have written the expiration date wrong! Please try again!")
                continue
            if start:
                if datetime.date.fromisoformat(till) < datetime.date.fromisoformat(start):
                    print("The expiration date can't be before the start date!")
                    continue
            else:
                if datetime.date.fromisoformat(till) < datetime.date.today():
                    print("The expiration date can't be before the start date!")
                    continue
            period = questionary.select("What is the periodicity of the habit?", choices=["Daily", "Weekly"]).ask()
            # The program calls DbHabit class to store the habit's data into the "main.db" database.
            habit = DbHabit(name, desc, start, till, period)
            habit.store(db)
        if choice == "Check-off":
            # If the user chooses "Check-off", he should insert all the necessary data needed to check-off a habit.
            name = questionary.text("What's the name of a habit you want to check-off?").ask()
            habit_id = DB.name_to_id(db, name)
            if habit_id == "Error":
                continue
            check = questionary.confirm("Have you completed a habit in a given period?").ask()
            print("Important: Please enter the date in format YYYY-MM-DD")
            date: str = questionary.text("What is the date of check-off?\nKeep in mind, if you don't choose a check-off"
                                         "date,\nThe check-off date will be the present day!").ask()
            try:
                if date:
                    datetime.date.fromisoformat(date)
            except ValueError:
                print("You have written the start date wrong! Please try again!")
                continue
            # The program imports all the necessary data about a certain habit from "main.db" dataset.
            cur = db.cursor()
            cur.execute("""SELECT habit.name, habit.description, habit.start_date, habit.valid_till, habit.periodicity, 
            streak.current_streak, streak.longest_streak, streak.break_count, streak.last_break, habit.streak,
            habit.last_check, habit.last_check_week, habit.last_check_day
            FROM habit LEFT JOIN streak on habit.habit_id = streak.habit_id WHERE habit.habit_id = ? 
            AND habit.status = 'Still in progress'""", (habit_id,))
            select = cur.fetchall()[0]
            filtered_select = tuple(x for x in select if x is not None)
            # The program calls DbHabit class to check-off the habit.
            habit = DbHabit(*filtered_select)
            habit.add_habit_check(db, check, date)
        if choice == "Delete":
            # If the user chooses "Delete", he should insert the name of the habit he wants to delete.
            name = questionary.text("What is the name of a habit you want to delete?").ask()
            # The program calls the delete_habit method of DB class.
            DB.delete_habit(db, name)
        if choice == "Analyse":
            # If the user chooses "Analyse", he is given a choice of actions.
            analysis = questionary.select(
                "What do you want to do?",
                ["Return a list of all habits, in spite of their status",
                 "Return a list of all currently tracked habits",
                 "Return a list of all habits with the same periodicity",
                 "Return the longest run streak of all defined habits",
                 "Return the longest run streak for a given habit",
                 "Return all actions' history of a certain habit"]).ask()
            if analysis == "Return a list of all habits, in spite of their status":
                # The program prints the list of all habits, in spite of their status.
                Analysis.all_habits(db)
            if analysis == "Return a list of all currently tracked habits":
                # The program prints the list of all currently tracked habits.
                Analysis.currently_tracked_habits(db)
            if analysis == "Return a list of all habits with the same periodicity":
                # The program prints the list of all habits with the same periodicity.
                Analysis.same_periodicity_habits(db)
            if analysis == "Return the longest run streak of all defined habits":
                # The program prints the list of the longest run streak of all defined habits.
                Analysis.habits_longest_streak(db)
            if analysis == "Return the longest run streak for a given habit":
                # The program prints the longest run streak for a given habit.
                Analysis.given_habits_longest_streak(db)
            if analysis == "Return all actions' history of a certain habit":
                # The program prints all actions' history of a certain habit.
                name = questionary.text("What is the name of a habit you want track?").ask()
                Analysis.all_actions(db, name)
        if choice == "Exit":
            # If the user chooses "Exit", program closes the CLI.
            # The program prints "Bye!".
            print("Bye!")
            # The program changes the stop value to True, in order to stop the program loop.
            stop = True


# Executed when invoked directly.
if __name__ == "__main__":
    # Calls the cli() method.
    cli()
