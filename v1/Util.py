# Parsing a line like:
# 51 files changed, 3927 insertions(+), 3398 deletions(-)
# return (added lines, deleted lines)
def ParseSummaryInCommit(line):
    data = line.split(',')
    added = 0
    deleted = 0
    for item in data:
        item = item.strip()
        v = int(item[:item.find(' ')]);
        if item.find('+') > -1:
            added = v
        elif item.find('-') > -1:
            deleted = v
    return added, deleted

# webpack.config.js => webpack.config.local.js (71%)
def handleRenameFile(line, myDict):
    idx = line.find('=>')
    dotL = line.rfind('.', 0, idx)
    dotR = line.rfind('.', idx)
    extL = line[dotL+1:idx-1]
    extR = cleanExt(line[dotR+1:])
    if extL == extR:
        return
    if extL not in myDict.keys():
        myDict[extL] = 0
    if extR not in myDict.keys():
        myDict[extR] = 0
    myDict[extL] -= 1
    myDict[extR] += 1

# js (71%) => js
def cleanExt(ext):
    idx = ext.find(' ')
    if idx > 0:
        return ext[:ext.find(' ')]
    return ext
