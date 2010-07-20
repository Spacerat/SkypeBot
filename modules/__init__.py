
import inspect
import sys

#Like I said, bits and pieces. :p

modules = {}

class MessageHook:


    Hooks = []

    def __init__(self,hook):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.Hook = hook
        self.Module = mod.__name__
        MessageHook.Hooks.append(self)

    @classmethod
    def UnHook(cls,modname):
        for x in cls.Hooks:
            if x.Module == "modules.%s"%modname:
                cls.Hooks.remove(x)


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
    ComHook.UnHook(module)
    MessageHook.UnHook(module)
    try:
        modules[module].terminate()
    except:
        pass
    del sys.modules["modules.%s"%module]
    del modules[module]

def load_modules(list):
    for x in list:
        x = x.replace('\n','')
        if x.startswith('/'): return
        try:
            if not x.startswith('#'): add_module(x)
        except ModuleAlreadyLoaded as e:
            print e
