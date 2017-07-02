from datetime import datetime
import time
from Commit import Commit;
import Constant;

# other dependency
import pandas as pd
from yattag import Doc

def generateHTML(commits):
    fields = ['author', 'commit_number', 'date']
    r = map(lambda commit : (commit.author, 1, str(commit.date.year) + '-' + paddingMonth(commit.date.month)), commits)
    df = pd.DataFrame(data=r, columns=fields) \
        .groupby(['date', 'author']) \
        .sum() \
        .sort_values(by='commit_number', ascending=False)
    commitData = zip(df.index, *df.values.T) # df is the result above

    mydict = {}
    for ele in commitData:
        commitDate = ele[0][0]
        author = ele[0][1]
        number = ele[1]
        if commitDate not in mydict:
            mydict[commitDate] = ''
        mydict[commitDate] += (author + '(' + str(number) + '); ');

    doc, tag, text = Doc().tagtext()
    with tag('table', ('class', 'table table-bordered table-condensed table-hover')):
        with tag('tr'):
            with tag('th', ('align', 'center')):
                text('Date (year-month)')
            with tag('th', ('align', 'center')):
                text('Hero (commit number)')
        for key, value in sorted(mydict.iteritems()):
            with tag('tr'):
                with tag('td', ('align', 'center')):
                    text(key)
                with tag('td'):
                    text(value)
    with open(Constant.RANK_TEMPLATE, "rt") as fin:
        with open(Constant.RANK, "wt") as fout:
            for line in fin:
                if '$data' in line:
                    fout.write(line.replace('$data', doc.getvalue()))
                else:
                    fout.write(line)

def paddingMonth(month):
    if month < 10:
        return '0' + str(month)
    return str(month)
