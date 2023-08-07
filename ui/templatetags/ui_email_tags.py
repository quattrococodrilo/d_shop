from django import template

register = template.Library()


# ------------------------------------------------------------
# One Column
# ------------------------------------------------------------
class OneColumnNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        tag_open = (
            '<table role="presentation" style="width:100%;border:0;border-spacing:0;">'
        )
        tag_close = "</table>"
        return f"{tag_open}\n\t{content}\n{tag_close}"


@register.tag("onecolumn")
def one_column(parser, token):
    nodelist = parser.parse(("endonecolumn",))
    parser.delete_first_token()
    return OneColumnNode(nodelist)


# ------------------------------------------------------------
# Row
# ------------------------------------------------------------
class RowNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        tag_open = '<tr>\n\t<td style="padding:10px;text-align:left;">'
        tag_close = '\t</td>\n</tr>'
        return f"{tag_open}\n\t\t{content}\n{tag_close}"

@register.tag("row")
def row(parser, token):
    nodelist = parser.parse(("endrow",))
    parser.delete_first_token()
    return RowNode(nodelist)

