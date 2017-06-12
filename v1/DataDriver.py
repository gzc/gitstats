from datetime import datetime
import time
from Commit import Commit;
import Constant;
import collections

def generateHTML(commits, projectName, totalAuthors):
    totalLines, totalLinesAdded, totalLinesDeleted = generateLinesByDate(commits, projectName)
    totalFiles = generateFilesByDate(commits, projectName)
    generateIndexHtml(projectName, totalLines, totalLinesAdded, totalLinesDeleted,
        totalFiles, len(commits), totalAuthors)

def generateIndexHtml(projectName, totalLines, totalLinesAdded, totalLinesDeleted,
    totalFiles, totalCommits, totalAuthors):
    with open(Constant.INDEX_HTML_TEMPLATE, "rt") as fin:
        with open(Constant.INDEX_HTML, "wt") as fout:
            for line in fin:
                if '$title' in line:
                    fout.write(line.replace('$title', projectName))
                elif '$time' in line:
                    fout.write(line.replace('$time', time.strftime('%l:%M%p %Z on %b %d, %Y')))
                elif '$files' in line:
                    fout.write(line.replace('$files', str(totalFiles)))
                elif '$commits' in line:
                    fout.write(line.replace('$commits', str(totalCommits)))
                elif '$totallines' in line:
                    fout.write(line.replace('$totallines', str(totalLines)))
                elif '$linesadded' in line:
                    fout.write(line.replace('$linesadded', str(totalLinesAdded)))
                elif '$linesdeleted' in line:
                    fout.write(line.replace('$linesdeleted', str(totalLinesDeleted)))
                elif '$author' in line:
                    fout.write(line.replace('$author', str(totalAuthors)))
                else:
                    fout.write(line)

def generateLinesByDate(commits, projectName):
    totalLines = 0
    totalLinesAdded = 0
    totalLinesDeleted = 0;
    mydic = collections.OrderedDict()
    for commit in reversed(commits):
        dateKey = int(commit.date.strftime("%s")) * 1000
        totalLinesAdded = totalLinesAdded + commit.linesAdded
        totalLinesDeleted = totalLinesDeleted + commit.linesDeleted
        linesDiff = commit.linesAdded - commit.linesDeleted;
        totalLines = totalLines + linesDiff
        if dateKey in mydic:
            mydic[dateKey] = mydic[dateKey] + linesDiff
        else:
            mydic[dateKey] = totalLines + linesDiff
    data = []
    for item in mydic.items():
        data.append([item[0], item[1]])
    with open(Constant.LINES_BY_DATE_TEMPLATE, "rt") as fin:
        with open(Constant.LINES_BY_DATE, "wt") as fout:
            for line in fin:
                if '$data' in line:
                    fout.write(line.replace('$data', str(data)))
                elif '$title' in line:
                    fout.write(line.replace('$title', projectName))
                else:
                    fout.write(line)
    return totalLines, totalLinesAdded, totalLinesDeleted

def generateFilesByDate(commits, projectName):
    totalFiles = 0
    mydic = collections.OrderedDict()
    for commit in reversed(commits):
        dateKey = int(commit.date.strftime("%s")) * 1000
        filesDiff = commit.filesAdded - commit.filesDeleted;
        totalFiles = totalFiles + filesDiff
        if dateKey in mydic:
            mydic[dateKey] = mydic[dateKey] + filesDiff
        else:
            mydic[dateKey] = totalFiles + filesDiff
    data = []
    for item in mydic.items():
        data.append([item[0], item[1]])
    with open(Constant.FILES_BY_DATE_TEMPLATE, "rt") as fin:
        with open(Constant.FILES_BY_DATE, "wt") as fout:
            for line in fin:
                if '$data' in line:
                    fout.write(line.replace('$data', str(data)))
                elif '$title' in line:
                    fout.write(line.replace('$title', projectName))
                else:
                    fout.write(line)
    return totalFiles
