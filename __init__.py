import markdown
import re

MACRO_RE = r'\[\[(?P<macro>(?P<name>[A-Za-z0-9_^(]+)\((?P<args>.*)\))\]\]'

class BaseMacro(object):
    """
    A base class for creating new macros.  Extend this class, changing the
    ``name`` and ``key`` attributes and define your own ``handler`` function.
    """
    name = 'Base macro'
    key  = 'Macro'
    
    def __init__(self, inline):
        self.inline = inline
    
    def handler(self, *args, **kwargs):
        pass

def render_macro(name, arguments, inline, config):
    """
    Converts a macro found within a Markdown document into HTML.  If the macro
    fails for whatever reason, nothing is returned.
    """
    for MacroKlass in config.get('macros', []):
        if MacroKlass.key == name:
            macro = MacroKlass(inline)
            if macro.handler:
                args, kwargs = [], {}
                for arg in arguments.split(','):
                    if '=' in arg:
                        k, v = arg.strip().split('=', 1)
                        kwargs[k] = v
                    else:
                        args.append(arg.strip())
                return macro.handler(*args, **kwargs)

class MacroExtension(markdown.Extension):
    """
    Macro Extension for Python-Markdown.
    """
    def __init__(self, config):
        # set extension defaults
        self.config = {'macros': []}
        
        for conf in config:
            if conf[0] == "macros":
                self.config['macros'].extend(conf[1])

    def extendMarkdown(self, md, md_globals):
        macroPattern = MacroPattern(MACRO_RE, self.config)
        md.inlinePatterns.add('macro', macroPattern, "<not_strong")
        md.parser.blockprocessors.add('macro', MacroBlockParser(self.config, md.parser), '<empty')

class MacroPattern(markdown.inlinepatterns.Pattern):
    """
    Matches inline macros.
    """
    def __init__(self, pattern, config):
        markdown.inlinepatterns.Pattern.__init__(self, pattern)
        self.config = config
    
    def handleMatch(self, m):
        macro_name = m.groupdict()['name']
        rendered = render_macro(macro_name, m.groupdict()['args'], True, self.config)
        if rendered:
            return markdown.util.etree.fromstring(rendered)
        else:
            logger.error("Invalid macro: %s" % macro_name)
            return m.group(0)

class MacroBlockParser(markdown.blockprocessors.BlockProcessor):
    """
    Matches block-level macros.
    """
    def __init__(self, config, *args, **kwargs):
        markdown.blockprocessors.BlockProcessor.__init__(self, *args, **kwargs)
        self.config = config
        self.pattern = re.compile(MACRO_RE)
    
    def test(self, parent, block):
        return (self.pattern.match(block.strip()) is not None)
    
    def run(self, parent, blocks):
        block = blocks.pop(0).strip()
        m = self.pattern.match(block)
        if m:
            macro_name = m.groupdict()['name']
            rendered = render_macro(macro_name, m.groupdict()['args'], False, self.config)
            if rendered:
                elem = markdown.util.etree.fromstring(rendered)
                parent.append(elem)
            else:
                # The macro doesn't exist, so just place the macro in the
                # output wrapped in a <p> tag
                elem = markdown.util.etree.SubElement(parent, 'p')
                elem.text = block
                logger.error("Invalid macro: %s" % macro_name)
        
def makeExtension(config=[]):
    return MacroExtension(config)