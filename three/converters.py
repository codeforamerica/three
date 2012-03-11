"""
Convert XML to a Python dictionary.

Adapted from:  https://github.com/zachwill/xml2dict
"""

import re

try:
    # Try to use lxml if it's available.
    from lxml import etree
except ImportError:
    try:
        # Python 2.5+
        import xml.etree.cElementTree as etree
    except ImportError:
        # Python 2.5+
        import xml.etree.ElementTree as etree


def xml(data):
    """Turn XML into a dictionary."""
    converter = XML2Dict()
    if hasattr(data, 'read'):
        # Then it's a file.
        data = data.read()
    results = converter.fromstring(data)
    first_element = results.keys()[0]
    return results[first_element]


class XML2Dict(object):
    """Turn XML into a dictionary data structure."""

    def _parse_node(self, node):
        node_tree = {}
        if node.text and node.attrib:
            if node.tag in node.attrib:
                message = """Name conflict: Attribute name conflicts with tag
                name. Check the documentation."""
                raise ValueError(message)
            node.attrib.update({node.tag: node.text})
            node.text = ''
        # Save attrs and text. Fair warning, if there's a child node with
        # the same name as an attribute, values will become a list.
        if node.text and node.text.strip():
            node_tree = node.text
        else:
            for k, v in node.attrib.items():
                k, v = self._namespace_split(k, v)
                node_tree[k] = v
            # Save children.
            for child in node.getchildren():
                tag, tree = self._namespace_split(child.tag, self._parse_node(child))
                if tag not in node_tree:  # First encounter, store it in dict.
                    node_tree[tag] = tree
                    continue
                old = node_tree[tag]
                if not isinstance(old, list):
                    # Multiple encounters, change dict to a list
                    node_tree.pop(tag)
                    node_tree[tag] = [old]
                node_tree[tag].append(tree)  # Add the new one.
        return node_tree

    def _namespace_split(self, tag, value):
        """Split namespace tags."""
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            tag = result.groups(1)
            # value.namespace, tag = result.groups()
        return (tag, value)

    def parse(self, file):
        """Parse an XML file to a dict."""
        with open(file, 'r') as f:
            return self.fromstring(f.read())

    def fromstring(self, s):
        """Parse an XML string into a dict."""
        t = etree.fromstring(s)
        root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
        return {root_tag: root_tree}
