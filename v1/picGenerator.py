from datetime import datetime
from Commit import Commit;
import Constant;
import collections

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generateLinesOfCode(commits):
    totalLines = 0
    mydic = collections.OrderedDict()
    for commit in reversed(commits):
        dateKey = mdates.date2num(datetime(commit.date.year, commit.date.month, commit.date.day))
        linesDiff = commit.linesAdded - commit.linesDeleted;
        totalLines = totalLines + linesDiff
        if dateKey in mydic:
            mydic[dateKey] = mydic[dateKey] + linesDiff
        else:
            mydic[dateKey] = totalLines + linesDiff

    plt.plot_date(mydic.keys(), mydic.values(), '-')
    plt.ylabel('Lines of code')
    plt.title('Lines of code about your repo')
    plt.gcf().autofmt_xdate()
    plt.savefig(Constant.LINES_CHANGE_PIC_NAME)
