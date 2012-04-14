import markdown
import sys

sys.path.append('../')

import mdx_macros

class SummationMacro(mdx_macros.BaseMacro):
    """
    A trivial macro that attempts to sum up a series of numbers.  Example
    usage::
    
        [[Sum(4,6,2,9)]]
    """
    name = 'Summation macro'
    key  = 'Sum'
    
    def handler(self, *args, **kwargs):
        total = 0
        for arg in args:
            try:
                total += arg
            except:
                pass
        
        if self.inline:
            return "<span class='sum'>%s</span>" % total
        return "<div class='sum'>%s</div>" % total

md = markdown.Markdown(
        extensions=['macros'],
        extension_configs={
            'macros': {
                'macros': [SummationMacro]
                }
        })

text = """
This is an example of the `macros` extension for `python-markdown`.

The sum 1+3+5+7 = [[Sum(1,3,5,7)]].  The macro was called like so: `[[Sum(1,3,5,7)]]`.

Macros can be either inline or block-level elements.  For example, here
is the sum of 19923+19875 as a block-level element:

[[Sum(19923, 19875)]]
"""

print md.convert(text)