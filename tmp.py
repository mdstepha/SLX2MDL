class Tooltip(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Tooltip') and strval.endswith('</Tooltip>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Tooltip(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Tooltip "{self.content}"'
