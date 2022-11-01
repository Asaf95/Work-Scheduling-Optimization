"""
smart sender module

this module will send tasks to the model.
what this module will do:
1. implement the priority attribute by given then larger wighted.
2. verify the limitation of none working days.
3. generate weighted score for each job considering the resources it will take and the profit.
4. convert from open_shop to job_shop
"""
import logging

import pandas as pd

import jobshop_solver as jss


def get_logger():
    logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                        format="%(asctime)s -%(levelname)s - %(message)s -")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logs.test')
    formatter = logging.Formatter('%(asctime)s - line: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def send_jobs():
    # Getting the data from the database
    all_jobs_df = pd.read_csv('database/combine_data_from_user/all_jobs.csv')

    # If you want first to take task with high priority this how you can filter it
    # Pzero_jobs = all_jobs_df[all_jobs_df['Priority'] == 0]

    # At this point we will use only the machines time to process in each machine and optimize the due date
    times_of_jobs = all_jobs_df[["Time-m1", "Time-m2", "Time-m3"]]

    # Transform the data structure to structure that the CP-CAT model can optimize

    times_of_jobs = times_of_jobs.values.tolist()
    main_li = []
    for i in times_of_jobs:
        lst1 = [1, 2, 3]
        lst_tuple = list(zip(lst1, i))
        main_li.append(lst_tuple)

    # Transforming the user
    string_results, list_results = jss.main(main_li)
    transform_to_lists = make_outputs(string_results, list_results)
    return transform_to_lists


def make_outputs(string_results, list_results):
    from datetime import timedelta, date

    transform_to_lists = []
    for machine in list_results:
        machine_name = "Machine - " + str(machine)
        current_machine = list_results[machine]
        for item in current_machine:
            name_of_task = "Job_" + str(item.job)
            StartDate = date.today() + timedelta(days=item.start)
            EndDate = StartDate + timedelta(days=item.duration)

            task = dict(Task=machine_name, Start=StartDate, Finish=EndDate, Resource=name_of_task)
            transform_to_lists.append(task)
    return transform_to_lists

# df = [dict(Task="Job AB", Start='2009-01-01', Finish='2009-01-28'),
#       dict(Task="Job B", Start='2009-01-05', Finish='2009-02-15'),
#       dict(Task="Job C", Start='2009-01-20', Finish='2009-02-28')]
#
# print(df)
# transform_to_lists = send_jobs()
# print(transform_to_lists)
