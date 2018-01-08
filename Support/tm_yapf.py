# -*- coding: utf-8 -*-

import os
import sys
import traceback
import textwrap
from sys import stdout, stdin, exit, argv
from yapf.yapflib.yapf_api import FormatCode


def calc_indent_width(s):
    return len(s) - len(s.lstrip())


def indent_info(s):
    '''
    Returns (indent_width, indent_char, indentation) if all lines in the
    string s are indented by the same whitespace
    '''

    res = (0, None, None)

    if s[0] in (' ', '\t'):
        # The string starts with whitespace
        indent_char = s[0]
        indent_width_of_first_line = calc_indent_width(s)
        indentation_of_first_line = s[:indent_width_of_first_line]

        # Returns True if all lines start with the same indentation
        if all(
            line.startswith(indentation_of_first_line)
            for line in s.splitlines()
        ):
            res = (
                indent_width_of_first_line,
                indent_char,
                indentation_of_first_line,
            )

    return res


filename = getattr(os.environ, 'TM_FILENAME', False) or 'not_saved'
soft_tab_size = getattr(os.environ, 'TM_TAB_SIZE', False) or 4
did_helpfully_dedent = False
print_diff = False
use_tabs = False
source = stdin.read()

if 'TM_SOFT_TABS' in os.environ:
    use_tabs = os.environ['TM_SOFT_TABS'] == 'NO'

indent_width = 1 if use_tabs else soft_tab_size

style_config = {
    'use_tabs': use_tabs,
    'dedent_closing_brackets': True,
    'indent_width': indent_width,
    'continuation_indent_width': indent_width,
}

if len(argv) > 2:
    if argv[2] == '--vertical':
        style_config.update({'column_limit': 1})
    if argv[2] == '--diff':
        print_diff = True

# If every line are equally indented we dedent them before formatting.
# This allows for selecting a range of lines in the middle of the file and
# formatting those only without getting an IndentationError exception.
# We indent the result accordingly afterwards.
indent_w, indent_ch, indentation = indent_info(source)

if indent_w:
    source = textwrap.dedent(source)
    did_helpfully_dedent = True

try:
    format_result = FormatCode(
        source,
        style_config=style_config,
        print_diff=print_diff,
        filename=filename,
    )

    # Indent the result again if we dedented it earlier
    result = format_result[0] if not did_helpfully_dedent else textwrap.indent(
        format_result[0], indentation
    )
except Exception:
    stdout.write(
        ''.join(
            traceback.format_exception(*sys.exc_info())
        )
    )  # yapf: disable

    exit(206)  # exiting with this code show's output in a tooltip
else:
    stdout.write(result)
