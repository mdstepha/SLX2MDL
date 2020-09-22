#!/usr/bin/python3

import sys
import os
import shutil
import zipfile
import argparse
import datetime 
# from xml.dom import minidom


class Utils:

    # key: XmlElement
    # value: ObjectID in mdl
    _object_id_dict = {}

    @classmethod
    def clear_ids(cls):
        """Clear all entries in cls._object_id_dict.
        Call this method from Transformer.initialize() when operating in 'batch' mode
        so that all previous ids, if any, are cleared. """
        cls._object_id_dict = {}

    @classmethod
    def object_idmdl_by_xml_element(cls, xml_element):
        """Return object id 
        Args: 
            xml_element(an object of a class that inherits XmlElement)
        """
        # Not all objects that inherit XmlElement qualify to have an objectID.
        # Only those classes which may appear as 'Object' in the mdl format
        # are qualified to have an object ID.

        assert xml_element.tag in [
            'Object',
            'Mask',
            'MaskDefaults',
            'MaskParameter',
            'DialogControl',
        ]

        key = id(xml_element)
        try:
            return cls._object_id_dict[key]
        except KeyError:
            ids = cls._object_id_dict.values()
            ids = [int(x) for x in ids]
            max_id = max(ids) if ids else 0  # because ids is initially empty
            id_ = str(max_id + 1)
            cls._object_id_dict[key] = id_
            return id_

    @classmethod
    def parse_and_verify_args(cls):
        """Return command line args in a dict. 
        'mode' will be set to 'single' if the user does not provide this argument
        Raise error if provided arguments are invalid. 
        """
        # parse args
        parser = argparse.ArgumentParser()
        parser.add_argument('--mode')           # 'single'/'batch'
        parser.add_argument('--slx-filepath')   # absolute/relative filepath of slx file (relevant when mode = 'single')
        parser.add_argument('--slx-dirpath')    # absolute/relative filepath of slx directory (relevant when mode = 'batch')        
        parser.add_argument('--mdl-filepath')
        
        # if mode is 'batch' and conversion fails for any slx file, 
        # this argument controls whether to continue with the conversion of other slx files
        # useful during development phase 
        parser.add_argument('--exit-on-failure')    # 'yes'/'no' (default: 'no')
        
        # if report-performance is set to 'yes', 
        # number of lines in output mdl file, and 
        # time taken for conversion will be output, as well 
        parser.add_argument('--report-performance')    # 'yes'/'no' (default: 'no')

        # if devt-mode is set to 'yes', 
        # there will be some useful files (for debugging) in current and working directory.
        # otherwise these files either not be created at all, or deleted after the transformation completes or throws exception. 
        parser.add_argument('--devt-mode')  # 'yes'/'no' (default: 'no')

        # if dash (-) is present in the input argument,
        # it is automatically converted to underscore.
        # eg. slx-filepath --> slx_filepath
        args = parser.parse_args()
        args = vars(args)  # argparse.Namespace --> dict

        # now, verify args

        # mode
        if args['mode'] is None:
            args['mode'] = 'single'
        # converting single file vs. converting all files in a folder
        assert args['mode'] in ['single', 'batch']

        args['exit_on_failure'] = True if args['exit_on_failure'] == 'yes' else False 
        args['report_performance'] = True if args['report_performance'] == 'yes' else False 
        args['devt_mode'] = True if args['devt_mode'] == 'yes' else False 

        print()
        if args['mode'] == 'single':

            if not args['slx_filepath']:
                raise Exception(f"Missing argument 'slx-filepath' for mode 'single'")
            if not os.path.exists(args['slx_filepath']):
                raise Exception(f"Invalid slx-filepath: '{args['slx_filepath']}'")

            if not args['mdl_filepath']:
                print(f"Argument 'mdl-filepath' was not provided. Default path (see below) will be used.")

        else:
            if not args['slx_dirpath']:
                raise Exception(f"Missing argument 'slx-dirpath' for mode 'batch'")
            if not os.path.exists(args['slx_dirpath']):
                raise Exception(f"Invalid slx-dirpath: '{args['slx_dirpath']}'")

        return args

    @classmethod
    def create_file(cls, filepath):
        """Create file if it does not exist already. 
        Parent directory is created if it does not exist already.
        filepath may be relative or absolute."""
        if not os.path.exists(filepath):
            # convert to absolute path so that dirpath is guarranted
            # to be non-empty
            filepath = os.path.abspath(filepath)
            dirpath = os.path.dirname(filepath)
            # need to make sure directory exists before creating file
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            open(filepath, 'w').close()  # create file

    @classmethod
    def create_dirpath(cls, dirpath):
        """Create directory if it does not exist already. 
        Parent directory is created if it does not exist already.
        dirpath may be relative or absolute."""
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    @classmethod
    def remove_file(cls, filepath):
        """Remove a file if it exists. 
        filepath may be relative or absolute"""
        if os.path.exists(filepath):
            os.remove(filepath)

    @classmethod
    def remove_dirpath(cls, dirpath):
        """Remove directory if it exists. 
        dirpath may be relative or absolute"""
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)

    @classmethod
    def copy_file(cls, srcpath, dstpath, ignore_same_file_error=False):
        try:
            shutil.copyfile(srcpath, dstpath)
        except shutil.SameFileError:
            if not ignore_same_file_error:
                raise

    @classmethod
    def uncomment_xml(cls, xml):
        """Remove all xml comments from the input xml str"""
        indices = []  # tuple of (start_index, end_index)
        length = len(xml)
        i = -1
        while i < length:
            i += 1
            if xml[i:i+4] == '<!--':
                index_comment_start = i
                j = i + 4
                while True:
                    j += 1
                    if xml[j:j+3] == '-->':
                        index_comment_end = j+3  # exclusive
                        indices.append(
                            (index_comment_start, index_comment_end))
                        i = j + 3
                        break

        res = xml
        for s, e in indices:
            comment = xml[s:e]
            res = res.replace(comment, '')
        return res

    @classmethod
    def uncomment_xml_file(cls, input_filepath, output_filepath):
        """input_filepath and output_filepath can be same"""
        with open(input_filepath) as rfile:
            str_ = rfile.read()
            str_ = Utils.uncomment_xml(str_)
        with open(output_filepath, 'w') as wfile:
            wfile.write(str_)

    @classmethod
    def preetify_mdl_file(cls, input_filepath, output_filepath):
        """input_filepath and output filepath can be same"""
        os.system(f"txl {input_filepath} preetify-mdl.txl > {output_filepath}")

    @classmethod
    def transform_self_closing_tag(cls, xml):
        """Transform self-closing tag, if any, to non-self-closing tag"""

        def transform_first_self_closing_tag(xml):
            """Transform only the first self_closing tag. All occurrences of the
            first self-closing tag are transformed"""

            len_xml = len(xml)
            found = False
            i = 0
            while i < len_xml - 1:
                i += 1
                if xml[i:i+2] == '/>':
                    found = True
                    j = i
                    while True:
                        j -= 1
                        if xml[j] == '<':
                            k = j
                            while True:
                                k += 1
                                if xml[k] in [' ', '/']:
                                    tag_name = xml[j+1:k]
                                    break
                            break
                    break

            if found:
                self_closing_tag = xml[j:i+2]
                non_self_closing_tag = f"{self_closing_tag[0:-2]}></{tag_name}>"

                xml = xml.replace(self_closing_tag, non_self_closing_tag)
            return xml

        xml = xml.strip()
        i = 0
        while True:
            i += 1
            xml_transformed = transform_first_self_closing_tag(xml)
            if xml_transformed == xml:
                return xml
            xml = xml_transformed

    # @classmethod
    # def preetify_xml(cls, xml, no_self_closing_tags=False):
    #     dom = minidom.parseString(xml)
    #     xml = dom.toprettyxml()
    #     with open('___tempfile___', 'w') as file:
    #         file.write(xml)
    #     lines = []
    #     with open('___tempfile___', 'r') as file:
    #         for line in file:
    #             line = line.rstrip()
    #             if line:
    #                 lines.append(line)
    #     os.remove('___tempfile___')
    #     # dom.topreetyxml adds title line, which we want to avoid
    #     xml = '\n'.join(lines[1:])
    #     # revert undesired replacements introduced by the python library
    #     replacements = {
    #         # "'" : '&apos;',
    #     }

    #     for k, v in replacements.items():
    #         xml = xml.replace(k, v)

    #     if no_self_closing_tags:
    #         xml = Utils.transform_self_closing_tag(xml)

    #     return xml

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

    @classmethod
    def tag(cls, xml):
        """Return the tag's name of given xml string.
        Return None if no match found."""
        xml = Utils.transform_self_closing_tag(xml)
        xml = xml.strip()

        global ALL_TAGS
        for tag in ALL_TAGS:
            if xml.endswith(f"</{tag}>"):
                return tag

    @classmethod
    def end_index(cls, xml, start_index):
        """Return the last index of the tag

        DOES NOT SUPPORT SELF-CLOSING TAGS

        Parameters:
        xml (string)        : xml string
        start_index (int)   : index of first character i.e. '<' of starting tag

        Returns:
        (int) : index (NOT exclusive) of last character i.e. '>' of ending tag
        """

        # find tag's name
        i = start_index
        while True:
            i += 1
            if xml[i] in [' ', '>']:
                tag_name = xml[start_index + 1: i]
                break

        start_pattern = f'<{tag_name}'
        end_pattern = f'</{tag_name}>'

        len_start_pattern = len(start_pattern)
        len_end_pattern = len(end_pattern)
        len_xml = len(xml)

        stack = ['s']
        i = start_index
        while i < len_xml - len_end_pattern:
            i += 1

            # the second condition makes sure that if an inner tag begins with the same
            # string pattern as an outer tag, the inner tag is not falsely matched to
            # the start_pattern
            if xml[i: i + len_start_pattern] == start_pattern and xml[i + len_start_pattern] in [' ', '>']:
                stack.append('s')

            if xml[i: i + len_end_pattern] == end_pattern:
                stack.append('e')

            if len(stack) > 1 and stack[-1] == 'e' and stack[-2] == 's':
                stack = stack[0: -2]  # remove last 2 entries

            if len(stack) == 0:
                return i + len_end_pattern - 1

    @classmethod
    def disect_xml_str(cls, xml):
        """Return (tagname(str), list_of_XmlAttrs, content(str))
        Args: 
            xml(str)
        """
        xml = xml.strip()
        assert xml.startswith('<') and xml.endswith('>')

        i = 0
        index_tag_start = 1
        while True:
            i += 1
            if xml[i] in [' ', '>']:
                index_tag_end = i  # exclusive
                if xml[i] == '>':
                    attrless = True
                else:
                    attrless = False
                break

        xml_attrs = []
        if not attrless:
            nquote = 0
            i -= 1
            while True:
                i += 1
                if xml[i] == '>':  # end of attrs
                    break

                if xml[i] == ' ':
                    j = i
                    while True:
                        j += 1
                        if xml[j] != ' ':
                            index_attrname_start = j
                            break

                if xml[i] == '=':
                    index_attrname_end = i  # exclusive

                    j = i
                    while True:
                        j += 1
                        if xml[j] == '"':               # starting quote of an attribute's value
                            index_attrval_start = j + 1  # not including "
                            k = j
                            while True:
                                k += 1
                                # k will eventually have corresponding ending quote's index
                                if xml[k] == '"':
                                    index_attrval_end = k

                                    attrname = xml[index_attrname_start: index_attrname_end]
                                    attrval = xml[index_attrval_start: index_attrval_end]
                                    xml_attr = XmlAttr(attrname, attrval)
                                    xml_attrs.append(xml_attr)

                                    i = k
                                    break
                            break

        index_content_start = i + 1
        i = len(xml)
        while True:
            i -= 1
            if xml[i] == '<':
                index_content_end = i  # exclusive
                break

        tag = xml[index_tag_start: index_tag_end]
        content = xml[index_content_start: index_content_end]

        return tag, xml_attrs, content

    @classmethod
    def content_elements(cls, content):
        """Return a list of xml blocks (strs) which appear in the content (str)
        Assumptions:
            - content contains at least 1 xml element i.e. <>...<>
            - content does not contain any self-closing xml elements

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

    @classmethod
    def str_contents_multiline_to_singleline(cls, input_filepath, output_filepath):
        """COMBINE MULTI-LINE STRINGS INTO SINGLE-LINE STRINGS CONCATENATED BY '&#xA;' IF THESE STRINGS APPEAR AS THE CONTENT OF THE LISTED TAGS

        input_filepath and output_filepath can be same.

        ASSUMPTIONS: 
        - input_file contains no xml comments 

        We are using '&#xA' rather than '\n', to concatenate lines because
        1. '\n' changed to '\\n' by another method i.e.
           str_content_replacements() which is called after this method. This was observed to introduce errors in the model
           (dma/ex_bus_to_vector).
           So, we cannot use '\n' to concatenate lines.
        2. slx format also uses '&#xA;' to represent linebreaks (this is
           standard xml encoding).
        """
        tags = [
            'P',
            'Description',
            'Help',
            'Display',          # first found in powerwindow05
            'Initialization',   # first found in powerwindow05
            'Callback',         # first found in applications/aero_dap3dof
        ]

        # for any tag, start patterns can be of 2 types.
        # eg for 'P', they may be either '<P>' or '<P '
        # This is needed to avoid matching other starting tags starting with
        # these tags, eg: <Port> matchies <P> otherwise
        start_patterns = [f'<{x}>' for x in tags] + [f'<{x} ' for x in tags]
        sp_ep = {}
        for sp in start_patterns:
            sp_ep[sp] = f'</{sp[1:-1]}>'

        with open(input_filepath) as file:
            lines = file.readlines()

        writelines = []
        nlines = len(lines)
        i = -1
        while i < nlines - 1:
            i += 1
            line = lines[i]
            ls = line.strip()
            for sp, ep in sp_ep.items():
                # cannot just check if ls.endswith(ep) because the line might
                # end in a comment too while still having a multi line string content

                if ls.startswith(sp) and not ep in line and not '/>' in line:
                    while True:
                        # remove the nextline char at the end of the line
                        # IMP: cannot use "line = line.rstrip()" because that
                        # would strip away any trailing whitespace character
                        # as well along with the nextline character. This would
                        # then introduce errors -- such as invalid library block --
                        # in the output mdl file.
                        line = line[:-1]
                        i += 1
                        nextline = lines[i]
                        line += '&#xA;' + nextline
                        nrs = nextline.rstrip()
                        if ep in line or '/>' in line:
                            break
                    break
            writelines.append(line)

        with open(output_filepath, 'w') as file:
            for line in writelines:
                file.write(line)

    @classmethod
    def replacements4mdl(cls, mdl):
        """Make necessary requirements for mdl format.
        This transformation should be applied at the very end of the pipeline
        i.e. just before returning the generated mdl string. 
        Otherwise, these replacements will introduce unintended changes in the
        xml string (eg. '&lt' changes to '<' as a result xml parsing is affected
        producing errorneous results or raising exception.
        """

        # TODO: update this list incrementally
        replacements = {
            '&lt;': '<',
            '&gt;': '>',
            '&apos;': "'",
            '&#xA;': '\\n',
            '&amp;': '&',
            # IMPORTANT: the replacing character is not a 'space' character.
            # It is some special character that looks like a whitespace;
            # first found in AccelerationUnits (powerwindowlibphys)
            # when its raw value is printed as print(repr('')), this outputs \x1a 
            # (the whitespace-like character is inside the quotes) 
            '�': '',
            '&quot;': '\\"',
            # alpha and delta were discovered in 'selxAircraftExample'
            '\\alpha': '\\\\alpha',   #  \alpha --> \\alpha 
            '\\Alpha': '\\\\Alpha',   #  \alpha --> \\alpha 
            '\\beta': '\\\\beta', 
            '\\Beta': '\\\\Beta', 
            '\\gamma': '\\\\gamma', 
            '\\Gamma': '\\\\Gamma', 
            '\\delta': '\\\\delta', 
            '\\Delta': '\\\\Delta', 
            '\\epsilon': '\\\\epsilon', 
            '\\Epsilon': '\\\\Epsilon', 
            '\\zeta': '\\\\zeta', 
            '\\Zeta': '\\\\Zeta', 
            '\\eta': '\\\\eta', 
            '\\Eta': '\\\\Eta', 
            '\\theta': '\\\\theta', 
            '\\Theta': '\\\\Theta', 
            '\\iota': '\\\\iota', 
            '\\Iota': '\\\\Iota', 
            '\\kappa': '\\\\kappa', 
            '\\Kappa': '\\\\Kappa', 
            '\\lambda': '\\\\lambda', 
            '\\Lambda': '\\\\Lambda', 
            '\\mu': '\\\\mu', 
            '\\Mu': '\\\\Mu', 
            # 'nu' is commented out because it brought unintended changes: eg, \nusing --> \\nusing 
            # so, currently our transformation fails if model contains 'nu' character (rare case)
            # TODO: solve it 
            # '\\nu': '\\\\nu',   
            '\\Nu': '\\\\Nu',   
            '\\xi': '\\\\xi', 
            '\\Xi': '\\\\Xi', 
            '\\omikron': '\\\\omikron', 
            '\\Omikron': '\\\\Omikron', 
            '\\pi': '\\\\pi', 
            '\\Pi': '\\\\Pi', 
            '\\rho': '\\\\rho', 
            '\\Rho': '\\\\Rho', 
            '\\sigma': '\\\\sigma', 
            '\\Sigma': '\\\\Sigma', 
            '\\tau': '\\\\tau', 
            '\\Tau': '\\\\Tau', 
            '\\upsilon': '\\\\upsilon', 
            '\\Upsilon': '\\\\Upsilon', 
            '\\phi': '\\\\phi', 
            '\\Phi': '\\\\Phi', 
            '\\chi': '\\\\chi', 
            '\\Chi': '\\\\Chi', 
            '\\psi': '\\\\psi', 
            '\\Psi': '\\\\Psi', 
            '\\omega': '\\\\omega', 
            '\\Omega': '\\\\Omega', 
        }

        for k, v in replacements.items():
            mdl = mdl.replace(k, v)
        return mdl

    @classmethod
    def str_content_replacements(cls, content):
        """Make necessary requirements for the content of type 'str'.
        Args: 
            content(str); 
        """
        # IMPORTANT replacement that affect xml parsing such as '&gt;' --> '>'
        # are not made by this method

        replacements = {
            '\\n': '\\\\n',  # \n --> \\n   # first found in automotive/sldemo_wheelspeed_absbrake
            '\\t': '\\\\t',  # \t --> \\t   # first found in automotive/sldemo_wheelspeed_absbrake
        }

        for k, v in replacements.items():
            content = content.replace(k, v)
        return content

    @classmethod
    def remove_multiple_linegaps(cls, str_):
        """Returned string will not have 2 or more consecutive empty lines"""
        if not '\n\n\n' in str_:  # base condition
            return str_
        str_ = str_.replace('\n\n\n', '\n\n')
        return Utils.remove_multiple_linegaps(str_)

    @classmethod
    def remove_linegaps(cls, str_):
        """Returned string will not have any empty line"""
        if not '\n\n' in str_:  # base condition
            return str_
        str_ = str_.replace('\n\n', '\n')
        return Utils.remove_linegaps(str_)

    @classmethod
    def remove_multiple_linegaps_between_consecutive_closing_braces(cls, str_):
        """Returned string will not have an empty line between any 2 consecutive 
        closing braces i.e. }"""
        if not '}\n\n}' in str_:  # base condition
            return str_
        str_ = str_.replace('}\n\n}', '}\n}')
        return Utils.remove_multiple_linegaps_between_consecutive_closing_braces(str_)

    @classmethod
    def extract_first_tag(cls, xml, tag):
        """Return the first tag (<>...</>) as a string.
        If there is an inner tag inside the first tag, the outer tag (containing
        the inner tag) will be returned.
        Return None if no such tag is found

        Assumption:
        xml MUST NOT CONTAIN ANY SELF-CLOSING TAG

        Parameters:
        xml (string)   : xml string
        tag (string)   : tag to be found. eg. 'state'

        Returns:
        (string): entire tag (<>...</>)
        """

        stag = f"<{tag}"
        etag = f"</{tag}>"

        len_xml = len(xml)
        len_stag = len(stag)
        len_etag = len(etag)

        start_index = None
        end_index = None
        found = False

        # both insertion and removal from highest index
        # s : start
        # e : end
        tag_stack = []

        for i in range(0, len_xml - len_etag + 1):
            substr = xml[i: i + len_stag]
            if substr == stag:
                found = True
                tag_stack.append('s')

                if start_index == None:
                    start_index = i

            substr = xml[i: i + len_etag]
            if substr == etag:
                tag_stack.append('e')
                end_index = i + len_etag

            if found:
                if len(tag_stack) > 1 and tag_stack[-1] == 'e' and tag_stack[-2] == 's':
                    tag_stack = tag_stack[0: -2]  # remove last 2 entires
                if len(tag_stack) == 0:
                    return xml[start_index: end_index]

    @classmethod
    def extract_outer_tags(cls, xml, tag, ignore_inside=None):
        """Return a list of matching tags.
        - If there is an inner tag inside the first tag, the outer tag (containing
          the inner tag) will be added to the list, the inner tag will NOT be added
          separately.

        - Tags (in the returned list) will appear in the same order as they appear
          in the xml file

        Assumption:
        - xml MUST NOT CONTAIN ANY SELF-CLOSING TAG

        Args:
            xml (str): xml string
            tag (str): tag to be found. eg. 'state'
            ignore_inside ([str]): list of tags. The tag element inside these tags
                will be ignored.

        Returns:
            [string]: list of entire tag (<>...</>). The list is empty if no match is found.
        """

        if ignore_inside is None:
            ignore_inside = []

        stag = f"<{tag}"
        etag = f"</{tag}>"

        len_xml = len(xml)
        len_stag = len(stag)
        len_etag = len(etag)

        tags = []
        start_index = None
        end_index = None
        found = False
        inside_ignored_tag = False

        # both insertion and removal from highest index
        # s : start
        # e : end
        tag_stack = []

        # for i in range(0, len_xml - len_etag + 1):
        i = -1
        while i < len_xml - len_etag + 1:
            i += 1

            for ignored_tag in ignore_inside:
                start_pattern = f'<{ignored_tag}'
                len_start_pattern = len(start_pattern)
                if xml[i: i + len_start_pattern] == start_pattern:
                    # skip the entire tag
                    i = Utils.end_index(xml, i)

            if xml[i: i + len_stag] == stag:
                found = True

                # update start_index only if tag_stack is empty
                # i.e. all previously entered tags, if any, are exited.
                if len(tag_stack) == 0:
                    start_index = i
                tag_stack.append('s')

            if xml[i: i + len_etag] == etag:
                tag_stack.append('e')
                end_index = i + len_etag

            if found:
                if len(tag_stack) > 1 and tag_stack[-1] == 'e' and tag_stack[-2] == 's':
                    tag_stack = tag_stack[0: -2]  # remove last 2 entries
                if len(tag_stack) == 0:
                    tags.append(xml[start_index: end_index])
                    found = False

        return tags

    @classmethod
    def split_filepath(cls, filepath):
        """Return (dirpath, filename_without_extension, extension_with_dot)
        dirpath will be empty if filepath is relative and corresponds to a file
        in current directory"""
        dirpath, filename_with_ext = os.path.split(filepath)  # a/b/c/d.txt --> a/b/c, d.txt
        filename_without_ext, ext_with_dot = os.path.splitext(filename_with_ext)  # d.txt --> d, .txt
        return dirpath, filename_without_ext, ext_with_dot


    @classmethod 
    def log(cls, log_msg, log_filepath, write_mode):
        """Write log message to the file
        Args: 
            log_msg(str): log message 
            log_filepath(str): absolute path of the log file (will be created if does not exist already)
            write_mode(str): 'write'/'append'
        """
        assert write_mode in ['write', 'append']
        write_mode = 'w' if write_mode == 'write' else 'a'

        log_msg = f"\n\n\n-------------------------------------\n\nDate/time: {datetime.datetime.now()}\n\n" + log_msg

        with open(log_filepath, write_mode) as file: 
            file.write(log_msg)


class XmlAttr:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}={self.value}'


class XmlElement:
    """An XmlElement is either <tag>...</tag> or just any string, eg: 'abc' 
    In reality, a string without tag is not considered an XmlElement, but this model 
    treats such strings too as an XmlElement

    Attributes: 
        type(str): 'xml'/'str'
        strval(str):
        tag(str/None):
        xml_attrs([XmlAttr]/None):
        inner_xmls([XmlElement]/None): 
        content(str): 
        parent_xml(XmlElement)
    """

    def __init__(self, strval, parent_xml):
        """
        Args: 
            parent_xml(XmlElement): parent XmlElement, if any, else None 
        """
        self.parent_xml = parent_xml

        strval = Utils.transform_self_closing_tag(strval)
        strval_stripped = strval.strip()
        if strval_stripped.startswith('<') and strval_stripped.endswith('>'):
            self.type = 'xml'
            self.strval = strval_stripped
            tag, xml_attrs, content = Utils.disect_xml_str(strval)
            self.tag = tag
            self.attrs = xml_attrs
            content_striped = content.strip()

            if content_striped.startswith('<') and content_striped.endswith('>'):
                self.content = content_striped
                self.content_type = 'xml'
                content_elements = Utils.content_elements(content)  # [str]
                self.inner_xmls = [XmlElement(x, self)
                                   for x in content_elements]
            else:
                # if content is 'str' type:
                #  - don't strip leading/trailing spaces
                #  - make some replacements
                #     - replacements like \n --> \\n are made at this time
                #     - replacements like &gt; --> > are NOT made at this time.
                self.content = Utils.str_content_replacements(content)
                self.content_type = 'str'
                self.inner_xmls = [XmlElement(content, self)]
        else:
            self.type = 'str'
            # don't strip leading/trailing spaces for 'str' type element
            self.strval = strval
            self.attrs = None
            self.tag = None
            self.inner_xmls = []
            self.content_type = None
            self.content = None

    def attr_value_by_name(self, attrname):
        """Return the value (str) of attribute. 
        Return None if no such attribute exists"""
        for attr in self.attrs:
            if attr.name == attrname:
                return attr.value

    @property
    def inner_xmls_of_type_xml(self):
        return [x for x in self.inner_xmls if x.type == 'xml']

    @property
    def inner_xmls_of_type_str(self):
        return [x for x in self.inner_xmls if x.type == 'str']

    def __str__(self):
        return self.strval


class UtilsStfl:
    """Utility class for Stateflow"""

    _id_dict = {}

    @classmethod
    def clear_ids(cls):
        """Clear all entries in cls._id_dict.
        Call this method from Transformer.initialize() when operating in 'batch' mode
        so that all previous ids, if any, are cleared. """
        cls._id_dict = {}

    @classmethod
    def _get_idmdl(cls, idslx, ssid, idmdl_chart, create_if_needed=True):
        # ssid of elements from different <chart>s collide.
        # so, we need to include idmdl_chart in the key
        key = (idslx, ssid, idmdl_chart)

        try:
            return cls._id_dict[key]
        except KeyError:
            if create_if_needed:
                ids = cls._id_dict.values()
                ids = [int(x) for x in ids]
                max_id = max(ids) if ids else 0  # because ids is initially empty
                id = str(max_id + 1)
                cls._id_dict[key] = id
                return id
            return None

    @classmethod
    def idmdl_by_idslx(cls, idslx, create_if_needed=True):
        """Return idmdl for this element.
        The id will be generated, if this method
        is called with these arguments for the first time.

        Call this method to get idmdl for ['chart', 'instance', 'machine', 'target']

        Args: 
            idslx(str): id in slx version 
            created_if_needed(bool): If this is set to true, new id will be generated in 
                case idmdl for given idslx doesnot exist already. Otherwise, None will be 
                returned in such case. 
        """
        assert idslx
        return cls._get_idmdl(idslx=idslx, ssid=None, idmdl_chart=None, create_if_needed=create_if_needed)

    @classmethod
    def idmdl_by_ssid(cls, ssid, idmdl_chart, create_if_needed=True):
        """Return idmdl for this element.
        The id will be generated, if this method
        is called with these arguments for the first time.

        Call this method to get idmdl for ['data', 'event', 'junction', 'state', 'transition']

        Args: 
            ssid(str): ssid of the element 
            idmdl_chart(str): idmdl of parent chart. This is needed for some 
                elements, because SSIDs can collide between the children
                (for exampe, <state>s of two different <chart>s 
            created_if_needed(bool): If this is set to true, new id will be generated in 
                case idmdl for given idslx doesnot exist already. Otherwise, None will be 
                returned in such case. 
        """
        assert ssid
        assert idmdl_chart
        return cls._get_idmdl(idslx=None, ssid=ssid, idmdl_chart=idmdl_chart, create_if_needed=create_if_needed)


if __name__ == '__main__':
    pass
