# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Row(Component):
    """A Row component.


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
- no_gutters (boolean; optional): Remove the "gutters" between columns in this row.
see https://getbootstrap.com/docs/4.0/layout/grid/#no-gutters
- align (a value equal to: 'start', 'center', 'end'; optional): Set vertical alignment of columns in this row. Options are 'start',
'center' and 'end'.
- justify (a value equal to: 'start', 'center', 'end', 'around', 'between'; optional): Set horizontal spacing and alignment of columns in this row. Options are
'start', 'center', 'end', 'around' and 'between'.
- form (boolean; optional): For use in forms. When set to True the `form-row` class is applied, which
overrides the default column gutters for a tighter, more compact layout.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, no_gutters=Component.UNDEFINED, align=Component.UNDEFINED, justify=Component.UNDEFINED, form=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'no_gutters', 'align', 'justify', 'form']
        self._type = 'Row'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'no_gutters', 'align', 'justify', 'form']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Row, self).__init__(children=children, **args)

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
            return ('Row(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Row(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
