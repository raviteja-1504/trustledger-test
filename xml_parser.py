"""
XML parser with intentional XXE vulnerability for SAST testing.
"""

import xml.etree.ElementTree as ET
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import lxml.etree

# VULNERABILITY: XML External Entity (XXE) processing enabled
def parse_xml_xxe(xml_string):
    """Parse XML with external entity expansion enabled."""
    parser = make_parser()
    parser.setFeature("http://xml.org/sax/features/external-general-entities", True)
    parser.setFeature("http://xml.org/sax/features/external-parameter-entities", True)

    handler = ContentHandler()
    parser.setContentHandler(handler)
    parser.parseString(xml_string)
    return handler

# VULNERABILITY: lxml with no_ent=False (allowing entities)
def parse_with_lxml(xml_string):
    """Parse XML using lxml with entity expansion."""
    parser = lxml.etree.XMLParser(resolve_entities=True)
    root = lxml.etree.fromstring(xml_string, parser=parser)
    return lxml.etree.tostring(root)

# VULNERABILITY: ElementTree with entity expansion (if vulnerable version)
def parse_with_elementtree(xml_string):
    """Parse XML using ElementTree."""
    root = ET.fromstring(xml_string)
    return ET.tostring(root)

def process_user_xml():
    """Process user-supplied XML without validation."""
    import sys
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
        with open(xml_file, 'r') as f:
            xml_data = f.read()
        return parse_with_lxml(xml_data)
    return None