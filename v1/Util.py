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
