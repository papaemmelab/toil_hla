"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?
You might be tempted to import things from __main__ later, but that will
cause problems, the code will get executed twice:

    - When you run `python -m toil_hla` python will execute
      `__main__.py` as a script. That means there won't be any
      `toil_hla.__main__` in `sys.modules`.

    - When you import __main__ it will get executed again (as a module) because
      there's no `toil_hla.__main__` in `sys.modules`.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from toil_hla import __version__
from toil_hla import commands


def main(command=None):
    """toil_hla command."""
    if command in {"--version", "-v"}:
        msg = f"toil_hla {__version__}"
        print(msg)
    else:
        commands.main()


if __name__ == "__main__":
    main()
