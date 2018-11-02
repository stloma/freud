from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

from freud import STYLE

theme = STYLE['theme']
line_fg = STYLE.get('separator_line_fg', '')
line_bg = STYLE.get('separator_line_bg', '')


custom_style = [
    ('line', 'bg:{} fg:{}'.format(line_bg, line_fg)),
    ('button.selected', 'bg:#cccccc fg:#880000'),
]

style = style_from_pygments_cls(get_style_by_name(theme))

style._style_rules.extend(custom_style)
