#!/Users/bhisma/opt/anaconda3/bin/python

from commons import Utils, UtilsStfl, XmlElement 


class StflXmlElement(XmlElement):
    # these mdl attributes are based on id, and thus the value from
    # xml cannot be used directly while forming mdl string.
    # In XML tag they may either as attributes or enclosed <P> tags
    _id_based_mdl_attrs = [
        'chart',
        'firstSubWire',     # found in simulink_general/sldemo_boiler
        'id',
        'machine',
        'outputData',       # found in state
        'outputState',
        'quantum',          # found in automotive/sldemo_fuelsys(junction)
        'SSID',
        'subLink',          # found in simulink_general/sldemo_boiler
        'subviewer',
        'viewObj',
    ]

    # key: some tag
    # value: list of parent tag of the key tag whose id serves
    # as the first element in treeNode/linkNode. If there are
    # multiple such values (for example, 'chart' and 'state',
    # the one which is more closer (in the xml tree hierarchy)
    # to this element will have priority over others (see code
    # section in StflXmlElement.__init__() where this dict is used.)
    node1parent_map = {
        'data': ['chart', 'state'],
        'event': ['chart', 'state'],
        'junction': ['chart', 'state'],
        'target': ['machine'],   # TODO: needs further confirmation
        'transition': ['chart', 'state'],
        'state': ['chart', 'state']
    }

    def __init__(self, strval, parent_xml):
        super().__init__(strval, parent_xml)

        # note that not all StflXmlElements will have each of these attributes set to not-None value
        # They are declared here in the parent class to reduce model complexity (during development)

        # While this may look illogical from OOP design point of view,
        # this is justified since we don't have a complete knowledge of what attributes a class
        # should have. The project is fairly explorative.

        # if an attribute is discovered only in few classes, we will mention that in a comment
        # next to its declaration (for example, see idmdl_subviewer, idmdl_outputState)

        # Only those attributes which can be set here (in this parent class's initializer)
        # will be set by this method. Those attributes which are derived from information
        # contained within an included <P> tag will be set by the respective class's
        # initializer after its self.ps is set.

        self.idmdl = None
        self.idslx = None
        self.ssid = None

        # these are objects, not just ids
        self.chart = None
        self.machine = None
        self.superstate = None
        self.firstData = None
        self.firstEvent = None
        self.firstJunction = None
        self.firstTransition = None

        # these are ids, not objects
        self.idmdl_subviewer = None     # found in junction, state, transition
        self.idmdl_outputState = None   # found in data
        self.idmdl_outputData = None    # found in state
        self.idmdl_firstSubWire = None  # found in transition (simulink_general/sldemo_boiler)

        self.idmdl_treeNode1 = None
        self.idmdl_treeNode2 = None
        self.idmdl_treeNode3 = None
        self.idmdl_treeNode4 = None
        self.idmdl_linkNode1 = None
        self.idmdl_linkNode2 = None
        self.idmdl_linkNode3 = None

        # the information is contined in self.ps
        # so, this will be set
        self.idmdl_quantum1 = None
        self.idmdl_quantum2 = None
        self.idmdl_quantum3 = None
        self.idmdl_quantum4 = None

        # first found in simulink_general/sldemo_boiler (transition)
        self.idmdl_subLink1 = None
        self.idmdl_subLink2 = None
        self.idmdl_subLink3 = None

        # set self.chart
        xml = self.parent_xml
        while xml:
            if xml and xml.tag == 'chart':
                self.chart = xml
                break
            xml = xml.parent_xml

        # set self.machine
        xml = self.parent_xml
        while xml:
            if xml and xml.tag == 'machine':
                self.machine = xml
                break
            xml = xml.parent_xml

        # set self.superstate
        xml = self.parent_xml
        while xml:
            if xml and xml.tag == 'state':
                self.superstate = xml
                break
            xml = xml.parent_xml

        # set self.idmdl_treeNode1
        if self.tag in ['state']:
            xml = self.parent_xml
            while xml:
                if xml and xml.tag in self.node1parent_map[self.tag]:
                    self.idmdl_treeNode1 = xml.idmdl
                    break
                xml = xml.parent_xml

        # set self.idmdl_linkNode1
        if self.tag in ['data', 'event', 'junction', 'transition', 'target', ]:
            xml = self.parent_xml
            while xml:
                if xml and xml.tag in self.node1parent_map[self.tag]:
                    self.idmdl_linkNode1 = xml.idmdl
                    break
                xml = xml.parent_xml

        self.idslx = self.attr_value_by_name('id')
        self.ssid = self.attr_value_by_name('SSID')

        # for <src>, <dst>, idmdl is set in their own __init__()
        # because SSID for these tags is located in a included <P> tag
        # and self.ps are set only in corresponding init methods.
        if self.tag in ['data', 'event', 'junction', 'state', 'transition']:
            self.idmdl = UtilsStfl.idmdl_by_ssid(ssid=self.ssid, idmdl_chart=self.chart.idmdl)

        if self.tag in ['chart', 'instance', 'machine', 'target']:
            self.idmdl = UtilsStfl.idmdl_by_idslx(idslx=self.idslx)

    @property
    def treeNode(self):
        return f"[{self.idmdl_treeNode1} {self.idmdl_treeNode2} {self.idmdl_treeNode3} {self.idmdl_treeNode4}]"

    @property
    def linkNode(self):
        return f"[{self.idmdl_linkNode1} {self.idmdl_linkNode2} {self.idmdl_linkNode3}]"

    @property
    def quantum(self):
        return f"[{self.idmdl_quantum1} {self.idmdl_quantum2} {self.idmdl_quantum3} {self.idmdl_quantum4}]"

    @property
    def subLink(self):
        return f"[{self.idmdl_subLink1} {self.idmdl_subLink2} {self.idmdl_subLink3}]"


