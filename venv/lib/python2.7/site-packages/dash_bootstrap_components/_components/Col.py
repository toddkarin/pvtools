# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Col(Component):
    """A Col component.


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
- width (optional): Specify the width of the column. Behind the scenes this sets behaviour at
the xs breakpoint, and will be overriden if xs is specified.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- xs (optional): Specify column behaviour on an extra small screen.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- sm (optional): Specify column behaviour on a small screen.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- md (optional): Specify column behaviour on a medium screen.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- lg (optional): Specify column behaviour on a large screen.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- xl (optional): Specify column behaviour on an extra large screen.

Valid arguments are boolean, an integer in the range 1-12 inclusive, or a
dictionary with keys 'offset', 'order', 'size'. See the documentation for
more details.
- align (a value equal to: 'start', 'center', 'end'; optional): Set vertical alignment of this column's content in the parent row. Options
are 'start', 'center', 'end'.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, width=Component.UNDEFINED, xs=Component.UNDEFINED, sm=Component.UNDEFINED, md=Component.UNDEFINED, lg=Component.UNDEFINED, xl=Component.UNDEFINED, align=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'width', 'xs', 'sm', 'md', 'lg', 'xl', 'align']
        self._type = 'Col'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'width', 'xs', 'sm', 'md', 'lg', 'xl', 'align']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Col, self).__init__(children=children, **args)

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
            return ('Col(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Col(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
