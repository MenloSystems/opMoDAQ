
import json
import sys

version_json = '''
{
 "dirty": false,
 "error": null,
 "version": "0.1.0"
}
'''

def get_versions():
    return json.loads(version_json)
