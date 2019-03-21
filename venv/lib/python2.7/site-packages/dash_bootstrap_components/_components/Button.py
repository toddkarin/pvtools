# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component.
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- className (string; optional): Often used with CSS to style elements with common properties.
- style (dict; optional): Defines CSS styles which will override styles previously set.
- key (string; optional): A unique identifier for the component, used to improve
performance by React.js while rendering components
See https://reactjs.org/docs/lists-and-keys.html for more info
- n_clicks (number; optional): An integer that represents the number of times
that this element has been clicked on.
- n_clicks_timestamp (number; optional): An integer that represents the time (in ms since 1970)
at which n_clicks changed. This can be used to tell
which button was changed most recently.
- active (boolean; optional): Whether button is in active state. Default: False.
- block (boolean; optional): Create block level button, one that spans the full width of its parent.
Default: False
- color (string; optional): Button color, options: primary, secondary, success, info, warning, danger,
link. Default: secondary.
- disabled (boolean; optional): Disable button (make unclickable). Default: False.
- size (string; optional): Button size, options: 'lg', 'md', 'sm'.
- outline (boolean; optional): Set outline button style, which removes background images and colors for a
lightweight style.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, active=Component.UNDEFINED, block=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, size=Component.UNDEFINED, outline=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'style', 'key', 'n_clicks', 'n_clicks_timestamp', 'active', 'block', 'color', 'disabled', 'size', 'outline']
        self._type = 'Button'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'className', 'style', 'key', 'n_clicks', 'n_clicks_timestamp', 'active', 'block', 'color', 'disabled', 'size', 'outline']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Button, self).__init__(children=children, **args)

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
            return ('Button(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Button(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
