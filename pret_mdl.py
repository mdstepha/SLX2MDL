class Hello: 
    @classmethod
    def preetify_xml(cls, xml, idtn_space=2):
        """Return a preetified version of the xml string.
        Self-closing tags, if any, will be transformed to non-self-closing tags.

        THIS METHOD IS WRITTEN TO REMOVE THE DEPENDENCY ON PYTHON'S LIBRARY

        Args:
            xml(str): input xml string
            idtn_space(int, optional): number of spaces for indentation

        """

        def break_xml_into_tags_and_content(xml):
            """Return (<start_tag>, content, </end_tag>).
            Leading/trailing spaces in the content, if any, are NOT striped.

            Assumptions:
                - xml has no self-closing tag
            """
            xml = xml.strip()

            index_stag_start = 0
            i = 1
            while True:
                i += 1
                if xml[i] == '>':
                    index_stag_end = i + 1  # exclusive
                    break
                elif xml[i] == ' ':
                    j = i
                    while True:
                        j += 1
                        if xml[j] == '>':
                            index_stag_end = j + 1  # exclusive
                            break
                    break

            index_content_start = index_stag_end  # inclusive

            index_etag_end = len(xml)  # exclusive
            i = index_etag_end
            while True:
                i -= 1
                if xml[i:i+2] == '</':
                    index_etag_start = i  # inclusive
                    break

            index_content_end = index_etag_start  # exclusive

            stag = xml[index_stag_start: index_stag_end]
            content = xml[index_content_start: index_content_end]
            etag = xml[index_etag_start: index_etag_end]

            return stag, content, etag

        def content_blocks(content):
            """Return a list of xml blocks which appear in the content
            Assumptions:
                - content contains at least 1 xml element i.e. <>...<>
                - content does not contain any self-closing xml block
            """
            content = content.strip()
            if not(content.startswith('<') and content.endswith('>')):
                return []

            length = len(content)

            # list of tuple (start_index, end_index)
            # both start_index and end_index are inclusive
            start_end_indices = []
            i = -1
            while i < length-1:
                i += 1
                if content[i] == '<':
                    start_index = i
                    end_index = Utils.end_index(content, start_index)
                    start_end_indices.append((start_index, end_index))
                    i = end_index

            xmls = [content[s:e+1] for (s, e) in start_end_indices]
            return xmls

        def is_content_plain_str(content):
            cs = content.strip()
            return not (cs.startswith('<') and cs.endswith('>'))

        def indent_block(block, idtn_space=2, idtn_level=1):
            """Shift whole block by given indentation level to the right"""
            ind = ' ' * idtn_space * idtn_level
            lines = block.split('\n')
            lines = [f'{ind}{x}' for x in lines]
            block = '\n'.join(lines)
            return block

        def preetify_xml_helper(xml, idtn_space):
            stag, content, etag = break_xml_into_tags_and_content(xml)

            # base case
            if is_content_plain_str(content):
                return xml.strip()

            else:  # content contains one or more xml blocks
                cbs = content_blocks(content)
                preetified_xml = stag
                for cb in cbs:
                    pcb = preetify_xml_helper(cb, idtn_space)
                    pcb = indent_block(pcb, idtn_space, 1)
                    preetified_xml += f'\n{pcb}'
                preetified_xml += f'\n{etag}'
                return preetified_xml

        xml = Utils.transform_self_closing_tag(xml)
        return preetify_xml_helper(xml, idtn_space=idtn_space)
