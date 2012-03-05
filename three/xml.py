"""
Convert XML to a Python dictionary. Originally from:
http://code.activestate.com/recipes/578017/
"""

import re

try:
    # lxml ftw
    from lxml import etree
except ImportError:
    try:
        # Python 2.5+
        import xml.etree.cElementTree as etree
    except ImportError:
        # Python 2.5+
        import xml.etree.ElementTree as etree


class ElementList(list):
    """Configure an XML element structure into a list of dictionaries."""
    def __init__(self, a_list):
        for element in a_list:
            if element is not None:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XML(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(ElementList(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XML(dict):
    """
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XML(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XML(root)

    And then use xmldict for what it is... a dict.
    """
    def __init__(self, parent_element):
        is_unicode = isinstance(parent_element, unicode)
        is_string = isinstance(parent_element, str)
        if is_unicode or is_string:
            # Remove the XML prologue tag.
            xml_string = re.sub('<\?xml.*\?>', '', parent_element)
            xml_string = xml_string.strip('\n')
            parent_element = etree.fromstring(xml_string)
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            length = len(element)
            if length:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if length == 1 or element[0].tag != element[1].tag:
                    dictionary = XML(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    dictionary = {element[0].tag: ElementList(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    dictionary.update(dict(element.items()))
                self.update({element.tag: dictionary})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
