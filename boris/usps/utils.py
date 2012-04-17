"""
Utility functions for use in USPS app
"""
import urllib
try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET
    
def utf8urlencode(data):
    """
    utf8 URL encode the given dictionary's data
    
    @param data: a dictionary of data to be encoded
    @return: the dictionary data with values URL encoded
    """
    ret = dict()
    for key, value in data.iteritems():
        ret[key] = value.encode('utf8')
    return urllib.urlencode(ret)

def dicttoxml(dictionary, tagname, attributes=None):
    """
    Transform a dictionary to xml
    
    @todo: unit tests
    @param dictionary: a dictionary
    @param parent:  a parent node
    @return: XML serialization of the given dictionary
    """
    element = ET.Element(tagname)
    
    if attributes: #USPS likes things in a certain order!
        for key in attributes:
            value = dictionary.get(key, False)
            if type(value).__name__ == 'dict':
                elem = dicttoxml(value, key, attributes)
                element.append(elem)
            elif value != False:
                ET.SubElement(element, key).text = value
    else:
        for key, value in dictionary.iteritems():
            if type(value).__name__ == 'dict':
                elem = dicttoxml(value, key)
                element.append(elem)
            else:
                ET.SubElement(element, key).text = value
    return element

def xmltodict(element):
    """
    Transform an xml fragment into a python dictionary
    
    @todo: unit tests
    @param element: an XML fragment
    @return: a dictionary representation of an XML fragment
    """
    ret = dict()
    for item in element:
        if len(item) > 0:
            value = xmltodict(item)         
            if len(item.attrib.items()) > 0:
                for k, v in item.attrib.items():
                    value[k] = v
        elif len(item.attrib.items()) > 0:
            value = {'text': item.text}
            for k, v in item.attrib.items():
                    value[k] = v     
        else:
            value = item.text
            
        if item.tag in ret and type(ret[item.tag]).__name__ != 'list':
            old_value = ret.get(item.tag, None)
            ret[item.tag] = [old_value,value,]             
        elif item.tag in ret and type(ret[item.tag]).__name__ == 'list':
            ret[item.tag].append(value)
        else:
            ret[item.tag] = value
            
    return ret

