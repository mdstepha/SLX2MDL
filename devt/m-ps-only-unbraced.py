class Replaceme(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Replaceme') and strval.endswith(
            '</Replaceme>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(
                    f"Inner XML of 'Replaceme' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element, xml_element.parent_xml):
        return Replaceme(xml_element.strval)

    @property
    def strmdl(self):
        str_ = ''

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_