<template>
  <client-only>
    <div class="brython">
      <div :id="`container__${id}`" class="brython__editor">
        <div class="brython__actions">
          <button :id="`run__${id}`" class="brython__run">▶</button>
          <button :id="`show_console__${id}`" class="brython__show_console">Python</button>
        </div>

        <div class="brython__main">
          <div :id="`editor__${id}`" class="brython__editor-main"></div>
          <div class="brython__console">
            <textarea :id="`console__${id}`" readonly autocomplete="off"></textarea>
          </div>
        </div>
      </div>

      <script :id="`tests_editor__${id}`" type="text/python3">
        import sys
        import time
        import binascii

        import tb as traceback
        import javascript

        from browser import document as doc, window, alert, bind, html
        from browser.widgets import dialog

        has_ace = True
        try:
            editor = window.ace.edit("editor_{{id}}")
            editor.setTheme("ace/theme/solarized_light")
            editor.session.setMode("ace/mode/python")
            editor.focus()

            editor.setOptions({
             'enableLiveAutocompletion': True,
             'highlightActiveLine': False,
             'highlightSelectedWord': True
            })
        except:
            editor = html.TEXTAREA(rows=20, cols=70)
            doc["editor_{{id}}"] <= editor
            def get_value(): return editor.value
            def set_value(x): editor.value = x
            editor.getValue = get_value
            editor.setValue = set_value
            has_ace = False

        if hasattr(window, 'localStorage'):
            from browser.local_storage import storage
        else:
            storage = None

        def reset_src():
            if "code" in doc.query:
                code = doc.query.getlist("code")[0]
                editor.setValue(code)
            else:
                if storage is not None and "py_src" in storage:
                    editor.setValue(storage["py_src"])
                else:
                    editor.setValue('for i in range(10):\n\tprint(i)')
            editor.scrollToRow(0)
            editor.gotoLine(0)

        def reset_src_area():
            if storage and "py_src" in storage:
                editor.value = storage["py_src"]
            else:
                editor.value = 'for i in range(10):\n\tprint(i)'


        class cOutput:
            encoding = 'utf-8'

            def __init__(self):
                self.cons = doc["console_{{id}}"]
                self.buf = ''

            def write(self, data):
                self.buf += str(data)

            def flush(self):
                self.cons.value += self.buf
                self.buf = ''

            def __len__(self):
                return len(self.buf)

        if "console" in doc:
            cOut = cOutput()
            sys.stdout = cOut
            sys.stderr = cOut

        output = ''

        def show_console(ev):
            doc["console_{{id}}"].value = output
            doc["console_{{id}}"].cols = 60

        # load a Python script
        def load_script(evt):
            _name = evt.target.value + '?foo=%s' % time.time()
            editor.setValue(open(_name).read())

        # run a script, in global namespace if in_globals is True
        def run(*args):
            global output
            doc["console_{{id}}"].value = ''
            src = editor.getValue()
            if storage is not None:
               storage["py_src"] = src

            t0 = time.perf_counter()
            try:
                ns = {'__name__':'__main__'}
                exec(src, ns)
                state = 1
            except Exception as exc:
                traceback.print_exc(file=sys.stderr)
                state = 0
            sys.stdout.flush()
            output = doc["console_{{id}}"].value

            return state

        if has_ace:
            reset_src()
        else:
            reset_src_area()

        doc['run_{{id}}'].bind('click',lambda *args: run())
        doc['show_console_{{id}}'].bind('click', show_console)
      </script>
    </div>
  </client-only>
</template>

<script>
export default {
  props: {
    id: String,
  },
  mounted() {
    // TODO add method aka ready
    // setTimeout(() => {
    //   this.$refs.iframe.contentWindow.document.addEventListener('view.updated', () => {
    //     window.resizeIframe(this.$refs.iframe);
    //   });
    // }, 500);
    // window.resizeIframe = (obj) => {
    //   obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
    // };
  },
};
</script>

<style lang="scss" scoped>
.brython {
  position: relative;

  &__editor {
    position: relative;
    height: 100%;
    max-height: 600px;
    display: flex;
    flex-direction: column;
  }

  &__actions {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    background: #f3f3f3;
    padding: 2px 8px;
    border-bottom: 1px solid #c4c4c4;
  }

  &__main {
    flex: 1 1 auto;
    min-height: 1px;
    display: flex;
    flex-direction: column;
  }

  &__editor-main {
    flex: 0 0 auto;
    width: 100%;
    min-height: 60px;
    max-height: 400px;
  }

  &__console {
    position: relative;
    z-index: 2;
    flex: 1 1 auto;
    height: 100%;
    min-height: 1px;
    font-size: 0;
    overflow-y: auto;
    &::-webkit-scrollbar {
      width: 7px;
    }
    &::-webkit-scrollbar-track {
      border-radius: 0;
      background: #0a090c;
      box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    }
    &::-webkit-scrollbar-thumb {
      background: #939598;
      border-radius: 4px;
    }
    textarea {
      -webkit-appearance: none;
      width: 100%;
      height: auto;
      margin: 0;
      padding: 12px;
      font-size: 13px;
      border: 0;
      float: none;
      background-color: #0a090c;
      box-shadow: none;
      color: white;
      border-radius: 0;
      resize: none;
      &:focus,
      &:active {
        outline: none;
      }
    }
  }

  &__run {
    color: green;
    border: 0;
    background: transparent;
    cursor: pointer;
    font-size: 20px;
    padding: 5px;
  }
}
</style>
