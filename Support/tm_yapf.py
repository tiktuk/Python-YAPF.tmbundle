# -*- coding: utf-8 -*-

import os, sys, re, traceback
from sys import stdout, stdin, exit, argv
from yapf.yapflib.yapf_api import FormatCode

source = stdin.read()
filename = getattr(os.environ, 'TM_FILENAME', False) or 'not_saved'
use_tabs = getattr(os.environ, 'TM_SOFT_TABS', False) or os.environ['TM_SOFT_TABS'] == 'NO'
soft_tab_size = getattr(os.environ, 'TM_TAB_SIZE', False) or 4
indent_width = 1 if use_tabs else soft_tab_size
print_diff = False

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

try:
    result = FormatCode(
        source,
        style_config=style_config,
        print_diff=print_diff,
        filename=filename,
    )
except Exception:
    stdout.write(
        ''.join(
            traceback.format_exception(*sys.exc_info())
        )
    )  # yapf: disable
    
    exit(206)  # exiting with this code show's output in a tooltip
else:
    stdout.write(result[0])
