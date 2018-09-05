#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests the PEP8 compliancy of all Python code."""
import subprocess
import flow


def _test_pep8(args):
    """Shell wrapper for Pylint/Pycodestyle calls."""
    flow.hline("%s (%s)" % (args[1], args[0]))
    cmd = " ".join(args)
    proc = subprocess.run(cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          shell=True)
    proc_output = proc.stdout.decode("utf-8") + "\n"
    if proc.returncode == 127:
        print("Binary %s not found!" % args[0])
        return False
    if args[0] == 'pylint':
        if proc.returncode is not 0:
            print("cmd: %s (exit status: %d)\n" % (cmd, proc.returncode))
            print(proc_output)

            # Scan and report pylint ignore tags.
            ignores = subprocess.run(
                "grep -r 'pylint:disable' %s|grep -v grep" % args[1],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                shell=True)
            ignores = ignores.stdout.decode("utf-8").strip()
            if ignores:
                flow.hline("Code-level linter ignores", char=".")
                print(ignores)
            return False
    else:
        if proc.returncode is 1:
            print("cmd: %s (exit status: %d)\n" % (cmd, proc.returncode))
            print(proc_output)
            return False
    return True


if __name__ == '__main__':
    flow.banner(__file__)
    TESTS = []
    TESTS.append(
        _test_pep8(["pycodestyle",
                    ".travis/",
                    "--show-source"]))
    TESTS.append(
        _test_pep8(["pylint",
                    ".travis/*.py",
                    "--disable=duplicate-code",
                    "--disable=no-value-for-parameter"]))
    TESTS.append(
        _test_pep8(["pycodestyle",
                    "app",
                    "--show-source",
                    "--max-line-length=300"]))
    TESTS.append(
        _test_pep8(["pylint",
                    "app",
                    "--disable=line-too-long"]))
    if False in TESTS:
        flow.exit_failed(msg="Please fix the reported codestyle issues.")
    flow.exit_passed(msg="All code is PEP8 compliant!")
