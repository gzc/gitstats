"""
This class represents the info of one commit
"""

from Change import *;

class Commit:

    def __init__(self, hash, author, authorEmail, date, commitMessage):
        self.hash = hash;
        self.author = author;
        self.authorEmail = authorEmail
        self.date = date;
        self.commitMessage = commitMessage;
        
        self.changes = None;
        
        self.linesAdded = 0;
        self.linesDeleted = 0;

    def __str__(self):
        return ('commit hash {0}\ncommit author {1}\ncommit author email {2}\n'
        'commit date {3}\n{4} lines added, {5} lines deleted\n'). \
        format(self.hash, self.author, self.authorEmail, self.date,
        self.linesAdded, self.linesDeleted)