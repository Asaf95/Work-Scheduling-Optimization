from datetime import date
from datetime import datetime
import pandas as pd
from workalendar.asia import Israel
import logging
"""a

this script will deal with all the dates converting and for now also stores Israel calendar.  
The day's class will be store with all other objects in Job
Convert date to number

2012-06-13 --> 20120613 = 10,000 * (2012) + 100 * (6) + 1*(13)
this class will convert all what is needed for the SW

"""

"""
Israel calendar will be used to know if it's possible  to schedule the job at this date 


"""
cal = Israel()
logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                    format= "%(asctime)s -%(levelname)s - %(message)s")


def get_logger():
    logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                        format="%(asctime)s -%(levelname)s - %(message)s -")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logs.test')
    formatter = logging.Formatter('%(asctime)s - line: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def to_integer_from_date(dt_time: object) -> object:
    """

    :param dt_time:
    :return:
    """
    try:
        return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day
    except Exception as e:
        print(f'problem was find in using the function to_integer(): {e}')


def to_date_from_int(df_int) -> object:
    """

    :rtype: object
    """
    try:
        x = pd.to_datetime(df_int, format='%Y%m%d').date()

        return x
    except Exception as e:
        print(f'problem was find in using the function to_date_from_int(): {e}')


def get_current_time():
    x = datetime.now()
    return x


import datetime


def from_string_to_int(data_string):

    y = datetime.datetime.strptime(data_string, "%d/%m/%Y")
    y = to_integer_from_date(y)
    return y


#
#
# to_integer_from_date(datetime.date(2012, 6, 13))
#
# y = datetime.datetime.strptime("21/12/2008", "%d/%m/%Y")
#
# y = to_integer_from_date(y)
#
# y1 = to_date_from_int(y)
