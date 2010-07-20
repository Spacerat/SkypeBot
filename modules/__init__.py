
import inspect
import sys

modules = {}

class MessageHook:


    Hooks = []

    def __init__(self,hook):
        self.Hook = hook
        MessageHook.Hooks.append(self)

class ComHook:

    Hooks = {}

    def __init__(self,command,hook,name='',status='ANY',hidden=False,security=1,admin=False):

        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.Name = name
        self.MStatus = status
        self.Hook = hook
        self.Hidden = hidden
        self.Security=security
        self.Admin = admin
        self.Module = mod.__name__
        ComHook.Hooks[command]=self

    @classmethod
    def UnHook(cls,modname):
        for x in cls.Hooks.keys():
            if cls.Hooks[x].Module == "modules.%s"%modname:
                del cls.Hooks[x]
        del sys.modules["modules.%s"%modname]
        del modules[modname]


class ModuleAlreadyLoaded(Exception): pass

def add_module(module):
    if modules.get(module):
        raise ModuleAlreadyLoaded, "%s has already been loaded."%module
    try:
        modules[module] = __import__(module,globals(),locals(),[],-1)
    except ImportError, e:
        print e
    except Exception, e:
        print "Error loading %s: %s"%(module, str(e))

def unload_module(module):
    pass

def load_modules(list):
    for x in list:
        x = x.replace('\n','')
        if x.startswith('/'): return
        try:
            if not x.startswith('#'): add_module(x)
        except ModuleAlreadyLoaded as e:
            print e