####################################################################################

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

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Array(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<array') and strval.endswith('</array>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Array' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Array(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'array {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Chart(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<chart') and strval.endswith('</chart>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.subviewSs = []
        self.emls = []
        self.children = None

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                if p.name_attr.value == 'viewObj':
                    # slx contains viewObj in <P> whose value is equal to its own idslx (observation so far) which needs to be mapped to idmdl
                    self.idmdl_viewObj = UtilsStfl.idmdl_by_idslx(idslx=p.content)

            if x.tag == 'subviewS':
                self.subviewSs.append(SubviewS.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'eml':
                self.emls.append(Eml.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Children':
                self.children = Children.from_StflXmlElement(x)
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Chart' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Chart(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'chart {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'treeNode {self.treeNode}\n'
        str_ += f'machine {self.machine.idmdl}\n'
        str_ += f'viewObj {self.idmdl_viewObj}\n'

        if self.firstData:
            str_ += f'firstData {self.firstData.idmdl}\n'
        if self.firstEvent:
            str_ += f'firstEvent {self.firstEvent.idmdl}\n'
        if self.firstJunction:
            str_ += f'firstJunction {self.firstJunction.idmdl}\n'
        if self.firstTransition:
            str_ += f'firstTransition {self.firstTransition.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.subviewSs:
            str_ += f'{x.strmdl}\n'

        for x in self.emls:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'

        # mdl from children goes outside {}
        if self.children:
            str_ += f'{self.children.strmdl}\n'

        return str_


class Children(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Children') and strval.endswith('</Children>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.charts = []
        self.states = []
        self.transitions = []
        self.junctions = []
        self.datas = []
        self.events = []
        self.targets = []

        for x in self.inner_xmls:
            pass

            if x.tag == 'chart':
                self.charts.append(Chart.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'state':
                self.states.append(State.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'transition':
                self.transitions.append(Transition.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'junction':
                self.junctions.append(Junction.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'data':
                self.datas.append(Data.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'event':
                self.events.append(Event.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'target':
                self.targets.append(Target.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Children' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Children(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = ''

        for x in self.charts:
            str_ += f'{x.strmdl}\n'

        for x in self.states:
            str_ += f'{x.strmdl}\n'

        for x in self.transitions:
            str_ += f'{x.strmdl}\n'

        for x in self.junctions:
            str_ += f'{x.strmdl}\n'

        for x in self.datas:
            str_ += f'{x.strmdl}\n'

        for x in self.events:
            str_ += f'{x.strmdl}\n'

        for x in self.targets:
            str_ += f'{x.strmdl}\n'

        return str_


class Data(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<data') and strval.endswith('</data>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.propss = []
        self.messages = []  # first found in design-model-behavior/slexDynamicSchedulingExample

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                # TODO: We are assuming that the chart of this data is the same as the chart of the output state. What if this does not hold true?
                if p.name_attr.value == 'outputState':
                    self.idmdl_outputState = UtilsStfl.idmdl_by_ssid(p.content, self.chart.idmdl)

            if x.tag == 'props':
                self.propss.append(Props.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'message':
                self.messages.append(Message.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Data' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Data(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'data {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'machine {self.machine.idmdl}\n'
        if self.idmdl_outputState:
            str_ += f'outputState {self.idmdl_outputState}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.propss:
            str_ += f'{x.strmdl}\n'

        for x in self.messages:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Debug(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<debug') and strval.endswith('</debug>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Debug' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Debug(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'debug {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Dst(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<dst') and strval.endswith('</dst>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                if p.name_attr.value == 'SSID':
                    self.idmdl = UtilsStfl.idmdl_by_ssid(p.content, self.chart.idmdl)
        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Dst' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Dst(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'dst {\n'
        if self.idmdl:
            str_ += f'id {self.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Eml(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<eml') and strval.endswith('</eml>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Eml' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Eml(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'eml {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Event(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<event') and strval.endswith('</event>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Event' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Event(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'event {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'machine {self.machine.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Fixpt(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<fixpt') and strval.endswith('</fixpt>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Fixpt' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Fixpt(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'fixpt {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Instance(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<instance') and strval.endswith('</instance>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                if p.name_attr.value == 'machine':
                    self.idmdl_machine = UtilsStfl.idmdl_by_idslx(p.content)
                if p.name_attr.value == 'chart':
                    self.idmdl_chart = UtilsStfl.idmdl_by_idslx(p.content)

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Instance' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Instance(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'instance {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'machine {self.idmdl_machine}\n'
        str_ += f'chart {self.idmdl_chart}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Junction(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<junction') and strval.endswith('</junction>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.has_quantum = False

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                # OBSERVATION: subviewer can be either state or chart
                if p.name_attr.value == 'subviewer':
                    idmdl_subviewer = UtilsStfl.idmdl_by_idslx(idslx=p.content, create_if_needed=False)
                    if not idmdl_subviewer:
                        idmdl_subviewer = UtilsStfl.idmdl_by_ssid(ssid=p.content, idmdl_chart=self.chart.idmdl, create_if_needed=False)
                    if idmdl_subviewer:
                        self.idmdl_subviewer = idmdl_subviewer
                    else:
                        raise Exception(f"Failed to set 'subviewer' of junction.")

                if p.name_attr.value == 'quantum':
                    self.has_quantum = True
                    tokens = p.content.split()
                    self.idmdl_quantum1 = tokens[0][1:]
                    self.idmdl_quantum2 = tokens[1]
                    self.idmdl_quantum3 = tokens[2]
                    self.idmdl_quantum4 = tokens[3][:-1]

                    # OBSERVATION: the ids in quantum attribute are transition ids
                    # cannot just write "if slef.idmdl_quantum1", because bool('0') is True (unlike bool(0))
                    if self.idmdl_quantum1 != '0':
                        self.idmdl_quantum1 = UtilsStfl.idmdl_by_ssid(self.idmdl_quantum1, self.chart.idmdl)
                    if self.idmdl_quantum2 != '0':
                        self.idmdl_quantum2 = UtilsStfl.idmdl_by_ssid(self.idmdl_quantum2, self.chart.idmdl)
                    if self.idmdl_quantum3 != '0':
                        self.idmdl_quantum3 = UtilsStfl.idmdl_by_ssid(self.idmdl_quantum3, self.chart.idmdl)
                    if self.idmdl_quantum4 != '0':
                        self.idmdl_quantum4 = UtilsStfl.idmdl_by_ssid(self.idmdl_quantum4, self.chart.idmdl)

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Junction' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Junction(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'junction {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'chart {self.chart.idmdl}\n'
        str_ += f'subviewer {self.idmdl_subviewer}\n'
        if self.has_quantum:
            str_ += f'quantum {self.quantum}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class LoggingInfo(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<loggingInfo') and strval.endswith('</loggingInfo>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'LoggingInfo' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return LoggingInfo(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'loggingInfo {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Machine(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<machine') and strval.endswith('</machine>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.children = []
        self.debugs = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'debug':
                self.debugs.append(Debug.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Children':
                self.children = Children.from_StflXmlElement(x)
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Machine' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Machine(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'machine {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'name "dummy_name"\n'

        if self.firstTarget:
            str_ += f'firstTarget {self.firstTarget.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.debugs:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'

        if self.children:
            str_ += f'{self.children.strmdl}\n'

        return str_


class Message(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<message') and strval.endswith('</message>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Message' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Message(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'message {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class NoteBox(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<noteBox') and strval.endswith('</noteBox>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'NoteBox' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return NoteBox(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'noteBox {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class P(StflXmlElement):
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
    def from_StflXmlElement(cls, stfl_xml_element):
        return P(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        quoted = f'{self.name_attr.value} "{self.content}"'  # default
        unquoted = f'{self.name_attr.value} {self.content}'
        boxed = f'{self.name_attr.value} [{self.content}]'

        quoted_list = [
            'blockName',
            'codeFlags',
            'dataType',
            'description',
            'document',
            'editorLayout',  # first found in automotive/sldemo_fuelsys/(eml)
            'fimathString',  # first found in automotive/sldemo_fuelsys/(eml)
            'firstIndex',    # first found in powerwindow03/data
            'labelString',
            'logName',   # first found in simulink_general/sldemo_boiler
            'name',
            'sampleTime',
            'script',      # see automotive/sldemo_fuelsys/(eml)
            'size',         # first foundin powerwindow03/data
        ]

        if self.name_attr.value in quoted_list:
            return quoted
        return unquoted


class Props(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<props') and strval.endswith('</props>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.arrays = []
        self.types = []
        self.units = []
        self.ranges = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'array':
                self.arrays.append(Array.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'type':
                self.types.append(Type.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'unit':
                self.units.append(Unit.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'range':
                self.ranges.append(Range.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Props' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Props(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'props {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.arrays:
            str_ += f'{x.strmdl}\n'

        for x in self.types:
            str_ += f'{x.strmdl}\n'

        for x in self.units:
            str_ += f'{x.strmdl}\n'

        for x in self.ranges:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Range(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<range') and strval.endswith('</range>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Range' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Range(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'range {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Simulink(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<simulink') and strval.endswith('</simulink>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Simulink' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Simulink(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'simulink {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Slide(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<slide') and strval.endswith('</slide>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Slide' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Slide(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'slide {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Src(StflXmlElement):
    """the SSID in <src> and <dst> is of corresponding state/junction."""

    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<src') and strval.endswith('</src>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                # For some src eg. the initial transition which have no source state/junction,
                # this condition will never be met and
                # self.idmdl will remain None (set in super()'s init)
                if p.name_attr.value == 'SSID':
                    self.idmdl = UtilsStfl.idmdl_by_ssid(p.content, self.chart.idmdl)

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Src' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Src(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'src {\n'
        if self.idmdl:
            str_ += f'id {self.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class State(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<state') and strval.endswith('</state>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.subviewSs = []
        self.children = None
        self.activeStateOutputs = []
        self.simulinks = []
        self.emls = []
        self.noteBoxs = []
        self.loggingInfos = []

        for x in self.inner_xmls:

            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                # OBSERVATION: subviewer can be either state or chart
                if p.name_attr.value == 'subviewer':
                    idmdl_subviewer = UtilsStfl.idmdl_by_idslx(idslx=p.content, create_if_needed=False)
                    if not idmdl_subviewer:
                        idmdl_subviewer = UtilsStfl.idmdl_by_ssid(ssid=p.content, idmdl_chart=self.chart.idmdl, create_if_needed=False)
                    if idmdl_subviewer:
                        self.idmdl_subviewer = idmdl_subviewer
                    else:
                        raise Exception(f"Failed to set 'subviewer' of state.")
                if p.name_attr.value == 'outputData':
                    self.idmdl_outputData = UtilsStfl.idmdl_by_ssid(p.content, self.chart.idmdl)

            if x.tag == 'subviewS':
                self.subviewSs.append(SubviewS.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Children':
                self.children = Children.from_StflXmlElement(x)
                innerxml_used[x] = True

            if x.tag == 'activeStateOutput':
                self.activeStateOutputs.append(ActiveStateOutput.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'simulink':
                self.simulinks.append(Simulink.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'eml':
                self.emls.append(Eml.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'noteBox':
                self.noteBoxs.append(NoteBox.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'loggingInfo':
                self.loggingInfos.append(LoggingInfo.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'State' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return State(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'state {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'treeNode {self.treeNode}\n'
        str_ += f'chart {self.chart.idmdl}\n'
        str_ += f'subviewer {self.idmdl_subviewer}\n'

        if self.firstData:
            str_ += f'firstData {self.firstData.idmdl}\n'
        if self.firstEvent:
            str_ += f'firstEvent {self.firstEvent.idmdl}\n'
        if self.firstJunction:
            str_ += f'firstJunction {self.firstJunction.idmdl}\n'
        if self.firstTransition:
            str_ += f'firstTransition {self.firstTransition.idmdl}\n'
        if self.idmdl_outputData:
            str_ += f'outputData {self.idmdl_outputData}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.subviewSs:
            str_ += f'{x.strmdl}\n'

        for x in self.activeStateOutputs:
            str_ += f'{x.strmdl}\n'

        for x in self.simulinks:
            str_ += f'{x.strmdl}\n'

        for x in self.emls:
            str_ += f'{x.strmdl}\n'

        for x in self.noteBoxs:
            str_ += f'{x.strmdl}\n'

        for x in self.loggingInfos:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'

        if self.children:
            str_ += f'{self.children.strmdl}\n'

        return str_


class Stateflow(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<Stateflow') and strval.endswith('</Stateflow>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.machines = []
        self.instances = []
        self.children = None

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'machine':
                self.machines.append(Machine.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'instance':
                self.instances.append(Instance.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'Children':
                self.children = Children.from_StflXmlElement(x)
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Stateflow' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Stateflow(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'Stateflow {\n\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.machines:
            str_ += f'{x.strmdl}\n'

        for x in self.instances:
            str_ += f'{x.strmdl}\n'

        if self.children:
            str_ += f'{self.children.strmdl}\n'

        str_ += '}'
        return str_


class SubviewS(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<subviewS') and strval.endswith('</subviewS>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'SubviewS' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return SubviewS(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'subviewS {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Target(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<target') and strval.endswith('</target>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Target' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Target(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'target {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'machine {self.machine.idmdl}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Transition(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<transition') and strval.endswith('</transition>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.src = None
        self.dst = None
        self.slide = None
        self.has_subLink = False

        for x in self.inner_xmls:

            if x.tag == 'P':
                p = P.from_StflXmlElement(x)
                self.ps.append(p)
                innerxml_used[x] = True
                # OBSERVATION: subviewer can be either state or chart
                if p.name_attr.value == 'subviewer':
                    idmdl_subviewer = UtilsStfl.idmdl_by_idslx(idslx=p.content, create_if_needed=False)
                    if not idmdl_subviewer:
                        idmdl_subviewer = UtilsStfl.idmdl_by_ssid(ssid=p.content, idmdl_chart=self.chart.idmdl, create_if_needed=False)
                    if idmdl_subviewer:
                        self.idmdl_subviewer = idmdl_subviewer
                    else:
                        raise Exception(f"Failed to set 'subviewer' of transition.")
                # OBSERVATION: firstSubWire is an id of some transition
                if p.name_attr.value == 'firstSubWire':
                    self.idmdl_firstSubWire = UtilsStfl.idmdl_by_ssid(p.content, self.chart.idmdl)

                if p.name_attr.value == 'subLink':
                    self.has_subLink = True
                    tokens = p.content.split()
                    self.idmdl_subLink1 = tokens[0][1:]
                    self.idmdl_subLink2 = tokens[1]
                    self.idmdl_subLink3 = tokens[2][:-1]

                    # OBSERVATION: the ids in subLink attribute are transition ids
                    # cannot just write "if slef.idmdl_subLink1", because bool('0') is True (unlike bool(0))
                    if self.idmdl_subLink1 != '0':
                        self.idmdl_subLink1 = UtilsStfl.idmdl_by_ssid(self.idmdl_subLink1, self.chart.idmdl)
                    if self.idmdl_subLink2 != '0':
                        self.idmdl_subLink2 = UtilsStfl.idmdl_by_ssid(self.idmdl_subLink2, self.chart.idmdl)
                    if self.idmdl_subLink3 != '0':
                        self.idmdl_subLink3 = UtilsStfl.idmdl_by_ssid(self.idmdl_subLink3, self.chart.idmdl)

            if x.tag == 'src':
                self.src = Src.from_StflXmlElement(x)
                innerxml_used[x] = True

            if x.tag == 'dst':
                self.dst = Dst.from_StflXmlElement(x)
                innerxml_used[x] = True

            if x.tag == 'slide':
                self.slide = Slide.from_StflXmlElement(x)
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Transition' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Transition(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'transition {\n'
        str_ += f'id {self.idmdl}\n'
        str_ += f'ssIdNumber {self.ssid}\n'
        str_ += f'linkNode {self.linkNode}\n'
        str_ += f'chart {self.chart.idmdl}\n'
        str_ += f'subviewer {self.idmdl_subviewer}\n'

        if self.idmdl_firstSubWire:
            str_ += f'firstSubWire {self.idmdl_firstSubWire}\n'

        if self.has_subLink:
            str_ += f'subLink {self.subLink}\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '\n\n'
        str_ += f'{self.src.strmdl}\n'
        str_ += f'{self.dst.strmdl}\n'
        str_ += f'{self.slide.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Type(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<type') and strval.endswith('</type>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []
        self.fixpts = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

            if x.tag == 'fixpt':
                self.fixpts.append(Fixpt.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Type' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Type(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'type {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        for x in self.fixpts:
            str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


class Unit(StflXmlElement):
    def __init__(self, strval, parent_xml):
        strval = strval.strip()
        assert strval.startswith('<unit') and strval.endswith('</unit>')
        super().__init__(strval, parent_xml)

        innerxml_used = {x: False for x in self.inner_xmls if x.type == 'xml'}
        self.ps = []

        for x in self.inner_xmls:
            if x.tag == 'P':
                self.ps.append(P.from_StflXmlElement(x))
                innerxml_used[x] = True

        for ix, u in innerxml_used.items():
            if not u:
                raise Exception(f"Inner XML of 'Unit' not used.\nUnused XML:\n\n{ix.strval}")

    @classmethod
    def from_StflXmlElement(cls, stfl_xml_element):
        return Unit(stfl_xml_element.strval, stfl_xml_element.parent_xml)

    @property
    def strmdl(self):
        str_ = 'unit {\n'

        for x in self.attrs:
            if not x.name in self._id_based_mdl_attrs:
                str_ += f'{x.name} "{x.value}"\n'

        for x in self.ps:
            if not x.name_attr.value in self._id_based_mdl_attrs:
                str_ += f'{x.strmdl}\n'

        str_ += '}\n\n'
        return str_


def main():
    import glob

    files = glob.glob('**/stateflow-preprocessed.xml', recursive=True)
    for file in files[-1:]:
        print(file)
        Utils.copy_file(file, 'input.xml')

        with open('input.xml') as file:
            xml = file.read()
        xml = xml.strip()
        stateflow = Stateflow(strval=xml, parent_xml=None)
        mdl = stateflow.strmdl
        with open('output.xml', 'w') as file:
            file.write(mdl)


if __name__ == '__main__':
    main()
    pass
