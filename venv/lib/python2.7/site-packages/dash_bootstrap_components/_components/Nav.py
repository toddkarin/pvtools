# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Nav(Component):
    """A Nav component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- style (dict; optional): Defines CSS styles which will override styles previously set.
- className (string; optional): Often used with CSS to style elements with common properties.
- key (string; optional): A unique identifier for the component, used to improve
performance by React.js while rendering components
See https://reactjs.org/docs/lists-and-keys.html for more info
- pills (boolean; optional): Apply pill styling to nav items. Active items will be indicated by a pill.
- card (boolean; optional): Set to True when using Nav with pills styling inside a CardHeader.
- fill (boolean; optional): Expand the nav items to fill available horizontal space.
- justified (boolean; optional): Expand the nav items to fill available horizontal space, making sure
every nav item has the same width.
- vertical (boolean | string; optional): Stack NavItems vertically. Set to True for a vertical Nav on all screen
sizes, or pass one of the Bootstrap breakpoints ('xs', 'sm', 'md', 'lg',
'xl') for a Nav which is vertical at that breakpoint and above, and
horizontal on smaller screens.
- horizontal (a value equal to: "start", "center", "end"; optional): Specify the horizontal alignment of the NavItems. Options are 'start',
'center', or 'end'.
- navbar (boolean; optional): Set to True if using Nav in Navbar component. This applies the `navbar-nav`
class to the Nav which uses more lightweight styles to match the parent
Navbar better.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, pills=Component.UNDEFINED, card=Component.UNDEFINED, fill=Component.UNDEFINED, justified=Component.UNDEFINED, vertical=Component.UNDEFINED, horizontal=Component.UNDEFINED, navbar=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'pills', 'card', 'fill', 'justified', 'vertical', 'horizontal', 'navbar']
        self._type = 'Nav'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'pills', 'card', 'fill', 'justified', 'vertical', 'horizontal', 'navbar']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Nav, self).__init__(children=children, **args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('Nav(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Nav(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
