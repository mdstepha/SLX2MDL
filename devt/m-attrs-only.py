
class Replaceme(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Replaceme') and strval.endswith('</Replaceme>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element, xml_element.parent_xml):
        return Replaceme(xml_element.strval)

    @property
    def strmdl(self):
        return f'Replaceme "{self.content}"'