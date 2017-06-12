#coding:utf-8
#!/usr/bin/python

import sys
from datetime import datetime

# other dependency
import pandas as pd
from yattag import Doc

# own dependency
from Commit import Commit
import Constant
import DataCollector
import DataDriver
import Util

def main():
    logname = sys.argv[1]
    projectName = 'BBG'
    fields = ['author', 'commit_number', 'lines_added', 'lines_deleted']
    commits = DataCollector.fire(logname)

    r1 = map(lambda commit : (commit.author, 1, commit.linesAdded, commit.linesDeleted), commits)
    df = pd.DataFrame(data=r1, columns=fields) \
        .groupby('author') \
        .sum() \
        .sort_values(by=['commit_number', 'lines_added'], ascending=[False, False])
    commitData = zip(df.index, *df.values.T) # df is the result above

    # Generate html content
    # doc, tag, text = Doc().tagtext()
    # with tag('table', ('border', '1px solid black')):
    #     with tag('tr'):
    #         for i in range(4):
    #             with tag('th'):
    #                 text(fields[i])
    #     for commitdata in commitData:
    #         with tag('tr'):
    #             for i in range(4):
    #                 with tag('td', ('align', 'center')):
    #                     text(commitdata[i])
    # with tag('img', ('src', Constant.LINES_CHANGE_PIC_NAME)):
    #     pass

    # Generate html from template html and insert data
    DataDriver.generateHTML(commits, projectName, len(commitData))

if __name__ == "__main__":
    main()
    print 'Please open web/index.html to view your statistics.'
