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

    filesAdded = 0
    filesDeleted = 0

    myfile = open(logname)
    lines = myfile.readlines()

    # store file extention information
    fileExtentionMap = {}

    while count < len(lines):
        line = lines[count]
        count = count + 1
        if state == 0:
            # Parsing commit hash
            assert len(line) == 48 and line.startswith('commit'), "When parsing commit hash, the state should be 0"
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
            line = line.strip()
            if len(line) == 0:
                # end
                currentCommit = Commit(commitHash, commitAuthor, commitAuthorEmail, commitDate, commitMessage)
                currentCommit.linesAdded = commitLinesAdded
                currentCommit.linesDeleted = commitLinesDeleted
                currentCommit.filesAdded = filesAdded
                currentCommit.filesDeleted = filesDeleted
                commits.append(currentCommit)
                # clear state
                state = 0
                filesAdded = 0
                filesDeleted = 0
            else:
                if line.startswith('create'):
                    dotIdx = line.rfind('.');
                    ext = line[dotIdx+1:]
                    if ext not in fileExtentionMap.keys():
                        fileExtentionMap[ext] = 0
                    fileExtentionMap[ext] += 1
                    filesAdded = filesAdded + 1
                elif line.startswith('delete'):
                    dotIdx = line.rfind('.');
                    ext = line[dotIdx+1:]
                    if ext not in fileExtentionMap.keys():
                        fileExtentionMap[ext] = 0
                    fileExtentionMap[ext] -= 1
                    filesDeleted = filesDeleted + 1
                else:
                    # TODO : this is rename file
                    # 1  rename webpack.config.js => webpack.config.local.js (71%)
                    # 2. rename client/{ => a/b}/Sports/CurrentGame.tsx (65%)
	                # 3. rename client/reducers/{reservation => }/selected.js (67%)
                    # 4. rename test/{utils => testUtils}/Helpers.ts (100%)
                    # 5. rename client/actions/{scheduler.js => scheduler.ts} (51%)
                    braceL = line.find('{')
                    braceR = line.find('}')
                    if braceL < 0:
                        # case 1
                        Util.handleRenameFile(line, fileExtentionMap)
                    else:
                        arrowIdx = line.find('=>')
                        fileL = line[braceL+1:arrowIdx-1]
                        fileR = line[arrowIdx+3:braceR]
                        if fileL < 2 or fileR < 2:
                            # case 2 & 3
                            continue
                        if line[braceR+1] == '/':
                            # case 4
                            continue
                        Util.handleRenameFile(line[braceL+1:braceR], fileExtentionMap)

    myfile.close()
    return commits, fileExtentionMap
