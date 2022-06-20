import plotly.figure_factory as ff
import logging
import smart_sender

"""
From this file the User Output tab is reading the data
the df is all the final results of the scheduling that we had
"""

# df = [dict(Task="Job AB", Start='2009-01-01', Finish='2009-01-28'),
#       dict(Task="Job B", Start='2009-01-05', Finish='2009-02-15'),
#       dict(Task="Job C", Start='2009-01-20', Finish='2009-02-28')]
# fig.layout.xaxis.tickvals = pd.date_range('2009-01-01', '2009-03-01', freq='d')
# fig.layout.xaxis.ticktext = list(range(len(fig.layout.xaxis.tickvals)))

"""Simple function to display a jobshop solution using plotly."""

# transform_to_lists = smart_sender.send_jobs()
#
# print(f'transform_to_lists is {transform_to_lists}')
# print(transform_to_lists)
# # fig2 = ff.create_gantt(transform_to_lists, index_col='Resource', show_colorbar=True,
# #                        group_tasks=True)
# fig2 = ff.create_gantt(transform_to_lists,group_tasks=True, show_colorbar=True)


def get_logger():
    logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                        format="%(asctime)s -%(levelname)s - %(message)s -")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logs.test')
    formatter = logging.Formatter('%(asctime)s - line: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_gantt():
      transform_to_lists = smart_sender.send_jobs()

      print(f'transform_to_lists is {transform_to_lists}')
      print(transform_to_lists)
      try:
          fig2 = ff.create_gantt(transform_to_lists, index_col='Resource', show_colorbar=True,
                              group_tasks=True)
      except:
          fig2 = ff.create_gantt(transform_to_lists, show_colorbar=False,
                              group_tasks=True)
      return fig2


def get_fronts():
      external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

      colors = {
            'background': '#f1f7fd',
            'text': '#061932'
      }

      basic_style = {
            'width': '100%',
            'height': '100%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
      }

      basic_style2 = {
            'width': '100%',
            'height': '100%',
            'lineHeight': '60px',
            'textAlign': 'center',
            'margin': '10px'
      }
      return external_stylesheets, colors, basic_style, basic_style2