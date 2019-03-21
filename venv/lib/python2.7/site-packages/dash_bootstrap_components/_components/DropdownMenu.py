# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DropdownMenu(Component):
    """A DropdownMenu component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component.
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- style (dict; optional): Defines CSS styles which will override styles previously set.
- className (string; optional): Often used with CSS to style elements with common properties.
- key (string; optional): A unique identifier for the component, used to improve
performance by React.js while rendering components
See https://reactjs.org/docs/lists-and-keys.html for more info
- label (string; optional): Label for the DropdownMenu toggle.
- direction (a value equal to: 'down', 'left', 'right'; optional): Direction in which to expand the dropdown. Note that expanding
the dropdown upwards is currently unsupported. Default: 'down'.
- in_navbar (boolean; optional): Set this to True if the dropdown is inside a navbar. Default: False.
- addon_type (boolean | a value equal to: 'prepend', 'append'; optional): Set this to 'prepend' or 'append' if the dropdown menu is being used in an input group.
- disabled (boolean; optional): Disable the dropdown.
- nav (boolean; optional): Set this to True if the dropdown is inside a nav for styling consistent
with other nav items. Default: False.
- caret (boolean; optional): Add a caret to the dropdown toggle. Default: True.
- bs_size (a value equal to: 'sm', 'md', 'lg'; optional): Size of the dropdown. 'sm' corresponds to small, 'md' to medium
and 'lg' to large.

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, label=Component.UNDEFINED, direction=Component.UNDEFINED, in_navbar=Component.UNDEFINED, addon_type=Component.UNDEFINED, disabled=Component.UNDEFINED, nav=Component.UNDEFINED, caret=Component.UNDEFINED, bs_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'className', 'key', 'label', 'direction', 'in_navbar', 'addon_type', 'disabled', 'nav', 'caret', 'bs_size']
        self._type = 'DropdownMenu'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'style', 'className', 'key', 'label', 'direction', 'in_navbar', 'addon_type', 'disabled', 'nav', 'caret', 'bs_size']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DropdownMenu, self).__init__(children=children, **args)

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
            return ('DropdownMenu(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'DropdownMenu(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
