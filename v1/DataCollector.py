from datetime import datetime

from Commit import Commit
import Util

"""
The state change when parsing one commit
0 : initial state
1 : finish parsing commit hash
2 : finish parsing author
3 : finish parsing commit date
4-6 : parsing commit message
7 : finish parsing summary
8 : finish parsing per file change

commit 7e28c4657d6545d2a35e6d45ede1f510686d52e5  (1)
Author: Roopansh Bansal <roopansh@iitg.ac.in>  (2)
Date:   Thu Apr 27 00:16:12 2017 +0530   (3)

    intial answers to 25.3 added   (4)

 C25-All-Pairs-Shortest-Paths/25.3.md            |  63 ++++++++++++++++++++++++
 C25-All-Pairs-Shortest-Paths/repo/s3/25_3_6.gif | Bin 0 -> 46977 bytes  (5)
 2 files changed, 63 insertions(+)
 create mode 100644 C25-All-Pairs-Shortest-Paths/25.3.md
 create mode 100644 C25-All-Pairs-Shortest-Paths/repo/s3/25_3_6.gif  (0)
"""

def fire(logname):
    totalCommit = 0
    commits = []
    state = 0
    count = 0

    """
    each field
    """
    commitHash = ""
    commitAuthor = ""
    commitAuthorEmail = ""
    commitMessage = ""
    commitDate = None
    commitLinesAdded = 0
    commitLinesDeleted = 0

    myfile = open(logname)
    lines = myfile.readlines()

    while count < len(lines):
        line = lines[count]
        count = count + 1
        if state == 0:
            # Parsing commit hash
            assert len(line) == 48 and line.startswith('commit'), "When parsing commit hash, the state should be 0"
            totalCommit = totalCommit + 1
            commitHash = line[7:-2]
            state = 1
        elif state == 1:
            # Parsing author and email
            assert line.startswith('Author'), "When parsing Author, the state should be 1"
            emailidx = line.rfind('<')
            commitAuthorEmail = line[emailidx+1:-2]
            commitAuthor = line[8:emailidx-1]
            state = 2
        elif state == 2:
            # Parsing date, we do not care timeZone
            assert line.startswith('Date'), "When parsing Date, the state should be 2"
            commitDate = datetime.strptime(line[8:-7], '%a %b %d %H:%M:%S %Y')
            state = 3
        elif state == 3:
            nextLine = lines[count]
            if nextLine[0] == ' ' and nextLine[1] != ' ':
                state = 6
        elif state == 6:
            if line.find('|') > -1:
                continue
            else:
                # Parsing summary
                commitLinesAdded, commitLinesDeleted = Util.ParseSummaryInCommit(line)
                state = 7
        elif state == 7:
            if len(line.strip()) == 0:
                # end
                currentCommit = Commit(commitHash, commitAuthor, commitAuthorEmail, commitDate, commitMessage)
                currentCommit.linesAdded = commitLinesAdded
                currentCommit.linesDeleted = commitLinesDeleted
                commits.append(currentCommit)
                state = 0
            else:
                # TODO: collect create/delete mode data
                continue

    myfile.close()
    return commits
