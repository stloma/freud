from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Text

with open('logger.txt', 'a') as fout:
    fout.write(str(Text.Text))


class FreudStyle(Style):
    default_style = ""
    styles = {
        Comment:                '#776977',
        # Bool
        Keyword:                '#fff',
        Name:                   '#516aec',
        Name.Tag:               '#516aec',
        # JSON Value
        String:                 'noinherit',
        Number:                 '#ca402b'
    }
