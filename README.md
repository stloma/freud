![Freud terminal gif](https://f002.backblazeb2.com/file/x7udzfe/freud_demo.gif)

Freud is a TUI API endpoint analyzer utilizing Python Prompt Toolkit and
Requests.  It allows creating and saving request headers, authentication (basic
and digest), and body using both integrated forms and your native
editor.

Currently, it is designed and tested for receiving JSON, XML, and HTML
responses, but more can be added later as needed.

## Installation

> First, create an environment (_recommended_):

```shell
python -m venv .venv
. .venv/bin/activate
```

> Then you can either install through PyPI...

```shell
pip install freud
```

> or from sources

```
git clone https://github.com/stloma/freud
python setup.py install
```

## Keys

> Key shortcuts depend on which window you are in. There are 4 windows: server
> list (left window), response headers (top right), response body (middle
> right), and server summary (bottom).

* Server list/left window
    - New server: `n`
    - Select server: `enter`
    - Edit selected server: `e`
    - Edit authentication: `a`
    - Edit body: `b`
    - Send request for selected server: `r`
    - Delete selected server: `d`
    - Sort servers: `s`
    - Top/bottom of server list: `gg/G`

* Header window, Response body window, Server summary window
    - `h/j/k/l` Vi keybindings for movement
    - `/` Search text
    - `o`: Open response body in external editor

* General Navigation
    - Quit: `Ctrl+c`
    - Key Binding Quick Reference: `Ctrl+f`
    - Next window: `Tab`
    - Previous window: `Shift+Tab`


## Advanced uses

#### More keys
* Copy/Paste: `Shift+Click`

#### Changing default configuration

* Settings file: `config/freud.ini`

## Roadmap

Freud is still in development, but should work well for most use
cases.

Currently, it is designed to handle JSON, XML, and HTML responses; I
haven't tested others. If you would like it to handle something specific, you
can either submit a PR or create an issue and I'll add it!

#### Goals

* Add more authentication types (e.g., OAuth, Bearer Token, etc.)
* Handle more Content-Types (MIME types)
* Cookie handling
* Add capability to organize requests under categories
* Increase testing coverage

## Requirements

* Python: 3.5+
* Python Prompt Toolkit, Requests, Pygments
* set \$EDITOR environment variable
    - bash/zsh: `export EDITOR=$(which vim)`

## Testing

```
python setup.py test
pytest
```
