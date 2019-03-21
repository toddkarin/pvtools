# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Progress(Component):
    """A Progress component.


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
- tag (string; optional): HTML tag to use for the progress bar, default: div
- bar (boolean; optional): Apply progress-bar class, for use inside a multi progress bar.
- multi (boolean; optional): Create container for multiple progress bars
- max (string | number; optional): Upper limit for value, default: 100
- value (string | number; optional): Specify progress, value from 0 to max inclusive.
- animated (boolean; optional): Animate the bar, must have striped set to True to work.
- striped (boolean; optional): Use striped progress bar
- color (string; optional): Set color of the progress bar, options: primary, secondary, success,
warning, danger, info.
- barClassName (string; optional): CSS classes to apply to the bar.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, tag=Component.UNDEFINED, bar=Component.UNDEFINED, multi=Component.UNDEFINED, max=Component.UNDEFINED, value=Component.UNDEFINED, animated=Component.UNDEFINED, striped=Component.UNDEFINED, color=Component.UNDEFINED, barClassName=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'tag', 'bar', 'multi', 'max', 'value', 'animated', 'striped', 'color', 'barClassName']
        self._type = 'Progress'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'tag', 'bar', 'multi', 'max', 'value', 'animated', 'striped', 'color', 'barClassName']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Progress, self).__init__(children=children, **args)

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
            return ('Progress(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Progress(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
