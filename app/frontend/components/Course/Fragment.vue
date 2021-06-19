/* eslint-disable vue/no-v-html */
<template>
  <div class="lesson">
    <div class="container">
      <div class="lesson__wrapper">
        <CourseLessonSidebar
          :progress="data.progress"
          :title="data.title"
          :current-section-index="currentSectionIndex"
          :sections-count="sectionsCount"
          :sections="sections"
          :active-section="activeSection"
          @setFragment="setFragment"
          @handleQuestionClick="handleQuestionClick"
        />

        <div ref="content" class="lesson__content">
          <div class="lesson__box">
            <template v-if="activeSection === 0">
              <h3 class="h3-title">У вас нет доступа к этому уроку</h3>
            </template>

            <template v-else-if="sections">
              <CourseLessonNavigation
                :title="data.title"
                :current-section-index="currentSectionIndex"
                :sections-count="sectionsCount"
                :is-prev-available="isPrevLessonAvailable"
                :is-next-available="isNextLessonAvailable"
                :set-next-lesson="setNextLesson"
                :set-prev-lesson="setPrevLesson"
              />

              <template v-if="fragmentVisible">
                <div
                  v-for="fragment in fragmentVisible"
                  :key="fragment.id"
                  class="lesson__section"
                  :class="[fragment.id === activeSection && 'is-active']"
                >
                  <div class="lesson__body markdown-body">
                    <span v-for="(block, idx) in fragmentContent(fragment.content)" :key="idx">
                      <UiBrython v-if="block.type === 'code'" :code="block.content" :ready="brythonReady" />
                      <span v-else class="lesson__body-text" v-html="block.content" />
                    </span>
                  </div>

                  <div class="lesson__actions">
                    <UiButton @click.prevent="setNextFragment">Продолжить</UiButton>
                    <UiButton v-if="user.dialog" theme="outline" @click="handleQuestionClick"> Задать вопрос </UiButton>
                  </div>
                </div>
              </template>

              <template v-else>
                <UiLoader :loading="true" theme="block" />
              </template>
            </template>

            <template v-else>
              <UiLoader :loading="true" theme="block" />
            </template>
          </div>
        </div>
      </div>
    </div>

    <template v-if="user.dialog">
      <ChatHome :is-mini="true" :is-mini-opened="isChatOpened" :handle-click-back-mini="handleClickBack" />
    </template>

    <script type="text/python3">
      from browser import document as doc, window
      from editor import EditorCodeBlocks

      EditorCodeBlocks(doc, window).declare()
    </script>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  props: {
    data: Object,
    requestFragment: Function,
  },
  data() {
    return {
      isChatOpened: false,
      activeSection: 0,
      brythonReady: false,
    };
  },

  computed: {
    sections() {
      return this.data.lesson_fragments;
    },
    sectionsCount() {
      return this.sections.length;
    },

    currentSectionIndex() {
      return this.sections.findIndex((s) => s.id === this.activeSection);
    },
    nextSectionId() {
      const section = this.sections[this.currentSectionIndex + 1];
      return section ? section.id : null;
    },
    prevSectionId() {
      const section = this.sections[this.currentSectionIndex - 1];
      return section ? section.id : null;
    },
    isNextAvailable() {
      return this.nextSectionId;
    },
    isPrevAvailable() {
      if (this.prevSectionId) {
        return this.prevSectionId;
      }
      return null;
    },
    isPrevLessonAvailable() {
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (lesson.prev.pk && [1, 2, 3].includes(lesson.prev.status)) {
        return 1;
      } else if (theme.prev.pk && [1, 2, 3].includes(theme.prev.status)) {
        return 1;
      }
      return null;
    },
    isNextLessonAvailable() {
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (lesson.next.pk && [1, 2, 3].includes(lesson.next.status)) {
        return 1;
      } else if (theme.next.pk && [1, 2, 3].includes(theme.next.status)) {
        return 1;
      }
      return null;
    },
    fragmentVisible() {
      return this.data.accessible_lesson_fragments;
    },
    ...mapGetters('auth', ['user']),
  },
  watch: {
    activeSection() {
      this.highlightSyntax();
    },
  },
  created() {
    // getting current user fragment from props
    const activeFragment = this.data.accessible_lesson_fragments.find((frag) => [1, 2].includes(frag.status));

    if (activeFragment) {
      this.activeSection = activeFragment.id;
    } else if (this.data.accessible_lesson_fragments.length) {
      this.activeSection = this.data.accessible_lesson_fragments[0].id;
    } else {
      this.activeSection = 0;
    }
  },
  mounted() {
    const scripts = [
      '/brython/src/brython_builtins.js',
      '/brython/src/version_info.js',
      '/brython/src/py2js.js',
      '/brython/src/loaders.js',
      '/brython/src/py_object.js',
      '/brython/src/py_type.js',
      '/brython/src/py_utils.js',
      '/brython/src/py_sort.js',
      '/brython/src/py_builtin_functions.js',
      '/brython/src/py_exceptions.js',
      '/brython/src/py_range_slice.js',
      '/brython/src/py_bytes.js',
      '/brython/src/py_set.js',
      '/brython/src/js_objects.js',
      '/brython/src/stdlib_paths.js',
      '/brython/src/py_import.js',
      '/brython/src/unicode_data.js',
      '/brython/src/py_string.js',
      '/brython/src/py_int.js',
      '/brython/src/py_long_int.js',
      '/brython/src/py_float.js',
      '/brython/src/py_complex.js',
      '/brython/src/py_dict.js',
      '/brython/src/py_list.js',
      '/brython/src/py_generator.js',
      '/brython/src/py_dom.js',
      '/brython/src/builtin_modules.js',
      // '/brython/src/brython.js',
      '/brython/src/brython_stdlib.js',
      // '/brython/ace/ace.js',
      // '/brython/ace/ext-language_tools.js',
      '/brython/codemirror/codemirror.js',
      '/brython/codemirror/runmode.js',
      '/brython/codemirror/colorize.js',
      '/brython/codemirror/mode/python/python.js',
    ];

    const loadScripts = (scripts) => {
      const script = scripts.shift();
      const el = document.createElement('script');

      document.head.append(el);

      el.onload = (script) => {
        if (scripts.length) {
          loadScripts(scripts);
        } else {
          document.body.classList.add('brython-ready');
          this.brythonReady = true;
          window.brython();
        }
      };

      el.src = script;
    };

    if (!document.body.classList.value.includes('brython-ready')) {
      loadScripts(scripts);
    } else {
      this.brythonReady = true;
      window.brython();
    }
  },
  methods: {
    fragmentContent(content) {
      // const test_content =
      //   '<h1 id="ytyt">Как работать с платформой YtYt?</h1>\n<p>Весь обучающий курс состоит из нескольких тем.<br/>\nКаждая тема - из нескольких уроков.<br/>\nКаждый урок - из нескольких блоков.  </p>\n<p>[Изображение]</p>\n<p>Уроки открываются по очереди - для получения доступа ко второму уроку вам необходимо полностью пройти первый.<br/>\nАналогично с темами - вторая тема откроется после того, как вы полностью пройдете все уроки из первой темы.  </p>\n<p>В конце каждого урока, в блоке “Практика”, вам нужно будет выполнить практическое задание и сдать его на проверку своему наставнику.<br/>\nНаставник в течение суток проверит его, укажет вам на ошибки и поможет разобраться в сложных моментах.  </p>\n<p>Доступ к следующему уроку вы получите сразу после сдачи задания на проверку.<br/>\nТо есть дожидаться ответа от наставника необязательно, можно сразу идти дальше.<br/>\nНо если в задании вы допустите много ошибок, то наставник может закрыть доступ к следующим урокам, пока вы не разберетесь с практикой.  </p>\n<h3 id="_2">Готовые примеры кода</h3>\n<p>В каждом уроке вы увидите вот такие элементы:  </p>\n<p>[brython-snippet]print(\'Привет, мир!\')[/brython-snippet]</p>\n<p>В них написан готовый программный код, который вы можете запустить нажатием на кнопку <code class="language-python">►</code>.<br/>\nРезультат выполнения кода отобразится сразу под этим элементом.  </p>\n<p>Вы можете самостоятельно вносить изменения в код и запускать его повторно.<br/>\nЭто позволит вам лучше разобраться в том, как работает написанный код.  </p>\n<p>Практические задания вы будете выполнять не в этих ячейках, а в более удобной среде разработки.<br/>\nПодробнее об этом вы узнаете в блоке “Практика” в конце этого урока.  </p>\n<h3 id="_3">Вопросы наставнику</h3>\n<p>С помощью кнопки “Задать вопрос” вы можете общаться со своим наставником.<br/>\nОн ответит на любые вопросы.  </p>\n<p>Но прежде, чем просить помощи, попробуйте решить проблему самостоятельно.<br/>\nПоиск информации и решений - это важная часть работы программиста.<br/>\nДаже разработчики с опытом 15+ лет постоянно что-то “гуглят” во время работы, изучают документацию и другие источники.  </p>\n<p>Тому, как правильно искать в сети ответы на вопросы, посвящен отдельный урок.<br/>\nНа нем будут показаны основные источники информации и примеры того, как правильно составлять запросы.<br/>\nНо если у вас все-таки не получится самостоятельно решить проблему - не стесняйтесь просить помощи у наставника.  </p>\n<p>На этом инструкция по работе с платформой YtYt заканчивается.<br/>\nПора приступать к обучению.  </p>';

      return content.split(/\[brython-snippet](.*?)snippet\]/gms).map((block) => {
        if (block.endsWith('[/brython-')) {
          return {
            type: 'code',
            content: block.replace('[/brython-', ''),
          };
        } else {
          return {
            type: 'text',
            content: block,
          };
        }
      });
    },
    async setNextFragment() {
      let shouldFetch = true;
      const curIndex = this.sections.findIndex((x) => x.id === this.activeSection);
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (curIndex !== -1) {
        const nextSection = this.sections[curIndex + 1];
        if (nextSection && [1, 2, 3].includes(nextSection.status)) {
          shouldFetch = false;
          this.activeSection = nextSection.id;
        } else if (lesson.next.pk && [1, 2, 3].includes(lesson.next.status)) {
          shouldFetch = false;
          this.$router.push(`/theme/${lesson.next.course_theme_id}/${lesson.next.pk}`);
        } else if (theme.next.pk && [1, 2, 3].includes(theme.next.status)) {
          shouldFetch = false;
          this.$router.push(`/theme/${theme.next.pk}`);
        }
      }

      if (shouldFetch) {
        await this.requestFragment({
          id: this.activeSection,
        })
          .then((res) => {
            if (res.id) {
              this.activeSection = res.id;
            }
            // else if (res.course_id) {
            // }
          })
          .catch((_err) => {});
      }
    },
    setFragment(id, status) {
      if (status && ![4, 5, 6, 7, 8].includes(status)) {
        this.activeSection = id;
      }
    },
    setPrevFragment() {
      if (this.isPrevAvailable) {
        this.setFragment(this.prevSectionId, 2);
      }
    },
    setPrevLesson() {
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (this.isPrevLessonAvailable) {
        if (lesson.prev.pk && [1, 2, 3].includes(lesson.prev.status)) {
          this.$router.push(`/theme/${lesson.prev.course_theme_id}/${lesson.prev.pk}`);
        } else if (theme.prev.pk && [1, 2, 3].includes(theme.prev.status)) {
          this.$router.push(`/theme/${theme.prev.pk}`);
        }
      }
    },
    setNextLesson() {
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (this.isNextLessonAvailable) {
        if (lesson.next.pk && [1, 2, 3].includes(lesson.next.status)) {
          this.$router.push(`/theme/${lesson.next.course_theme_id}/${lesson.next.pk}`);
        } else if (theme.next.pk && [1, 2, 3].includes(theme.next.status)) {
          this.$router.push(`/theme/${theme.next.pk}`);
        }
      }
    },
    highlightSyntax() {
      if (this.$refs.content) {
        this.$refs.content.querySelectorAll('code').forEach((block) => {
          window.hljs.highlightElement(block);
        });

        this.$refs.content.querySelectorAll('.CodeMirror').forEach((block) => {
          if (block.CodeMirror) {
            setTimeout(() => {
              block.CodeMirror.refresh();
            }, 10);
          }
        });
      }
    },
    handleQuestionClick() {
      this.isChatOpened = !this.isChatOpened;
      // this.$router.push(`/messages?id=${this.user.dialog.id}`);
    },
    handleClickBack() {
      this.isChatOpened = false;
    },
  },
};
</script>

