'''
Created on Mar 4, 2012

@package: introspection
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Implementation for the components introspection.
'''

from ally.internationalization import dgettext
from ally.api.model import Part
from ally.container import wire
from ally.container.aop import modulesIn
from ally.container.ioc import injected
from ally.exception import InputException, Ref
from ally.support.api.util_service import trimIter
from introspection.api.component import IComponentService, Component
from os import path
import sys

# --------------------------------------------------------------------

@injected
class ComponentService(IComponentService):
    '''
    Provides the implementation for @see: IComponentService.
    '''
    
    package = '__setup__'; wire.config('package', doc=
    'The top package where the components are configured')
    
    def __init__(self):
        '''
        Constructs the components service.
        '''
        assert isinstance(self.package, str), 'Invalid package pattern %s' % self.package
    
    def getById(self, id):
        '''
        @see: IComponentService.getById
        '''
        assert isinstance(id, str), 'Invalid id %s' % id
        modules = modulesIn('%s.%s' % (self.package, id)).asList()
        if len(modules) != 1: raise InputException(Ref(dgettext('error', 'Invalid component id'), ref=Component.Id))
        return self.componentFor(modules[0])
    
    def getComponents(self, offset, limit):
        '''
        @see: IComponentService.getComponents
        '''
        modules = modulesIn('%s.*' % self.package).asList()
        modules.sort()
        components = (self.componentFor(module) for module in modules)
        return Part(trimIter(components, len(modules), offset, limit), len(modules))

    # ----------------------------------------------------------------
    
    def componentFor(self, module):
        '''
        Create a component based on the provided module.
        
        @param module: string
            The module to create a component for.
        @return: Component
            The component reflecting the module.
        '''
        c = Component()
        c.Id = module[len(self.package) + 1:]
        
        m = sys.modules.get(module)
        if m:
            c.Loaded = True
            c.Name = getattr(m, 'NAME', None)
            c.Group = getattr(m, 'GROUP', None)
            c.Version = getattr(m, 'VERSION', None)
            c.Description = getattr(m, 'DESCRIPTION', None)
            c.Path = path.relpath(path.dirname(path.dirname(path.dirname(m.__file__))))
            c.InEgg = not path.isfile(m.__file__)
        else:
            c.Loaded = False
            
        return c
