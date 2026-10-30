"""
Auto-pairing of brackets and quotes for Thonny editors and Shell.

- typing ( [ { " ' inserts the closing pair and puts the cursor between
- typing a closing char right before the same char just steps over it
- typing an opener or quote with a selection wraps the selection
- Backspace between an empty pair deletes both
- Return between an empty pair (in editors) puts the closer on its own line
- typing a third quote after "" makes a triple-quoted pair

Options are under Tools > Options > Auto-pairs.
"""

import re
import tkinter as tk
from logging import getLogger

from thonny import get_workbench
from thonny.config_ui import ConfigurationPage
from thonny.misc_utils import running_on_windows
from thonny.ui_utils import command_is_pressed, control_is_pressed

logger = getLogger(__name__)

BINDTAG = "ThonnyAutoPairs"

BRACKETS = {"(": ")", "[": "]", "{": "}"}
CLOSERS = set(BRACKETS.values())
QUOTES = {'"', "'"}
PAIRS = {**BRACKETS, '"': '"', "'": "'"}

# a pair is added only when the char right of the cursor is one of these
PAIR_BEFORE = {"", "\n", " ", "\t", ")", "]", "}", ",", ":", ";"}

STRING_PREFIX_REGEX = re.compile(r"(?:^|[^\w])([rRbBuUfFtT]{1,2})$")
VALID_STRING_PREFIXES = {
    "r", "u", "b", "f", "t", "br", "rb", "fr", "rf", "tr", "rt",
}


def _option(name):
    return get_workbench().get_option(name)


def _is_shell(text):
    from thonny.shell import ShellText

    return isinstance(text, ShellText)


def _can_edit_at(text, index):
    if text.is_read_only():
        return False
    if _is_shell(text):
        try:
            return text._editing_allowed() and text._in_current_input_range(index)
        except Exception:
            return False
    return True


def _scan_line(s):
    """Returns (open_quote_or_None, in_comment) for the end of the given line prefix"""
    quote = None
    i = 0
    while i < len(s):
        c = s[i]
        if quote:
            if c == "\\":
                i += 2
            elif s.startswith(quote, i):
                i += len(quote)
                quote = None
            else:
                i += 1
        elif c == "#":
            return None, True
        elif c in QUOTES:
            quote = c * 3 if s.startswith(c * 3, i) else c
            i += len(quote)
        else:
            i += 1
    return quote, False


def _ends_with_escape(s):
    return (len(s) - len(s.rstrip("\\"))) % 2 == 1


def _is_shortcut(event):
    if command_is_pressed(event):
        return True
    # AltGr on Windows comes as Ctrl+Alt, but it types real characters (eg. { on German keyboards)
    return control_is_pressed(event) and not (running_on_windows() and event.state & 0x20000)


def _log_for_undo(text, event):
    log = getattr(text, "_log_keypress_for_undo", None)
    if log:
        log(event)


def _insert_closer(text, event, closer):
    """Put the closer right of the cursor and let Tk insert the opener as usual,
    so that calltips and other key listeners still see the keypress."""
    _log_for_undo(text, event)
    text.insert("insert", closer)
    text.mark_set("insert", "insert-%dc" % len(closer))


def _step_over(text, event):
    _log_for_undo(text, event)
    text.mark_set("insert", "insert+1c")
    text.see("insert")
    return "break"


def _wrap_selection(text, first, last, opener, closer):
    n = len(text.get(first, last))
    text.edit_separator()
    text.insert(last, closer)
    text.insert(first, opener)
    text.edit_separator()

    start = text.index("%s+%dc" % (first, len(opener)))
    end = text.index("%s+%dc" % (start, n))
    text.tag_remove("sel", "1.0", "end")
    text.tag_add("sel", start, end)
    text.mark_set("insert", end)
    return "break"


