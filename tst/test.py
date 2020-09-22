@property
def strmdl(self):
    str_ = 'machine {\n'
    str_ += f'id {self.idmdl}\n'
    str_ += f'name "dummy_name"\n'

    if self.firstTarget:
        str_ += \ 
        f'firstTarget {self.firstTarget.idmdl}\n'

    for x in self.attrs:
        if not x.name in self._id_based_mdl_attrs:
            str_ += f'{x.name} "{x.value}"\n'

    for x in self.ps:
        if not x.name_attr.value in self.\
        _id_based_mdl_attrs:
            str_ += f'{x.strmdl}\n'

    for x in self.debugs:
        str_ += f'{x.strmdl}\n'

    str_ += '}\n\n'

    if self.children:
        str_ += f'{self.children.strmdl}\n'

    return str_
