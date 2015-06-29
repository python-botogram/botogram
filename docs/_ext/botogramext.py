from pygments import style
from pygments import token


KEYWORD = "bold #179CDE"
STRING = "#00af00"
NAMES = "#000"
NUMBERS = "#8700ff"
COMMENTS = "#888"
OPERATORS = "#444"


class BotogramStyle(style.Style):
    """Pygments style for the botogram documentation"""
    background_color = "#fff"
    highlight_color = "#f3f3f3"
    default_style = ""

    styles = {
        token.Whitespace:                "underline #f8f8f8",      # w
        token.Error:                     "#a40000 border:#ef2929", # err
        token.Other:                     NAMES,                # class x

        token.Comment:                   COMMENTS, # c

        token.Keyword:                   KEYWORD, # k

        token.Operator:                  OPERATORS, # o
        token.Operator.Word:             KEYWORD, # ow

        token.Punctuation:               NAMES, # p

        token.Name:                      NAMES, # n
        token.Name.Decorator:            "bold "+OPERATORS, # nd
        token.Name.Entity:               "#ce5c00", # ni
        token.Name.Tag:                  KEYWORD, # nt

        token.Number:                    NUMBERS, # m

        token.Literal:                   NAMES, # l

        token.String:                    STRING, # s
        token.String.Doc:                COMMENTS, # sd

        token.Generic:                   NAMES,        # g
        token.Generic.Deleted:           "#a40000",        # gd
        token.Generic.Emph:              "italic #000000", # ge
        token.Generic.Error:             "#ef2929",        # gr
        token.Generic.Heading:           "bold #000080",   # gh
        token.Generic.Inserted:          "#00A000",        # gi
        token.Generic.Output:            "#888",           # go
        token.Generic.Prompt:            "#745334",        # gp
        token.Generic.Strong:            "bold #000000",   # gs
        token.Generic.Subheading:        "bold #800080",   # gu
        token.Generic.Traceback:         "bold #a40000",   # gt
    }