def _on_key(event):
    text = event.widget
    ch = event.char
    if ch not in PAIRS and ch not in CLOSERS:
        return None
    if _is_shortcut(event):
        return None

    is_quote = ch in QUOTES
    if is_quote and not _option("edit.autopairs_quotes"):
        return None
    if not is_quote and not _option("edit.autopairs_brackets"):
        return None

    if not _can_edit_at(text, "insert"):
        return None

    first, last = text.get_selection_indices()
    if first and last:
        if ch in PAIRS and _can_edit_at(text, first):
            return _wrap_selection(text, first, last, ch, PAIRS[ch])
        return None

    next_char = text.get("insert")
    left = text.get("insert linestart", "insert")

    if ch in CLOSERS:
        if next_char == ch:
            return _step_over(text, event)
        return None

    open_quote, in_comment = _scan_line(left)

    if ch in BRACKETS:
        # at the end of a string (eg. f"|") the closing quote is fine too
        if next_char in PAIR_BEFORE or (open_quote and next_char == open_quote[0]):
            _insert_closer(text, event, BRACKETS[ch])
        return None

    # quotes
    if in_comment or _ends_with_escape(left):
        return None

    if open_quote is not None:
        # inside a string: only closing it is interesting
        if open_quote[0] == ch and next_char == ch:
            return _step_over(text, event)
        return None

    if next_char == ch:
        return None

    if left.endswith(ch * 2) and not left.endswith(ch * 3):
        # "" + " -> """|"""
        _insert_closer(text, event, ch * 3)
        return None

    prev_char = left[-1:]
    if prev_char and (prev_char.isalnum() or prev_char == "_"):
        m = STRING_PREFIX_REGEX.search(left)
        if not m or m.group(1).lower() not in VALID_STRING_PREFIXES:
            return None

    if next_char in PAIR_BEFORE:
        _insert_closer(text, event, ch)
    return None


def _between_pair(text):
    prev_char = text.get("insert-1c")
    return prev_char in PAIRS and text.get("insert") == PAIRS[prev_char]


def _pair_enabled(opener):
    if opener in QUOTES:
        return _option("edit.autopairs_quotes")
    return _option("edit.autopairs_brackets")


def _on_backspace(event):
    text = event.widget
    if text.has_selection() or not _between_pair(text):
        return None
    if not _pair_enabled(text.get("insert-1c")):
        return None
    if not _can_edit_at(text, "insert-1c"):
        return None

    _log_for_undo(text, event)
    text.delete("insert-1c", "insert+1c")
    return "break"


def _on_return(event):
    text = event.widget
    if _is_shell(text) or text.is_read_only() or text.has_selection():
        return None
    if not _option("edit.autopairs_brackets"):
        return None
    if text.get("insert-1c") not in BRACKETS or not _between_pair(text):
        return None

    line = text.get("insert linestart", "insert lineend")
    indent = line[: len(line) - len(line.lstrip(" \t"))]

    _log_for_undo(text, event)
    text.perform_return(event)
    pos = text.index("insert")
    text.insert("insert", "\n" + indent)
    text.mark_set("insert", pos)
    text.see("insert")
    return "break"


def _install(text):
    tags = list(text.bindtags())
    if BINDTAG in tags:
        return
    # Right before the widget's own tag, so that it runs before Thonny's
    # smart backspace / return, but after completion popups (which prepend theirs).
    own_tag = str(text)
    pos = tags.index(own_tag) if own_tag in tags else 0
    tags.insert(pos, BINDTAG)
    text.bindtags(tuple(tags))


def _on_text_created(event):
    text = getattr(event, "text_widget", None)
    if text is not None:
        _install(text)


def _on_focus_in(event):
    if isinstance(event.widget, tk.Text):
        _install(event.widget)


class AutoPairsConfigurationPage(ConfigurationPage):
    def __init__(self, master):
        ConfigurationPage.__init__(self, master)
        self.add_checkbox(
            "edit.autopairs_brackets",
            "Auto-close brackets  ( ) [ ] { }",
        )
        self.add_checkbox(
            "edit.autopairs_quotes",
            "Auto-close quotes  \" \" ' '",
        )
        self.add_checkbox(
            "edit.autopairs_in_shell",
            "Also in Shell",
            pady=(10, 0),
        )


def _check_shell_option(handler):
    def wrapper(event):
        if _is_shell(event.widget) and not _option("edit.autopairs_in_shell"):
            return None
        return handler(event)

    return wrapper


def load_plugin() -> None:
    wb = get_workbench()
    wb.set_default("edit.autopairs_brackets", True)
    wb.set_default("edit.autopairs_quotes", True)
    wb.set_default("edit.autopairs_in_shell", True)

    wb.bind_class(BINDTAG, "<Key>", _check_shell_option(_on_key))
    wb.bind_class(BINDTAG, "<BackSpace>", _check_shell_option(_on_backspace))
    wb.bind_class(BINDTAG, "<Return>", _on_return)
    wb.bind_class(BINDTAG, "<KP_Enter>", _on_return)

    wb.bind("EditorTextCreated", _on_text_created, True)
    wb.bind("ShellTextCreated", _on_text_created, True)
    # fallback for text widgets created before this plugin got loaded
    wb.bind_class("EditorCodeViewText", "<FocusIn>", _on_focus_in, True)
    wb.bind_class("ShellText", "<FocusIn>", _on_focus_in, True)

    wb.add_configuration_page("autopairs", "Auto-pairs", AutoPairsConfigurationPage, 35)
