# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popover(Component):
    """A Popover component.


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
- placement (a value equal to: 'auto', 'auto-start', 'auto-end', 'top', 'top-start', 'top-end', 'right', 'right-start', 'right-end', 'bottom', 'bottom-start', 'bottom-end', 'left', 'left-start', 'left-end'; optional): Specify popover placement.
- target (string; optional): ID of the component to attach the popover to.
- container (string; optional): Where to inject the popper DOM node, default body.
- is_open (boolean; optional): Whether the Popover is open or not.
- hide_arrow (boolean; optional): Hide popover arrow.
- innerClassName (string; optional): CSS class to apply to the popover.
- delay (optional): Optionally override show/hide delays - default {show: 0, hide: 250}. delay has the following type: dict containing keys 'show', 'hide'.
Those keys have the following types: 
  - show (number; optional)
  - hide (number; optional) | number
- offset (string | number; optional): Popover offset.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, placement=Component.UNDEFINED, target=Component.UNDEFINED, container=Component.UNDEFINED, is_open=Component.UNDEFINED, hide_arrow=Component.UNDEFINED, innerClassName=Component.UNDEFINED, delay=Component.UNDEFINED, offset=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'placement', 'target', 'container', 'is_open', 'hide_arrow', 'innerClassName', 'delay', 'offset']
        self._type = 'Popover'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'placement', 'target', 'container', 'is_open', 'hide_arrow', 'innerClassName', 'delay', 'offset']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popover, self).__init__(children=children, **args)

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
            return ('Popover(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Popover(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
