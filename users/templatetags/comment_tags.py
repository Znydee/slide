from django import template
from users.models import Comment
register = template.Library()


#@register.inclusion_tag('index.html', takes_context=True)
#@register.simple_tag
@register.filter
def has_comment(conn,co):
    com_obj=Comment.objects.filter(post=conn,user=co).first()
    if com_obj == None:
        result = "no"
    else:
        result= "yes"
    return result