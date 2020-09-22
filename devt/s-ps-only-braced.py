
class ActiveStateOutput(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<activeStateOutput') and strval.endswith('</activeStateOutput>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ActiveStateOutput' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return ActiveStateOutput(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'activeStateOutput {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'treeNode {self.treeNode}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'chart {self.chart.idmdl}\n'
        str_ += f'machine {self.machine.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'



        str_ += '}\n\n'
        return str_
