#coding:utf-8
#!/usr/bin/python

import sys
from datetime import datetime

# other dependency
import pandas as pd

# own dependency
from Commit import Commit
import Constant
import DataCollector
import DataDriver
import MotivationDataDriver
import Util

def main():
    projectName = sys.argv[1]
    logname = sys.argv[2]
    fields = ['author', 'commit_number', 'lines_added', 'lines_deleted']
    commits, fileExtensionMap = DataCollector.fire(logname)

    r1 = map(lambda commit : (commit.author, 1, commit.linesAdded, commit.linesDeleted), commits)
    df = pd.DataFrame(data=r1, columns=fields) \
        .groupby('author') \
        .sum() \
        .sort_values(by=['commit_number', 'lines_added'], ascending=[False, False])
    commitData = zip(df.index, *df.values.T) # df is the result above

    # Generate html from template html and insert data
    DataDriver.generateHTML(commits, projectName, commitData, fileExtensionMap)

    # Motivation data
    MotivationDataDriver.generateHTML(projectName, commits)

if __name__ == "__main__":
    main()
    print 'Please open web/index.html to view your statistics.'
