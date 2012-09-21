from django import template
import datetime

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print parentdir
os.sys.path.insert(0,parentdir) 
import appsettings


register = template.Library()


class GaJSScriptNode(template.Node):
    def render(self, context):
        return appsettings.GA_JS_PLACEHOLDER


@register.tag(name='djp_ga_js_script')
def djp_ga_js_script(parser, token):
    return GaJSScriptNode()

