# -*- coding: utf-8 -*-
"""Test, output and flow-control helpers."""
import os
import sys
import hashlib
import subprocess


def banner(caller, subtext=None, char='#'):
    """Print the head-banner for a test-script."""
    caller = os.path.basename(caller)
    caller = os.path.splitext(caller)[0].lstrip('test_').upper()
    if subtext and "\n" in subtext:
        caller = "%s:\n%s" % (caller, subtext)
    elif subtext:
        caller = "%s - %s" % (caller, subtext)
    hbreak(0)
    hbox(caller, char=char)
    hbreak(0)


def exit_error(msg="Exiting..."):
    """Exit the script in ERROR state with a positive status code."""
    exit_as(1, 'error', msg=msg)


def exit_info(msg="Exiting..."):
    """Exit the script in INFO state with a positive status code."""
    exit_as(0, 'info', msg=msg)


def exit_failed(msg="Exiting..."):
    """Exit the script in FAILED state with a positive status code."""
    exit_as(1, 'failed', msg=msg)


def exit_passed(msg="Exiting..."):
    """Exit the script in PASSED state with a zero status code."""
    exit_as(0, 'passed', msg=msg)


def exit_as(scode, sstring, msg=False, char='#'):
    """Exit the script as specified."""
    if msg is False:
        sys.exit(scode)
    # Update the status string and decorative character.
    sstring = sstring.upper()
    if scode:
        char = '!'
    # Start rendering the output.
    hbreak()
    hline(char=char)
    if msg is None:
        hline(sstring, char=char)
    elif '\n' in msg:
        hline("%s:\n%s" % (sstring, msg), char=char)
    else:
        hline("%s - %s" % (sstring, msg), char=char)
    hline(char=char)
    sys.exit(scode)


def hbox(text, char='.'):
    """Print a horizontal box with text."""
    hline(char=char)
    hline(text, char=char)
    hline(char=char)


def hbreak(lines=1):
    """Print newlines (two by default, just one with lines=0)."""
    print(lines * "\n")


def hline(text='', mlen=95, char='-', lchar=None, rchar=None):
    """Print a horizontal line (with optional text)."""
    if not lchar:
        lchar = char
    if not rchar:
        rchar = char
    for index, line in enumerate(text.split('\n')):
        if line:
            line = ' ' + line + ' '
        if index == 0:
            line_right = (mlen-2-len(line)) * rchar
        else:
            line_right = ((mlen-4-len(line)) * ' ') + rchar + rchar
        print(lchar + lchar + line + line_right)
