#!/usr/bin/python3

from commons import *


def inner_mdls(content):
    """Split the content into inner mdls."""
    length = len(content)
    brace_stack = []
    mdls = []
    start_index = 0
    i = -1
    while i < length - 1:
        i += 1
        if content[i] == '{':
            brace_stack.append('{')
            j = i
            while True:
                j += 1
                if content[j] == '{':
                    brace_stack.append('{')
                if content[j] == '}':
                    brace_stack.append('}')
                if len(brace_stack) > 1 and brace_stack[-1] == '}' and brace_stack[-2] == '{':
                    brace_stack = brace_stack[:-2]
                if len(brace_stack) == 0:  # reached the closing brace of an inner mdl
                    mdls.append(content[start_index: j + 1])
                    start_index = j
                    k = j
                    while True:
                        k += 1
                        if content[k] == '\n':
                            i = k
                            break
                    break

        elif content[i] == '\n':
            mdls.append(content[start_index: i+1])
            start_index = i

    mdls = [m for m in mdls if m.strip()]
    mdls = [m.strip() for m in mdls] 
    return mdls 


def indent(content, indentation_spaces=4):
    ind = ' ' * indentation_spaces
    lines = content.split('\n')
    lines = [ind + line for line in lines]
    content = '\n'.join(lines)
    return content



def preetify_mdl(mdl):



    bak = mdl
    mdl = mdl.strip()
    tokens = mdl.split()

    # base case
    if len(tokens) > 1 and tokens[1] != '{':
        print(f'----------------------- unbraced content  {mdl}')
        return bak

    print(f'------------------------- braced content')
    element_name = tokens[0]
    content = mdl[len(element_name) + 2: -1]  # excludes element_name and braces

    imdls = inner_mdls(content)

    # for x in imdls: 
    #     print('-----------')
    #     print(x)

    imdls = [preetify_mdl(x) for x in imdls]
    imdls = [indent(x) for x in imdls]
    content = '\n'.join(imdls)
    # content = indent(content)
    
    mdl = element_name + ' {\n' + content + '\n}'
    return mdl 


with open('ip.mdl') as file:
    mdl = file.read()

mdl = preetify_mdl(mdl)
print(mdl)


