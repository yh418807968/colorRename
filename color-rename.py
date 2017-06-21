
import sublime
import sublime_plugin
import re
import time
import os
import json
import os.path

scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, 'data.json')
testFile=open(filename)
data=json.load(testFile)


SETTINGS = {}
lastCompletion = {"needFix": False, "value": None, "region": None}


def plugin_loaded():
    init_settings()

def init_settings():
    get_settings()
    sublime.load_settings('color-rename.sublime-settings').add_on_change('get_settings', get_settings)

def get_settings():
    settings = sublime.load_settings('color-rename.sublime-settings')
    # SETTINGS['fontsize'] = settings.get('fontsize', 16)
    # SETTINGS['precision'] = settings.get('precision', 8)
    SETTINGS['exts'] = settings.get('exts', [".css", ".scss", ".less", ".sass", ".styl"])
    # SETTINGS['leadingzero'] = settings.get('leadingzero', False)

def get_setting(view, key):
    return view.settings().get(key, SETTINGS[key]);

class CssRemCommand(sublime_plugin.EventListener):
    def on_text_command(self, view, name, args):
        # if name == 'commit_completion':
            view.run_command('')
        # return None

    def on_query_completions(self, view, prefix, locations):
        # print('color-rename start {0}, {1}'.format(prefix, locations))

        # only works on specific file types
        fileName, fileExtension = os.path.splitext(view.file_name())
        if not fileExtension.lower() in get_setting(view, 'exts'):
            return []

        # reset completion match
        lastCompletion["needFix"] = False
        location = locations[0]
        snippet = []

        # get rem match
        # match = re.compile("([\d.]+)f(x)?").match(prefix)
        match = re.compile("([a-fA-F1-9]{3,6})").match(prefix)
        if match:
            lineLocation = view.line(location)
            line = view.substr(sublime.Region(lineLocation.a, location))
            value = '#'+match.group(0)
            # value='123f'
            

            # # fix: values like `0.5px`
            # segmentStart = line.rfind(" ", 0, location)
            # if segmentStart == -1:
            #     segmentStart = 0
            # segmentStr = line[segmentStart:location]

            # segment = re.compile(value).search(segmentStr)
            # if segment:
            #     value = segment.group(0)
            #     start = lineLocation.a + segmentStart + 0 + segment.start(0)
            #     lastCompletion["needFix"] = True
            # else:
            #     start = location

            # remValue = round(float(value) / get_setting(view, 'fontsize'), get_setting(view, 'precision'))

            # # remove useless .0
            # intValue = int(remValue)
            # if intValue == remValue:
            #     remValue = intValue

            # strRem = str(remValue)
            rename = data[value]
            # # remove leadingzero
            # if (get_setting(view, 'leadingzero') == False) and (remValue < 1.0):
            #     strRem = strRem[1:]

            # # add rem unit unless value = 0
            # if remValue != 0:
            #     strRem += 'rem'
            # else:
            #     strRem = '0'

            # # save them for replace fix
            # lastCompletion["value"] = rename
            # lastCompletion["region"] = sublime.Region(start, location)
            commentStr = '';
            if (fileExtension.lower() in [".sass", ".scss", ".styl", ".less"]):
                commentStr = '; // ' + value + '';
            else:
                commentStr = '/*' + value + '*/';

            # set completion snippet
            # snippets += [(value + 'px -> ' +strRem+ '(' + str(get_setting(view, 'fontsize')) + 'px/rem)',strRem)]
            # snippets += [(value + 'px -> ' + strRem + '(keep px value)', strRem + commentStr)]
            snippet+= [[value +'\t'+'-> '+ rename +'(keep number value)', '\\'+rename[0] +rename[1:]+commentStr]]

        # print("color-rename: {0}".format(snippets))
        return snippet

# class ReplaceRemCommand(sublime_plugin.TextCommand):
#     def run(self, view, args):
#         needFix = lastCompletion["needFix"]
#         if needFix == True:
#             value = lastCompletion["value"]
#             region = lastCompletion["region"]
#             # print('replace: {0}, {1}'.format(value, region))
#             view.replace(region, value)
#             view.end_edit()
