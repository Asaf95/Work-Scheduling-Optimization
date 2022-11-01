import logging
from os import listdir

import pandas

import time_converter as tc

"""
Thia file convert the data from the user Input to objects that the Algorithm can use to solve the problem
It will get data from the app.py:
DF - is all the Jobs that the user want to do in the following year with the following columns
Job ID - what Jobs he want to do
Start Date - the release date of the missions what is the first date that the machines can work on those jobs.
End Date - (Deadline) the last date that the machines can complete the Job

This class use OrTools and Scheduling_Classes.py classes to add more known properties of Job objects

after creating all the right objects with there properties this class will move the objects to the Algorithm class.
"""


def get_logger():
    logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                        format="%(asctime)s -%(levelname)s - %(message)s -")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logs.test')
    formatter = logging.Formatter('%(asctime)s - line: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def convert_user_jobs_csv(df: pandas.DataFrame, filename) -> None:
    """
    this function convert the user input to csv file in the db
    the name of the file in the db will be as the name of the file
    that the the user insert.
    IMPOTENT TO NOT USE NEW FILE NAMES WITH OUT CHANGING THE FUNCTION WHO READ FROM THE DB!!!!

    :param df:  the user input
    :param filename:  the name of the file that the user had insert
    :return: NONE
    """
    logger = get_logger()
    logger.info(f"function convert_user_jobs_csv() is in use with the file name {filename}")
    df.to_csv(f'database/csv_from_user/{filename}', index=False, header=True, encoding='utf-8-sig')
    check_if_can_start_level2_files()


def convert_user_values(input1, input2, input3, input4):
    """
    convert the user input (the values) to a csv file that the model will be able to use.
    :param input1:
    :param input2:
    :param input3:
    :param input4:
    :return:
    """
    import csv
    logging.info(f"""the function convert_user_values() got the following variables{input1, input2, input3, input4}
                """)

    with open('database/testi2.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['resource_id', 'resource_name', 'resource_quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'resource_id': 'r_id_1', 'resource_name': 'Worker_1', 'resource_quantity': input1})
        writer.writerow({'resource_id': 'r_id_2', 'resource_name': 'Worker_2', 'resource_quantity': input2})
        writer.writerow({'resource_id': 'r_id_3', 'resource_name': 'Worker_3', 'resource_quantity': input3})
        writer.writerow({'resource_id': 'r_id_4', 'resource_name': 'Worker_4', 'resource_quantity': input4})
        file.close()
    check_if_can_start_level2_files()


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def check_if_can_start_level2_files():
    import pandas as pd
    logger = get_logger()
    logger.info("function check_if_can_start_level2_files() is in use ")
    filenames = find_csv_filenames("database/csv_from_user")
    files_from_user = []
    for name in filenames:
        files_from_user.append(name)
    logger.info(f'There are {len(files_from_user)}/4 files in the folder')
    if len(files_from_user) == 4:
        logger.info("all user files are in place and we are ready to start solving the problem")
        filenames = find_csv_filenames("database/csv_from_user")
        logger.info(f'the files in the folder are {filenames}')
        for name in filenames:
            if "Job_Pro" in name:
                df_Job_Pro = pd.read_csv("database/csv_from_user/" + name)
            if "Input_Job" in name:
                df_Input_Job = pd.read_csv("database/csv_from_user/" + name)
            if "Machine_Pro" in name:
                df_Machine_Pro = pd.read_csv("database/csv_from_user/" + name)
            if "Input_Machine" in name:
                df_Input_Machine = pd.read_csv("database/csv_from_user/" + name)
        start_level2_files(df_Job_Pro, df_Input_Job, df_Machine_Pro, df_Input_Machine)
    else:
        number_of_files = len(files_from_user)
        logger.info(f'not all files was added.. there is only {number_of_files}')


def start_level2_files(df_Job_Pro, df_Input_Job, df_Machine_Pro, df_Input_Machine):
    logger = get_logger()
    logger.info("Start of start_level2_files")
    all_jobs = df_Job_Pro.merge(df_Input_Job, on='Job_Id', how='right')
    print(all_jobs)
    logger.info(f'the all_jobs file is {all_jobs}')
    all_jobs['startTime-i'] = all_jobs.apply(lambda x: tc.from_string_to_int(x['startTime']), axis=1)
    all_jobs['endTime-i'] = all_jobs.apply(lambda x: tc.from_string_to_int(x['endTime']), axis=1)

    #   @TODO:  understand why this dose not work
    # all_jobs['ReleaseTime-i'] = all_jobs.apply(lambda x: time_converter.from_string_to_int(x['ReleaseTime']), axis=1)
    logger.info(f'the file all_jobs is \n {all_jobs}')
    print(all_jobs)

    all_machines = df_Machine_Pro.merge(df_Input_Machine, on='resource_id', how='inner')
    all_jobs.to_csv(f'database/combine_data_from_user/all_jobs.csv',
                    index=False, header=True, encoding='utf-8-sig')
    all_machines.to_csv(f'database/combine_data_from_user/all_machines.csv',
                        index=False, header=True, encoding='utf-8-sig')
    logger.info('User Data was processed into the database')
