# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tooltip(Component):
    """A Tooltip component.


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
- target (string; optional): The id of the element to attach the tooltip to
- boundaries_element (string; optional): Boundaries for popper, can be scrollParent, window, viewport, or any DOM
element
- hide_arrow (boolean; optional): Hide arrow on tooltip
- container (string; optional): Where to inject the popper DOM node, default body
- delay (optional): optionally override show/hide delays - default { show: 0, hide: 250 }. delay has the following type: dict containing keys 'show', 'hide'.
Those keys have the following types: 
  - show (number; optional)
  - hide (number; optional) | number
- innerClassName (string; optional): CSS classes to apply to the inner-tooltip
- arrowClassName (string; optional): CSS classes to apply to the arrow-tooltip ('arrow' by default)
- autohide (boolean; optional): Optionally hide tooltip when hovering over tooltip content - default true
- placement (a value equal to: 'auto', 'auto-start', 'auto-end', 'top', 'top-start', 'top-end', 'right', 'right-start', 'right-end', 'bottom', 'bottom-start', 'bottom-end', 'left', 'left-start', 'left-end'; optional): How to place the tooltip.
- offset (string | number; optional): Tooltip offset

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, target=Component.UNDEFINED, boundaries_element=Component.UNDEFINED, hide_arrow=Component.UNDEFINED, container=Component.UNDEFINED, delay=Component.UNDEFINED, innerClassName=Component.UNDEFINED, arrowClassName=Component.UNDEFINED, autohide=Component.UNDEFINED, placement=Component.UNDEFINED, offset=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'target', 'boundaries_element', 'hide_arrow', 'container', 'delay', 'innerClassName', 'arrowClassName', 'autohide', 'placement', 'offset']
        self._type = 'Tooltip'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'target', 'boundaries_element', 'hide_arrow', 'container', 'delay', 'innerClassName', 'arrowClassName', 'autohide', 'placement', 'offset']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tooltip, self).__init__(children=children, **args)

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
            return ('Tooltip(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Tooltip(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
