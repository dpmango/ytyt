import sys
import time

import tb as traceback


class ConsoleOutput:
    encoding = 'utf-8'

    def __init__(self, doc, console_id):
        self.cons = doc[console_id]
        self.buf = ''

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ''

    def __len__(self):
        return len(self.buf)


class EditorCodeBlocks:

    def __init__(self, doc, window):
        self.doc = doc
        self.window = window
        self.editor_class_name = 'editor__block'

    def declare(self):
        editors = self.doc.getElementsByClassName(self.editor_class_name)
        if len(editors) == 0:
            return None

        for editor in editors:
            unique_id = self.get_unique_id(editor.id)

            self.set_options_editor_by_id(unique_id)
            self.bind_click_to_run_id(unique_id, self._run)

    def set_options_editor_by_id(self, unique_id):
        ace_editor = self.get_ace_editor_by_id(unique_id)
        ace_editor.setTheme('ace/theme/solarized_light')
        ace_editor.session.setMode('ace/mode/python')

        ace_editor.setOptions({
            'enableLiveAutocompletion': True,
            'highlightActiveLine': False,
            'highlightSelectedWord': True
        })

    def bind_click_to_run_id(self, unique_id, func):
        self.doc['run__%s' % unique_id].bind('click', func)

    def _run(self, event):
        unique_id = self.get_unique_id(event.target.id)
        ace_editor = self.get_ace_editor_by_id(unique_id)

        self.clean_console_by_id(unique_id)
        self.change_stdout_by_id(unique_id)

        src = ace_editor.getValue()
        time_start = time.perf_counter()

        try:
            ns = {'__name__': '__main__'}
            exec(src, ns)
            state = 1
        except Exception:
            traceback.print_exc(file=sys.stderr)
            state = 0

        sys.stdout.flush()
        print('<completed in %6.2f ms>' % ((time.perf_counter() - time_start) * 1000.0))
        return state

    def change_stdout_by_id(self, unique_id):
        console_output = ConsoleOutput(doc=self.doc, console_id='console__%s' % unique_id)
        sys.stdout = console_output
        sys.stderr = console_output

    def clean_console_by_id(self, unique_id):
        self.doc['console__%s' % unique_id].value = ''

    def get_ace_editor_by_id(self, unique_id):
        return self.window.ace.edit('editor__%s' % unique_id)

    def get_unique_id(self, string):
        return string.split('__')[-1]
