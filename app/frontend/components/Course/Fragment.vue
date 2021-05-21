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
                  <UiBrython />

                  <div class="lesson__body markdown-body" v-html="fragment.content"></div>

                  <div class="lesson__actions">
                    <UiButton @click.prevent="setNextFragment">Продолжить</UiButton>
                    <UiButton v-if="user.dialog" theme="outline" @click="handleQuestionClick">
                      Задать вопрос куратору
                    </UiButton>
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
      return this.prevSectionId;
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
    // this.highlightSyntax();
  },
  methods: {
    async setNextFragment() {
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
    },
    setFragment(id, status) {
      if (status && status !== 4) {
        this.activeSection = id;
      }
    },
    setPrevFragment() {
      if (this.isPrevAvailable) {
        this.setFragment(this.prevSectionId, 2);
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
      this.isChatOpened = true;
      // this.$router.push(`/messages?id=${this.user.dialog.id}`);
    },
    handleClickBack() {
      this.isChatOpened = false;
    },
  },
};
</script>

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
  &__actions {
    padding: 20px;
    display: flex;
    align-items: center;
    .button {
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
