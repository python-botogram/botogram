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
    default_style = ""

    styles = {
        token.Whitespace:                "underline #f8f8f8",      # w
        token.Error:                     "#a40000 border:#ef2929", # err
        token.Other:                     NAMES,                # class x

        token.Comment:                   COMMENTS, # c
        token.Comment.Preproc:           COMMENTS,       # cp

        token.Keyword:                   KEYWORD, # k
        token.Keyword.Constant:          KEYWORD, # kc
        token.Keyword.Declaration:       KEYWORD, # kd
        token.Keyword.Namespace:         KEYWORD, # kn
        token.Keyword.Pseudo:            KEYWORD, # kp
        token.Keyword.Reserved:          KEYWORD, # kr
        token.Keyword.Type:              KEYWORD, # kt

        token.Operator:                  OPERATORS, # o
        token.Operator.Word:             KEYWORD, # ow

        token.Punctuation:               NAMES, # p

        token.Name:                      NAMES, # n
        token.Name.Attribute:            NAMES, # na
        token.Name.Builtin:              NAMES, # nb
        token.Name.Builtin.Pseudo:       NAMES, # bp
        token.Name.Class:                NAMES, # nc
        token.Name.Constant:             NAMES, # no
        token.Name.Decorator:            "bold "+OPERATORS, # nd
        token.Name.Entity:               "#ce5c00", # ni
        token.Name.Exception:            NAMES, # ne
        token.Name.Function:             NAMES, # nf
        token.Name.Property:             NAMES, # py
        token.Name.Label:                NAMES, # nl
        token.Name.Namespace:            NAMES, # nn
        token.Name.Other:                NAMES, # nx
        token.Name.Tag:                  KEYWORD, # nt
        token.Name.Variable:             NAMES, # nv
        token.Name.Variable.Class:       NAMES, # vc
        token.Name.Variable.Global:      NAMES, # vg
        token.Name.Variable.Instance:    NAMES, # vi

        token.Number:                    NUMBERS, # m

        token.Literal:                   NAMES, # l
        token.Literal.Date:              NAMES, # ld

        token.String:                    STRING, # s
        token.String.Backtick:           STRING, # sb
        token.String.Char:               STRING, # sc
        token.String.Doc:                COMMENTS, # sd
        token.String.Double:             STRING, # s2
        token.String.Escape:             STRING, # se
        token.String.Heredoc:            STRING, # sh
        token.String.Interpol:           STRING, # si
        token.String.Other:              STRING, # sx
        token.String.Regex:              STRING, # sr
        token.String.Single:             STRING, # s1
        token.String.Symbol:             STRING, # ss

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
