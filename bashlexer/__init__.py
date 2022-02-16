from pygments.lexers.shell import BashLexer
from pygments.token import Keyword, Token


class ExtendedBashLexer(BashLexer):
    name = "extbash"
    aliases = [
        "extbash",
        "extzsh",
        "extconsole",
        "extshell",
        "bash",
        "shell",
        "console",
    ]

    EXTRA_BUILTINS = [
        "alias",
        "which",
        "typeset",
        "echo",
        "cat",
        "ls",
        "mkdir",
        "cp",
        "mv",
        "rm",
        "man",
        "ln",
        "grep",
        "less",
        "awk",
        "sed",
        "cut",
        "paste",
        "head",
        "tail",
        "wc",
        "sort",
        "uniq",
        "tr",
        "fold",
        "xargs",
        "touch",
        "tree",
        "sudo",
        "chsh",
        "python",
        "ifconfig",
        "bash",
        "chmod",
        "vim",
        "printenv",
    ]
    EXTRA_KEYWORDS = [
        ">",
        "<",
        "<<",
        ">>",
        "&",
        "|",
        "!$",
        "!!",
        "~",
        "~-",
        "~+",
        "!^",
        "^",
        "$?",
    ]

    def get_tokens_unprocessed(self, text):
        for index, token, value in BashLexer.get_tokens_unprocessed(self, text):
            if value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            elif value in self.EXTRA_BUILTINS:
                yield index, Token.Name.Builtin, value
            else:
                yield index, token, value