<style lang="scss">
.brython {
  .CodeMirror,
  .CodeMirror-scroll {
    min-height: 1px;
    height: 100%;
    max-height: 300px;
  }

  .CodeMirror {
    padding: 12px 16px;
    border: 0;
    background: #fafafa;
    font-size: 15px;
  }
}
</style>

<style lang="scss" scoped>
.lesson {
  padding-top: 24px;
  &__wrapper {
    display: flex;
    flex-wrap: wrap;
  }
  &__sidebar,
  &__content {
    width: 100%;
    min-width: 1px;
    min-height: 0;
  }

  &__sidebar {
    flex: 0 0 260px;
    max-width: 260px;
  }
  &__content {
    flex: 0 0 calc(100% - 260px);
    max-width: calc(100% - 260px);
  }
  &__box {
    background: #fff;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    border-radius: 8px;
  }
  &__section {
    display: none;
    &.is-active {
      display: block;
    }
  }
  &__body {
    padding: 20px;
  }
  &__body-text > ::v-deep * {
    max-width: 640px;
  }
  &__body-text > ::v-deep *:first-child {
    margin-top: 0 !important;
  }
  &__actions {
    padding: 20px;
    display: flex;
    align-items: center;
    .button {
      padding-top: 13px;
      padding-bottom: 14px;
      margin-right: 16px;
      &:last-child {
        margin-right: 0;
      }
    }
  }
}

@include r($lg) {
  .lesson {
    &__sidebar {
      flex-basis: 100%;
      max-width: 100%;
    }
    &__content {
      flex-basis: 100%;
      max-width: 100%;
    }
    &__box {
      margin-top: 16px;
      background: transparent;
      box-shadow: none;
    }
    &__nav.nav {
      display: none;
    }
    &__body {
      padding: 0;
    }
    &__actions {
      padding: 0;
    }
  }
}
</style>
