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
                :is-prev-available="isPrevAvailable"
                :set-next-fragment="setNextFragment"
                :set-prev-fragment="setPrevFragment"
              />

              <template v-if="fragmentVisible">
                <div
                  v-for="fragment in fragmentVisible"
                  :key="fragment.id"
                  class="lesson__section"
                  :class="[fragment.id === activeSection && 'is-active']"
                >
                  <div class="lesson__body markdown-body" v-html="fragment.content"></div>

                  <UiBrython :id="`${fragment.id}`" :ready="brythonReady" />

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
      const section = this.sections[this.currentSectionIndex + 11];
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
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (this.prevSectionId) {
        return this.prevSectionId;
      } else if (lesson.prev.pk && [1, 2, 3].includes(lesson.prev.status)) {
        return 1;
      } else if (theme.prev.pk && [1, 2, 3].includes(theme.prev.status)) {
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
    }
  },
  methods: {
    async setNextFragment() {
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      let shouldFetch = true;
      const curIndex = this.sections.findIndex((x) => x.id === this.activeSection);

      if (curIndex !== -1) {
        const nextSection = this.sections[curIndex + 1];
        if (nextSection && [1, 2, 3].includes(nextSection.status)) {
          shouldFetch = false;
          this.activeSection = nextSection.id;
        } else if (lesson.next.pk && [1, 2, 3].includes(lesson.next.status)) {
          shouldFetch = false;
          this.$router.push(`/theme/${theme.next.pk}/${lesson.next.pk}`);
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
            } else if (res.course_id) {
              // eslint-disable-next-line no-console
              console.log('end of lesson');
            }
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
      const { course_lesson: lesson, course_theme: theme } = this.data.meta;

      if (this.isPrevAvailable) {
        if (lesson.prev.pk && [1, 2, 3].includes(lesson.prev.status)) {
          this.$router.push(`/theme/${theme.prev.pk}/${lesson.prev.pk}`);
        } else if (theme.prev.pk && [1, 2, 3].includes(theme.prev.status)) {
          this.$router.push(`/theme/${theme.prev.pk}`);
        } else {
          this.setFragment(this.prevSectionId, 2);
        }
      }
    },
    highlightSyntax() {
      if (this.$refs.content) {
        this.$refs.content.querySelectorAll('code').forEach((block) => {
          window.hljs.highlightElement(block);
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
  &__body > ::v-deep * {
    max-width: 640px;
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
