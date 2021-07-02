#!/usr/bin/python3

from commons import * 
from tags_stateflow import * 


class Transformer:

    @classmethod
    def set_treeNodes_and_linkNodes(cls, stateflow):
        """Set all the treeNodes and linkNodes."""

        def set_linkNode(element, siblings):
            """Set the linkNode (last 2 ids) of the element. 
            Assumptions: 
                - The first id in linkNode is assumed to be already set. 
                - arg siblings includes this element too.
                - siblings contains elements in the same order as they appear in stateflow.xml"""

            # only 1 element
            if len(siblings) == 1:
                element.idmdl_linkNode2 = '0'  # no previous sibling
                element.idmdl_linkNode3 = '0'  # no next sibling

            # the element is the first sibling and has other siblings
            elif element == siblings[0]:
                element.idmdl_linkNode2 = '0'  # no previous sibling
                element.idmdl_linkNode3 = siblings[1].idmdl

            # the element is the last sibling and has other siblings
            elif element == siblings[-1]:
                element.idmdl_linkNode2 = siblings[-2].idmdl
                element.idmdl_linkNode3 = '0'  # no next sibling

            # there are at least 3 siblings (this element included) and
            # this element has both previous and next siblings
            else:
                index = siblings.index(element)
                element.idmdl_linkNode2 = siblings[index-1].idmdl
                element.idmdl_linkNode3 = siblings[index+1].idmdl

        def set_nodes_in_state_recursively(state, sibling_states):
            """Set the treeNode (of state) and linkNode (of other elements in the state)
            recursively. 
            ASSUMPTION: The first id of any treeNode or linkNode is already set."""

            state.idmdl_treeNode2 = '0'  # will be overridden if a child state exists

            # set treeNode3 and treeNode4
            # only 1 state
            if len(sibling_states) == 1:
                state.idmdl_treeNode3 = '0'  # no previous sibling
                state.idmdl_treeNode4 = '0'  # no next sibling

            # the state is the first sibling and has other siblings
            elif state == sibling_states[0]:
                state.idmdl_treeNode3 = '0'  # no previous sibling
                state.idmdl_treeNode4 = sibling_states[1].idmdl

            # the state is the last sibling and has other siblings
            elif state == sibling_states[-1]:
                state.idmdl_treeNode3 = sibling_states[-2].idmdl
                state.idmdl_treeNode4 = '0'  # no next sibling

            # there are at least 3 siblings (this state included) and
            # this state has both previous and next siblings
            else:
                index = sibling_states.index(state)
                state.idmdl_treeNode3 = sibling_states[index-1].idmdl
                state.idmdl_treeNode4 = sibling_states[index+1].idmdl

            # -------------------------------------------------------

            if state.children:
                if state.children.datas:
                    state.firstData = state.children.datas[0]
                if state.children.events:
                    state.firstEvent = state.children.events[0]
                if state.children.states:
                    state.idmdl_treeNode2 = state.children.states[0].idmdl

                for data in state.children.datas:
                    set_linkNode(data, state.children.datas)
                for event in state.children.events:
                    set_linkNode(event, state.children.events)
                for junction in state.children.junctions:
                    set_linkNode(junction, state.children.junctions)
                for child_state in state.children.states:
                    set_nodes_in_state_recursively(
                        child_state, state.children.states)
                for transition in state.children.transitions:
                    set_linkNode(transition, state.children.transitions)

        for machine in stateflow.machines:
            if machine.children:
                for target in machine.children.targets:
                    set_linkNode(element=target,
                                 siblings=machine.children.targets)
                for chart in machine.children.charts:
                    # TODO: the information about 1st, 3rd, and 4th ids of treeNode is not
                    # known, so we are setting them to '0', update this once the information
                    # is known
                    chart.idmdl_treeNode1 = '0'
                    chart.idmdl_treeNode2 = '0'  # is overridden below
                    chart.idmdl_treeNode3 = '0'
                    chart.idmdl_treeNode4 = '0'

                    if chart.children:
                        if chart.children.states:
                            chart.idmdl_treeNode2 = chart.children.states[0].idmdl

                        for data in chart.children.datas:
                            set_linkNode(data, chart.children.datas)
                        for event in chart.children.events:
                            set_linkNode(event, chart.children.events)
                        for junction in chart.children.junctions:
                            set_linkNode(junction, chart.children.junctions)
                        for state in chart.children.states:
                            set_nodes_in_state_recursively(
                                state, chart.children.states)
                        for transition in chart.children.transitions:
                            set_linkNode(
                                transition, chart.children.transitions)

    @classmethod
    def set_firstChildren(cls, stateflow):
        """Set the following attributes, if they exist
            - for machines, set firstTarget 
            - for states, set firstTransition, firstJunction, firstData, firstEvent
            - for charts, set fistData, firstEvent, firstTransition 

        """

        # TODO: we might still be missing to set all the firstXXX. 
        # As new firstXXX are discovered in various elements, update this implementation  

        def set_firstChildren_of_state(state):
            if state.children:
                if state.children.datas: 
                    state.firstData = state.children.datas[0]
                if state.children.events: 
                    state.firstEvent = state.children.events[0]
                if state.children.junctions: 
                    state.firstJunction = state.children.junctions[0]
                if state.children.transitions:
                    state.firstTransition = state.children.transitions[0]
                if state.children.states:  # recursion
                    for x in state.children.states:
                        set_firstChildren_of_state(x)

        for machine in stateflow.machines:
            if machine.children:
                for chart in machine.children.charts:
                    if chart.children:
                        if chart.children.datas:
                            chart.firstData = chart.children.datas[0]
                        if chart.children.events:
                            chart.firstEvent = chart.children.events[0]
                        if chart.children.junctions:
                            chart.firstJunction = chart.children.junctions[0]
                        if chart.children.transitions:
                            chart.firstTransition = chart.children.transitions[0]    
                        for state in chart.children.states:
                            set_firstChildren_of_state(state)  # recursively
                        
                if machine.children.targets:
                    machine.firstTarget = machine.children.targets[0]

   
# public funciton     
def stateflow_xml2mdl(xml):
    """Convert stateflow xml string to mdl string"""
    xml = xml.strip()
    xml = Utils.transform_self_closing_tag(xml)
    stateflow = Stateflow(xml, parent_xml=None) 
    Transformer.set_treeNodes_and_linkNodes(stateflow)
    Transformer.set_firstChildren(stateflow)

    mdl = stateflow.strmdl 
    mdl = Utils.remove_multiple_linegaps(mdl)
    mdl = Utils.replacements4mdl(mdl)
    return mdl 



def main():
    
    input_file = 'input.xml'
    with open(input_file, 'r') as file:
        xml = file.read()  # whole file as single string

    mdl = stateflow_xml2mdl(xml) or '--- empty ---'

    with open('op-stateflow.mdl', 'w') as file:
        file.write(mdl)

    # print(mdl)


def test():
    input_file = 'input.xml'
    with open(input_file, 'r') as file:
        xml = file.read()  # whole file as single string
    xml = Utils.transform_self_closing_tag(xml)

    Transformer._xml = xml
    Transformer.set_treeNodes_and_linkNodes(
        None)


if __name__ == '__main__':
    main()
    # test()
