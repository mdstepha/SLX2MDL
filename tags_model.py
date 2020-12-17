#!/usr/bin/python3

from commons import Utils, XmlElement


class Annotation(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Annotation') and strval.endswith('</Annotation>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Annotation' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Annotation(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Annotation {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class AnnotationDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<AnnotationDefaults') and strval.endswith('</AnnotationDefaults>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'AnnotationDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return AnnotationDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'AnnotationDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Array(XmlElement):
    # OBSERVATION:
    # 1. <Array> contains only one type of children tag
    # 2. <Array> does not contain <P> tag (follows from observation 1)
    # 3. 'Dimension' of an array (in mdl) is its number of children

    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Array') and strval.endswith('</Array>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.dimension = len(self.inner_xmls_of_type_xml)
        self.ps = []
        self.objects = []
        self.cells = []
        self.mATStructs = []
        self.arrays = []  # found in matlab-central/RC_Demo_C2000_Control_Unit

        for x in self.inner_xmls:

            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Cell':
                self.cells.append(Cell.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MATStruct':
                self.mATStructs.append(MATStruct.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

                

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Array' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Array(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):

        str_ = 'Array {\n'

        for x in self.attrs:
            if x.name in ['Dimension']:
                continue
            str_ += f'{x.name} "{x.value}"\n'

        str_ += f'Dimension {self.dimension}\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        for x in self.cells:
            str_ += f'{x.strmdl}\n'

        for x in self.mATStructs:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

            

        str_ += '}\n\n'
        return str_


class Block(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Block') and strval.endswith('</Block>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.ports = []
        self.masks = []
        self.systems = []
        self.instanceDatas = []
        self.lists = []
        self.functionPorts = []
        self.objects = [] 
        self.linkDatas = []  # found in corpus/matlab-central/Dual_Clutch_Trans.slx 
        self.instanceDatas = [] # found in corpus/matlab-central/HEV_Battery_Lib.slx
        self.arrays = []  # found in corpus/github/daq2_sim.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Port':
                self.ports.append(Port.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Mask':
                self.masks.append(Mask.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'System':
                self.systems.append(System.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'InstanceData':
                self.instanceDatas.append(InstanceData.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'List':
                self.lists.append(List.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'FunctionPort':
                self.functionPorts.append(FunctionPort.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'LinkData':
                self.linkDatas.append(LinkData.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'InstanceData':
                self.instanceDatas.append(InstanceData.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Block' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Block(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Block {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.ports:
            str_ += f'{x.strmdl}\n'

        for x in self.masks:
            str_ += f'{x.strmdl}\n'

        for x in self.systems:
            str_ += f'{x.strmdl}\n'

        for x in self.instanceDatas:
            str_ += f'{x.strmdl}\n'

        for x in self.lists:
            str_ += f'{x.strmdl}\n'

        for x in self.functionPorts:
            str_ += f'{x.strmdl}\n'

        for x in self.objects: 
            str_ += f'{x.strmdl}\n'

        for x in self.linkDatas: 
            str_ += f'{x.strmdl}\n'

        for x in self.instanceDatas: 
            str_ += f'{x.strmdl}\n'

        for x in self.arrays: 
            str_ += f'{x.strmdl}\n'


        str_ += '}\n\n'
        return str_


class BlockDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<BlockDefaults') and strval.endswith('</BlockDefaults>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'BlockDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return BlockDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'BlockDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class BlockDiagramDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<BlockDiagramDefaults') and strval.endswith('</BlockDiagramDefaults>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.systemDefaults = []
        self.blockDefaults = []
        self.annotationDefaults = []
        self.lineDefaults = []
        self.maskDefaults = []
        self.blockParameterDefaults = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'SystemDefaults':
                self.systemDefaults.append(SystemDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'BlockDefaults':
                self.blockDefaults.append(BlockDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'AnnotationDefaults':
                self.annotationDefaults.append(AnnotationDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'LineDefaults':
                self.lineDefaults.append(LineDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MaskDefaults':
                self.maskDefaults.append(MaskDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'BlockParameterDefaults':
                self.blockParameterDefaults.append(BlockParameterDefaults.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'BlockDiagramDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return BlockDiagramDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.systemDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.blockDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.annotationDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.lineDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.maskDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.blockParameterDefaults:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class BlockParameterDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<BlockParameterDefaults') and strval.endswith('</BlockParameterDefaults>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.blocks = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Block':
                self.blocks.append(Block.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'BlockParameterDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return BlockParameterDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'BlockParameterDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.blocks:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Branch(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Branch') and strval.endswith('</Branch>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.branches = []  # <Branch> can contain <Branch>

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Branch':
                self.branches.append(Branch.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Branch' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Branch(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Branch {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.branches:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Callback(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Callback') and strval.endswith('</Callback>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Callback(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Callback "{self.content}"'


class Capabilities(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Capabilities') and strval.endswith('</Capabilities>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Capabilities(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Capabilities "{self.content}"'


class Cell(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Cell') and strval.endswith('</Cell>')
        super().__init__(strval, parent_xml)
        self.class_attr = None
        for x in self.attrs:
            if x.name == 'Class':
                self.class_attr = x

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Cell(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        quoted = f'Cell "{self.content}"'
        unquoted = f'Cell {self.content}'
        boxed = f'Cell [{self.content}]'

        # as seen from corpus/matlab-central/fir_filter_example.slx, 
        # if attribute 'Class' = 'double', then content is boxed
        # if attribute 'Class' = 'char', then content is quoted
        
        if self.class_attr and self.class_attr.value in ['double']:
            if self.content.startswith('[') and self.content.endswith(']'):
                return unquoted
            return boxed
        return quoted  # default 
        


class ConfigSet(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ConfigSet') and strval.endswith('</ConfigSet>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ConfigSet' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ConfigSet(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Array {\n'
        str_ += 'Type "Handle"\n'
        str_ += f'Dimension {len(self.inner_xmls_of_type_xml)}\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class ConfigurationSet(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ConfigurationSet') and strval.endswith('</ConfigurationSet>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []
        self.arrays = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ConfigurationSet' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ConfigurationSet(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class ConcurrentExecutionSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ConcurrentExecutionSettings') and strval.endswith('</ConcurrentExecutionSettings>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []
        self.arrays = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ConcurrentExecutionSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ConcurrentExecutionSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class ConfigManagerSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ConfigManagerSettings') and strval.endswith('</ConfigManagerSettings>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ConfigManagerSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ConfigManagerSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class Connector(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Connector') and strval.endswith('</Connector>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Connector' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Connector(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Connector {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class ControlOptions(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ControlOptions') and strval.endswith('</ControlOptions>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ControlOptions' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ControlOptions(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        # special : no surrounding braces, just contents
        str_ = '\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class CustomProperty(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<CustomProperty') and strval.endswith('</CustomProperty>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.enumStrPairss = []  # first found in corpus/github-downloaded/CSEI_u.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'EnumStrPairs':
                self.enumStrPairss.append(EnumStrPairs.from_XmlElement(x))
                innerxml_used[x] = True


        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'CustomProperty' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return CustomProperty(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'CustomProperty {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.enumStrPairss:
            str_ += f'{x.strmdl}\n'

            

        str_ += '}\n\n'
        return str_

class Description(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Description') and strval.endswith('</Description>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Description(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Description "{self.content}"'


class DialogControl(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<DialogControl') and strval.endswith('</DialogControl>')
        super().__init__(strval, parent_xml)
        self.object_idmdl = Utils.object_idmdl_by_xml_element(self)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.controlOptions = []
        self.prompts = []
        self.dialogControls = []  # there can be nested <DialogControl> see: applications/sldemo_autotrans
        self.callbacks = []
        self.tooltips = []
        self.filePaths = []  # first found in corpus/matlab-central/Contact_Forces_Lib.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ControlOptions':
                self.controlOptions.append(ControlOptions.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Prompt':
                self.prompts.append(Prompt.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'DialogControl':
                self.dialogControls.append(DialogControl.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Callback':
                self.callbacks.append(Callback.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Tooltip':
                self.tooltips.append(Tooltip.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'FilePath':
                self.filePaths.append(FilePath.from_XmlElement(x))
                innerxml_used[x] = True

                

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'DialogControl' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return DialogControl(xml_element.strval, xml_element.parent_xml)

    def strmdl(self, is_array_element):
        """
        Args: 
            is_array_element (bool): True if the returned str is to be wrapped inside Array{}, else False 
        """

        # special
        str_ = 'Object {\n'

        # OBSERVATION: If multiple <DialogControl> are contained in a parent tag (eg. <Mask>),
        # they are wrapped in Array{}
        #
        # <DialogControl> become Object {} in mdl and they contain $ObjectID, $PropName, and
        # $ClassName.
        #
        # When they are wrapped in Array{}, in original mdl files (generated by Simulink)
        # - $ PropName is moved out (becomes a MANDATORY attribute of Array and renamed to
        #   Propname i.e. no leading $)
        # - $ClassName is NOT removed.       (THIS IS DIFFERENT IN <MaskParameter>)
        # - $ObjectID remains the same.
        #
        # Although keeping $PropName inside these wrapped Object{}s
        # does not harm, we have chosen to remove it just like in the mdl file produced by Simulink.

        str_ += f'$ObjectID {self.object_idmdl}\n'  # TODO: figure out what ObjectID is
        str_ += f'$ClassName "{self.array_type_or_object_className()}"\n'
        if not is_array_element:
            str_ += f'$PropName "DialogControls"\n'

        for x in self.attrs:
            # 'Type' info goes to $ClassName
            if x.name not in ['Type']:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.controlOptions:
            str_ += f'{x.strmdl}\n'

        # OBSERVATION: Some <Prompt> in <DialogControl> do not appear in the mdl file
        # for example, when <DialogControl> has Type="CheckBox", the <Prompt> contained in the
        # <DialogControl> does not appear in the mdl file. (see applications/aero_dap3dof)
        # However, at this time, we are not sure when exactly not to include <Prompt>'s transformation
        # in the mdl format. So, we are always including it.
        # TODO: If this results in problem(s), investigate further and when <Prompt>'s transformation
        # should appear and when it should not and make required changes.

        for x in self.prompts:
            str_ += f'{x.strmdl}\n'

        if self.dialogControls and len(self.dialogControls) > 1:
            str_ += 'Array {\n'
            str_ += f'Type "Simulink.dialog.Control"\n'
            # PropName attribute is mandatory.
            # Notice that there is no leading $
            str_ += 'PropName "DialogControls"\n'
            str_ += f'Dimension {len(self.dialogControls)}\n'
            for x in self.dialogControls:
                str_ += f'{x.strmdl(is_array_element=True)}\n'
            str_ += '}\n'
        else:
            for x in self.dialogControls:
                str_ += f'{x.strmdl(is_array_element=False)}\n'

        for x in self.callbacks:
            str_ += f'{x.strmdl}\n'

        for x in self.tooltips:
            str_ += f'{x.strmdl}\n'

        for x in self.filePaths:
            str_ += f'{x.strmdl}\n'

            

        str_ += '}\n\n'
        return str_

    def array_type_or_object_className(self):
        """Return what value is needed for 
            - Array/Type (if this DialogControl is to be wrapped in array, or
            - Object/$ClassName (if this DialogControl is not be wrapped in array)
        """
        # OBSERVATION: $ClassName, whether it appears inside Object{} or just inside Array{} i.e.
        # outside Object{} is derived from the value of 'Type' attr
        # OBSERVATION: $ClassName xxx may be of the form 'Simulink.dialog.parameter.xxx' or 'Simulink.dialog.xxx'
        # see applications/sldemo_autotrans, applications/aero_dap3dof
        type = self.attr_value_by_name('Type')

        if type in [
            'Button',
            'Group',
            'Text',
            'TabContainer',  # first found in corpus/github-downloaded/adi_ad961_models.slx 
            'Tab',  # first found in corpus/github-downloaded/adi_ad961_models.slx 
            'CollapsiblePanel',  # first found in corpus/github-downloaded/adi_ad961_models.slx 
            'Control',  # first found in corpus/github-downloaded/adi_ad961_models.slx
            'Panel',  # first found in corpus/github/Lib_Turbo_CompressorVG_TMATS.slx 
            'Image', # first found in corpus/github/matlab/Contact_Forces_Lib 
            
        ]:
            return f'Simulink.dialog.{type}'
        elif type in [
            'CheckBox',
            'Edit',
            'Slider',
            'Spinbox',
            'Popup',  # first found in corpus/github-downloaded/adi_ad961_models.slx 
            'RadioButton', # first found in corpus/matlab-central/ACTimeOvercurrentRelayBlock
        ]:
            return f'Simulink.dialog.parameter.{type}'
        else:
            raise Exception(f"Unknown 'Type' attribute '{type}' in <DialogControl>")


class DiagnosticSuppressor(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<DiagnosticSuppressor') and strval.endswith('</DiagnosticSuppressor>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'DiagnosticSuppressor' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return DiagnosticSuppressor(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_

class DialogParameters(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<DialogParameters') and strval.endswith('</DialogParameters>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'DialogParameters' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return DialogParameters(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'DialogParameters {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_

class Display(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Display') and strval.endswith('</Display>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Display' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Display(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += f'Display "{self.content}"'  # special

        str_ += '\n\n'
        return str_


class EditorSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<EditorSettings') and strval.endswith('</EditorSettings>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'EditorSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return EditorSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class EngineSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<EngineSettings') and strval.endswith('</EngineSettings>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'EngineSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return EngineSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special 

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class EnumStrPairs(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<EnumStrPairs') and strval.endswith('</EnumStrPairs>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'EnumStrPairs' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return EnumStrPairs(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'EnumStrPairs {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_

class ExternalFileReference(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ExternalFileReference') and strval.endswith('</ExternalFileReference>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ExternalFileReference' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ExternalFileReference(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'ExternalFileReference {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class ExternalMode(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ExternalMode') and strval.endswith('</ExternalMode>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ExternalMode' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ExternalMode(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class Field(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Field') and strval.endswith('</Field>')
        super().__init__(strval, parent_xml)
        self.name_attr = None
        self.class_attr = None
        for x in self.attrs:
            if x.name == 'Name':
                self.name_attr = x
            if x.name == 'Class':
                self.class_attr = x

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Field(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        quoted = f'{self.name_attr.value} "{self.content}"'  # default
        unquoted = f'{self.name_attr.value} {self.content}'  # special
        boxed = f'{self.name_attr.value} [{self.content}]'  # special

        if self.class_attr and self.class_attr.value in ['double']:
            if self.content.startswith('[') and self.content.endswith(']'):
                return unquoted
            return boxed
        return quoted


class FilePath(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<FilePath') and strval.endswith('</FilePath>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return FilePath(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'FilePath "{self.content}"'




class FunctionConnector(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<FunctionConnector') and strval.endswith('</FunctionConnector>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'FunctionConnector' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return FunctionConnector(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'FunctionConnector {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class FunctionPort(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<FunctionPort') and strval.endswith('</FunctionPort>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'FunctionPort' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return FunctionPort(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'FunctionPort {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class GraphicalInterface(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<GraphicalInterface') and strval.endswith('</GraphicalInterface>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.externalFileReferences = []
        self.modelReferences = []
        self.testPointedSignals = []
        self.inports = []
        self.outports = []
        self.requireFunctions = []
        self.subsystemReferences = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ExternalFileReference':
                self.externalFileReferences.append(ExternalFileReference.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ModelReference':
                self.modelReferences.append(ModelReference.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'TestPointedSignal':
                self.testPointedSignals.append(TestPointedSignal.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Inport':
                self.inports.append(Inport.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Outport':
                self.outports.append(Outport.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'RequireFunction':
                self.requireFunctions.append(RequireFunction.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'SubsystemReference':
                self.subsystemReferences.append(SubsystemReference.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'GraphicalInterface' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return GraphicalInterface(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'GraphicalInterface {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.externalFileReferences:
            str_ += f'{x.strmdl}\n'

        for x in self.modelReferences:
            str_ += f'{x.strmdl}\n'

        for x in self.testPointedSignals:
            str_ += f'{x.strmdl}\n'

        for x in self.inports:
            str_ += f'{x.strmdl}\n'

        for x in self.outports:
            str_ += f'{x.strmdl}\n'

        for x in self.requireFunctions:
            str_ += f'{x.strmdl}\n'

        for x in self.subsystemReferences:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Help(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Help') and strval.endswith('</Help>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Help(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Help "{self.content}"'


class Initialization(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Initialization') and strval.endswith('</Initialization>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Initialization(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Initialization "{self.content}"'


class Inport(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Inport') and strval.endswith('</Inport>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Inport' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Inport(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Inport {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class InstanceData(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<InstanceData') and strval.endswith('</InstanceData>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []  # found in matlab-central/HEV_Battery_Lib.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

                

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'InstanceData' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return InstanceData(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

            

        str_ += '\n\n'
        return str_

class LinkData(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<LinkData') and strval.endswith('</LinkData>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.dialogParameterss = []  # found in matlab-central/Dual_Clutch_Trans.slx 

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'DialogParameters':
                self.dialogParameterss.append(DialogParameters.from_XmlElement(x))
                innerxml_used[x] = True


        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'LinkData' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return LinkData(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'LinkData {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.dialogParameterss:
            str_ += f'{x.strmdl}\n'



        str_ += '}\n\n'
        return str_

class Line(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Line') and strval.endswith('</Line>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.branches = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Branch':
                self.branches.append(Branch.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Line' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Line(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Line {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.branches:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class LineDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<LineDefaults') and strval.endswith('</LineDefaults>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'LineDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return LineDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'LineDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class List(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<List') and strval.endswith('</List>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'List' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return List(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'List {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class LogicAnalyzerPlugin(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<LogicAnalyzerPlugin') and strval.endswith('</LogicAnalyzerPlugin>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'LogicAnalyzerPlugin' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return LogicAnalyzerPlugin(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class Mask(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Mask') and strval.endswith('</Mask>')
        super().__init__(strval, parent_xml)
        self.object_idmdl = Utils.object_idmdl_by_xml_element(self)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.displays = []
        self.types = []
        self.maskParameters = []
        self.dialogControls = []
        self.descriptions = []
        self.initializations = []
        self.helps = []
        self.capabilities = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Display':
                self.displays.append(Display.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Type':
                self.types.append(Type.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MaskParameter':
                self.maskParameters.append(MaskParameter.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'DialogControl':
                self.dialogControls.append(DialogControl.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Description':
                self.descriptions.append(Description.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Initialization':
                self.initializations.append(Initialization.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Capabilities':
                self.capabilities.append(Capabilities.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Help':
                self.helps.append(Help.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ImageFile':
                # the corresponding information does not appear in the mdl file
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Mask' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Mask(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Object {\n'  # special

        str_ += f'$PropName "MaskObject"\n'
        str_ += f'$ObjectID {self.object_idmdl}\n'  # TODO: figure out what ObjectID is
        str_ += f'$ClassName "Simulink.Mask"\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.displays:
            str_ += f'{x.strmdl}\n'

        for x in self.types:
            str_ += f'{x.strmdl}\n'

        if self.maskParameters and len(self.maskParameters) > 1:
            str_ += 'Array {\n'
            str_ += 'Type "Simulink.MaskParameter"\n'
            # PropName attribute is mandatory.
            # Notice that there is no leading $
            str_ += 'PropName "Parameters"\n'
            str_ += f'Dimension {len(self.maskParameters)}\n'
            for x in self.maskParameters:
                str_ += f'{x.strmdl(is_array_element=True)}\n'
            str_ += '}\n'
        else:
            for x in self.maskParameters:
                str_ += f'{x.strmdl(is_array_element=False)}\n'

        if self.dialogControls and len(self.dialogControls) > 1:
            str_ += 'Array {\n'
            str_ += f'Type "{self.dialogControls[0].array_type_or_object_className()}"\n'
            # PropName attribute is mandatory.
            # Notice that there is no leading $
            str_ += 'PropName "DialogControls"\n'
            str_ += f'Dimension {len(self.dialogControls)}\n'
            for x in self.dialogControls:
                str_ += f'{x.strmdl(is_array_element=True)}\n'
            str_ += '}\n'
        else:
            for x in self.dialogControls:
                str_ += f'{x.strmdl(is_array_element=False)}\n'

        for x in self.descriptions:
            str_ += f'{x.strmdl}\n'

        for x in self.initializations:
            str_ += f'{x.strmdl}\n'

        for x in self.helps:
            str_ += f'{x.strmdl}\n'

        for x in self.capabilities:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class MaskDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<MaskDefaults') and strval.endswith('</MaskDefaults>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.displays = []
        self.maskParameters = []
        self.dialogControls = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Display':
                self.displays.append(Display.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MaskParameter':
                self.maskParameters.append(MaskParameter.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'DialogControl':
                self.dialogControls.append(DialogControl.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'MaskDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return MaskDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'MaskDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.displays:
            str_ += f'{x.strmdl}\n'

        # although <MaskDefaults> contains <DialogControl>, the information
        # about the contained <DialogControl> and its children (<ControlOptions>) is
        # not present in the mdl file. So, it is not included in the mdl string

        # for x in self.dialogControls:
        #     str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'

        # special: appears outside the parent
        for x in self.maskParameters:
            str_ += f'{x.strmdl(is_array_element=False)}\n'

        return str_


class MaskParameter(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<MaskParameter') and strval.endswith('</MaskParameter>')
        super().__init__(strval, parent_xml)
        self.object_idmdl = Utils.object_idmdl_by_xml_element(self)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.prompts = []
        self.values = []
        self.typeOptions = []
        self.callbacks = []
        self.ranges = []
        self.tabNames = []  # first found in corpus/github/Lib_Cntrl_FirstOrderActuator_TMATS.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Prompt':
                self.prompts.append(Prompt.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Value':
                self.values.append(Value.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'TypeOptions':
                self.typeOptions.append(TypeOptions.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Callback':
                self.callbacks.append(Callback.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Range':
                self.ranges.append(Range.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'TabName':
                self.tabNames.append(TabName.from_XmlElement(x))
                innerxml_used[x] = True

                

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'MaskParameter' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return MaskParameter(xml_element.strval, xml_element.parent_xml)

    def strmdl(self, is_array_element):
        """
        Args: 
            is_array_element (bool): True if the returned str is to be wrapped inside Array{}, else False 
        """
        # special

        if self.parent_xml.tag == 'MaskDefaults':   # see automotive/sldemo_autotrans
            element_name = 'MaskParameterDefaults'
        elif self.parent_xml.tag == 'Mask':  # see automotive/sldemo_autotrans
            element_name = 'Object'
        else:
            raise Exception(f"Element name for <MaskParameter> not decided")

        str_ = f'{element_name} {{\n'

        # OBSERVATION: If multiple <MaskParameter> are contained in a parent tag (eg. <Mask>),
        # they are wrapped in Array{}
        #
        # <MaskParameter> become Object {} in mdl and they contain $ObjectID, $PropName, and
        # $ClassName.
        #
        # When they are wrapped in Array{}, in original mdl files (generated by Simulink)
        # - $ PropName is moved out (becomes a MANDATORY attribute of Array and renamed to
        #   Propname i.e. no leading $)
        # - $ClassName is removed        (THIS IS DIFFERENT IN <DialogControl>)
        # - $ObjectID remains the same.
        #
        # Although keeping $PropName, and $ClassName inside these wrapped Object{}s
        # does not harm, we have chosen to remove them just like in the mdl file produced by Simulink.

        if element_name == 'Object':
            str_ += f'$ObjectID {self.object_idmdl}\n'  # TODO: figure out what ObjectID is
            if not is_array_element:
                str_ += f'$PropName "Parameters"\n'
                str_ += f'$ClassName "Simulink.MaskParameter"\n'

        # TODO: mdl contains 'Prompt'. What is it? (see dma/ex_modeling_simple_system)

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.prompts:
            str_ += f'{x.strmdl}\n'

        # special 
        for x in self.values:
            str_ += f'{x.strmdl}\n'

        # special: inferred from corpus/matlab-central/Link_A.slx 
        # Even if 'Value' does not appear in attributes or inner tags of <MaskParameter>,
        # the corresponding mdl format still has 'Value' (set to ""). 
        if not self.values:  # if empty
            for x in self.attrs:
                if x.name == 'Value':
                    break 
            else:  # none of the  attributes has name 'Value' 
                str_ += f'Value ""\n'

        for x in self.typeOptions:
            str_ += f'{x.strmdl}\n'

        for x in self.callbacks:
            str_ += f'{x.strmdl}\n'

        for x in self.ranges:
            str_ += f'{x.strmdl}\n'

        for x in self.tabNames:
            str_ += f'{x.strmdl}\n'

        
    

        str_ += '}\n\n'
        return str_

class MaskParameterDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<MaskParameterDefaults') and strval.endswith('</MaskParameterDefaults>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'MaskParameterDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return MaskParameterDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'MaskParameterDefaults {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_

class MATStruct(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<MATStruct') and strval.endswith('</MATStruct>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.fields = []
        self.arrays = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Field':
                self.fields.append(Field.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'MATStruct' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return MATStruct(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'MATStruct {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.fields:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class ModelOrLibraryOrSubsystem(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert (strval.startswith('<Model') and strval.endswith('</Model>')) or (strval.startswith('<Library') and strval.endswith('</Library>')) or (strval.startswith('<Subsystem') and strval.endswith('</Subsystem>'))
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}

        self.ps = []
        self.configManagerSettings = []
        self.editorSettings = []
        self.simulationSettings = []
        self.externalModes = []
        self.modelReferenceSettings = []
        self.concurrentExecutionSettings = []
        self.systems = []
        self.diagnosticSuppressors = []
        self.logicAnalyzerPlugins = []
        self.notesPlugins = []
        self.sLCCPlugins = []
        self.webScopes_FoundationPlugins = []
        self.arrays = []
        self.graphicalInterfaces = []
        self.userParameters = []
        self.modelWorkspaces = []
        self.objects = []
        self.windowsInfos = []
        self.configSets = []
        self.blockDiagramDefaults = []
        self.verifications = []         # found in matlab-central/Baro_Library.slx
        self.configurationSets = []     # found in matlab-central/Baro_Library.slx
        self.systemDefaultss = []       # found in matlab-central/Baro_Library.slx
        self.blockDefaultss = []        # found in matlab-central/Baro_Library.slx
        self.annotationDefaultss = []   # found in matlab-central/Baro_Library.slx
        self.lineDefaultss = []          # found in matlab-central/Baro_Library.slx
        self.maskDefaultss = []          # found in matlab-central/Baro_Library.slx
        self.maskParameterDefaultss = []          # found in matlab-central/Baro_Library.slx
        self.blockParameterDefaultss = []          # found in matlab-central/Baro_Library.slx
        self.engineSettingss = []        # found in matlab-central/Assembly_Quadrotor.slx 

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ConfigManagerSettings':
                self.configManagerSettings.append(ConfigManagerSettings.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'EditorSettings':
                self.editorSettings.append(EditorSettings.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'SimulationSettings':
                self.simulationSettings.append(SimulationSettings.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ExternalMode':
                self.externalModes.append(ExternalMode.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ModelReferenceSettings':
                self.modelReferenceSettings.append(ModelReferenceSettings.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ConcurrentExecutionSettings':
                self.concurrentExecutionSettings.append(ConcurrentExecutionSettings.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'System':
                self.systems.append(System.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'DiagnosticSuppressor':
                self.diagnosticSuppressors.append(DiagnosticSuppressor.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'LogicAnalyzerPlugin':
                self.logicAnalyzerPlugins.append(LogicAnalyzerPlugin.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'NotesPlugin':
                self.notesPlugins.append(NotesPlugin.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'SLCCPlugin':
                self.sLCCPlugins.append(SLCCPluginPlugin.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'WebScopes_FoundationPlugin':
                self.webScopes_FoundationPlugins.append(WebScopes_FoundationPlugin.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'GraphicalInterface':
                self.graphicalInterfaces.append(GraphicalInterface.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'UserParameters':
                self.userParameters.append(UserParameters.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ModelWorkspace':
                self.modelWorkspaces.append(ModelWorkspace.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'WindowsInfo':
                self.windowsInfos.append(WindowsInfo.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ConfigSet':
                self.configSets.append(ConfigSet.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'BlockDiagramDefaults':
                self.blockDiagramDefaults.append(BlockDiagramDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Verification':
                self.verifications.append(Verification.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'ConfigurationSet':
                self.configurationSets.append(ConfigurationSet.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'SystemDefaults':
                self.systemDefaultss.append(SystemDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'BlockDefaults':
                self.blockDefaultss.append(BlockDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'AnnotationDefaults':
                self.annotationDefaultss.append(AnnotationDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'LineDefaults':
                self.lineDefaultss.append(LineDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MaskDefaults':
                self.maskDefaultss.append(MaskDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'MaskParameterDefaults':
                self.maskParameterDefaultss.append(MaskParameterDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'BlockParameterDefaults':
                self.blockParameterDefaultss.append(BlockParameterDefaults.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'EngineSettings':
                self.engineSettingss.append(EngineSettings.from_XmlElement(x))
                innerxml_used[x] = True


        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ModelOrLibraryOrSubsystem' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ModelOrLibraryOrSubsystem(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):

        str_ = f'{self.tag} {{\n'  # can be Model or Library

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.configManagerSettings:
            str_ += f'{x.strmdl}\n'

        for x in self.editorSettings:
            str_ += f'{x.strmdl}\n'

        for x in self.simulationSettings:
            str_ += f'{x.strmdl}\n'

        for x in self.externalModes:
            str_ += f'{x.strmdl}\n'

        for x in self.modelReferenceSettings:
            str_ += f'{x.strmdl}\n'

        for x in self.concurrentExecutionSettings:
            str_ += f'{x.strmdl}\n'

        for x in self.systems:
            str_ += f'{x.strmdl}\n'

        for x in self.diagnosticSuppressors:
            str_ += f'{x.strmdl}\n'

        for x in self.logicAnalyzerPlugins:
            str_ += f'{x.strmdl}\n'

        for x in self.notesPlugins:
            str_ += f'{x.strmdl}\n'

        for x in self.sLCCPlugins:
            str_ += f'{x.strmdl}\n'

        for x in self.webScopes_FoundationPlugins:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        for x in self.graphicalInterfaces:
            str_ += f'{x.strmdl}\n'

        for x in self.userParameters:
            str_ += f'{x.strmdl}\n'

        for x in self.modelWorkspaces:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        for x in self.windowsInfos:
            str_ += f'{x.strmdl}\n'

        for x in self.configSets:
            str_ += f'{x.strmdl}\n'

        for x in self.blockDiagramDefaults:
            str_ += f'{x.strmdl}\n'

        for x in self.verifications:
            str_ += f'{x.strmdl}\n'

        for x in self.configurationSets:
            str_ += f'{x.strmdl}\n'

        for x in self.systemDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.blockDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.annotationDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.lineDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.maskDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.maskParameterDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.blockParameterDefaultss:
            str_ += f'{x.strmdl}\n'

        for x in self.engineSettingss:
            str_ += f'{x.strmdl}\n'


        str_ += '}\n\n'

        str_ = Utils.remove_multiple_linegaps(str_)
        str_ = Utils.replacements4mdl(str_)
        str_ = Utils.remove_multiple_linegaps_between_consecutive_closing_braces(str_)
        return str_


class ModelReference(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ModelReference') and strval.endswith('</ModelReference>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ModelReference' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ModelReference(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'ModelReference {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class ModelReferenceSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ModelReferenceSettings') and strval.endswith('</ModelReferenceSettings>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ModelReferenceSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ModelReferenceSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class ModelWorkspace(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<ModelWorkspace') and strval.endswith('</ModelWorkspace>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'ModelWorkspace' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return ModelWorkspace(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class NotesPlugin(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<NotesPlugin') and strval.endswith('</NotesPlugin>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'NotesPlugin' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return NotesPlugin(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class Object(XmlElement):
    # TODO: what is $ObjectID in mdl? (this is generated)
    # there isObjectID in xml but that does not match mdl's $ObjectID
    # figure out how to generate it

    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Object') and strval.endswith('</Object>')
        super().__init__(strval, parent_xml)
        self.object_idmdl = Utils.object_idmdl_by_xml_element(self)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.arrays = []
        self.objects = []  # <Object> can contain children <Object>
        self.customPropertys = []  # first found in corpus/github-downloaded/CSEI_u.slx

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True
             
            if x.tag == 'CustomProperty':
                self.customPropertys.append(CustomProperty.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Object' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Object(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        # special

        # these <Object> tags are found in configSet0.xml
        if self.attr_value_by_name('ClassName') in [
            'Simulink.ConfigSet',
            'Simulink.SolverCC',
            'Simulink.DataIOCC',
            'Simulink.OptimizationCC',
            'Simulink.DebuggingCC',
            'Simulink.HardwareCC',
            'Simulink.ModelReferenceCC',
            'Simulink.SFSimCC',
            'Simulink.RTWCC',
            'SlCovCC.ConfigComp',
            'hdlcoderui.hdlcc'
        ]:
            element_name = self.attr_value_by_name('ClassName')

        else:
            element_name = 'Object'  # default

        str_ = f'{element_name} {{\n'

        for x in self.attrs:
            name = x.name
            value = x.value

            if x.name in ['ClassName', 'ObjectID', 'PropName']:
                name = '$' + name
            if x.name in ['BackupClass', 'ClassName', 'PropName', 'Version']:
                value = f'"{x.value}"'
            if x.name == 'ObjectID':
                value = self.object_idmdl

            str_ += f'{name} {value}\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        for x in self.customPropertys:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Option(XmlElement):
    # first found in design-model-behavior/prioritydemo
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Option') and strval.endswith('</Option>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Option(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Cell "{self.content}"'


class Outport(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Outport') and strval.endswith('</Outport>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Outport' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Outport(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Outport {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class P(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<P') and strval.endswith('</P>')
        super().__init__(strval, parent_xml)
        self.name_attr = None
        self.class_attr = None
        for x in self.attrs:
            if x.name == 'Name':
                self.name_attr = x
            if x.name == 'Class':
                self.class_attr = x

    @classmethod
    def from_XmlElement(cls, xml_element):
        return P(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        quoted = f'{self.name_attr.value} "{self.content}"'  # default
        unquoted = f'{self.name_attr.value} {self.content}'
        boxed = f'{self.name_attr.value} [{self.content}]'
        unquoted_indented = f'    {self.name_attr.value} {self.content}'

        # order rules by priority.

        if '&quot;' in self.content:  # content contains double quotes i.e. "
            return quoted

        # OBSERVATION: if these are not indented, model comparison shows differences -- don't know why
        # TODO: If mdl-preetification is implemented, this can be removed as preetifying mdl will 
        # introduce indentation by itself 
        if self.name_attr and self.name_attr.value in [
            'rep_seq_t',     # see applications/sldemo_hydroid
            'rep_seq_y',     # see applications/sldemo_hydroid
        ]:
            return unquoted_indented

        if self.name_attr and self.name_attr.value in [
            'Components',  # mandatory
            'Location',  # mandatory
            'Position',
        ]:
            return unquoted

        # contents starting and ending with [ and ] respectively are MOSTLY unquoted,
        # However, if some p tags with content starting and ending in [ and ] respectively need to
        # be quoted, put them in the list inside this rule.
        if self.content.startswith('[') and self.content.endswith(']'):
            # special
            if self.name_attr and self.name_attr.value in [

            ]:
                return quoted
            # default
            return unquoted

        if self.content in ['on', 'off']:
            return unquoted

        if self.class_attr:
            if self.class_attr.value == 'double':
                if self.content.startswith('[') and self.content.endswith(']'):
                    return unquoted
                return boxed
            if self.class_attr.value in ['logical', 'int32', 'uint32']:
                return boxed

        return quoted


class Port(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Port') and strval.endswith('</Port>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.arrays = [] 

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        
            if x.tag == 'Array':
                self.arrays.append(Array.from_XmlElement(x))
                innerxml_used[x] = True
        
        
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Port' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Port(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Port {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'


        str_ += '}\n\n'
        return str_


class Prompt(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Prompt') and strval.endswith('</Prompt>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Prompt(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Prompt "{self.content}"'


class Range(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Range') and strval.endswith('</Range>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Range(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Range {self.content}'


class RequireFunction(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<RequireFunction') and strval.endswith('</RequireFunction>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'RequireFunction' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return RequireFunction(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'RequireFunction {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class SimulationSettings(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<SimulationSettings') and strval.endswith('</SimulationSettings>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for x in self.inner_xmls:
            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'SimulationSettings' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return SimulationSettings(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class SLCCPluginPlugin(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<SLCCPlugin') and strval.endswith('</SLCCPlugin>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'SLCCPlugin' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return SLCCPluginPlugin(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class SubsystemReference(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<SubsystemReference') and strval.endswith('</SubsystemReference>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'SubsystemReference' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return SubsystemReference(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'SubsystemReference {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class System(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<System') and strval.endswith('</System>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.blocks = []
        self.lines = []
        self.annotations = []
        self.lists = []
        self.functionConnectors = []
        self.connectors = [] 

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Block':
                self.blocks.append(Block.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Line':
                self.lines.append(Line.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Annotation':
                self.annotations.append(Annotation.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'List':
                self.lists.append(List.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'FunctionConnector':
                self.functionConnectors.append(FunctionConnector.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Connector':
                self.connectors.append(Connector.from_XmlElement(x))
                innerxml_used[x] = True

                

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'System' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return System(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'System {\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.blocks:
            str_ += f'{x.strmdl}\n'

        for x in self.lines:
            str_ += f'{x.strmdl}\n'

        for x in self.annotations:
            str_ += f'{x.strmdl}\n'

        for x in self.lists:
            str_ += f'{x.strmdl}\n'

        for x in self.functionConnectors:
            str_ += f'{x.strmdl}\n'

        for x in self.connectors:
            str_ += f'{x.strmdl}\n'

            

        str_ += '}\n\n'
        return str_


class SystemDefaults(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<SystemDefaults') and strval.endswith('</SystemDefaults>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'SystemDefaults' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return SystemDefaults(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'System {\n'  # SystemDefaults appears as System only

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_



class TabName(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<TabName') and strval.endswith('</TabName>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return TabName(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'TabName "{self.content}"'




class TestPointedSignal(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<TestPointedSignal') and strval.endswith('</TestPointedSignal>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'TestPointedSignal' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return TestPointedSignal(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'TestPointedSignal {\n'

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


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


class Type(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Type') and strval.endswith('</Type>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Type(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Type "{self.content}"'


class UserParameters(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<UserParameters') and strval.endswith('</UserParameters>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'UserParameters' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return UserParameters(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class TypeOptions(XmlElement):
    # first found in design-model-behavior/prioritydemo
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<TypeOptions') and strval.endswith('</TypeOptions>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.options = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Option':
                self.options.append(Option.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'TypeOptions' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return TypeOptions(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Array {\n'  # special
        str_ += 'Type "Cell"\n'
        str_ += f'Dimension {len(self.inner_xmls_of_type_xml)}\n'
        str_ += 'PropName "TypeOptions"\n'  # required

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.options:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Value(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Value') and strval.endswith('</Value>')
        super().__init__(strval, parent_xml)

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Value(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        return f'Value "{self.content}"'




class Verification(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Verification') and strval.endswith('</Verification>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Verification' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return Verification(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        # special: this tag was found in matlab-central/Baro_Library
        # but the content was not found in corresponding mdl format
        return ''
        # str_ = 'Verification {\n'

        # for x in self.attrs:
        #     str_ += f'{x.name} "{x.value}"\n'

        # for x in self.ps:
        #     str_ += f'{x.strmdl}\n'

        # str_ += '}\n\n'
        # return str_


class WebScopes_FoundationPlugin(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<WebScopes_FoundationPlugin') and strval.endswith('</WebScopes_FoundationPlugin>')
        super().__init__(strval, parent_xml)
        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'WebScopes_FoundationPlugin' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return WebScopes_FoundationPlugin(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''  # special

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


class WindowsInfo(XmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<WindowsInfo') and strval.endswith('</WindowsInfo>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.objects = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_XmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Object':
                self.objects.append(Object.from_XmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'WindowsInfo' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_XmlElement(cls, xml_element):
        return WindowsInfo(xml_element.strval, xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''

        for x in self.attrs:
            str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            str_ += f'{x.strmdl}\n'

        for x in self.objects:
            str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        return str_


if __name__ == '__main__':
    pass
