from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Number


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
