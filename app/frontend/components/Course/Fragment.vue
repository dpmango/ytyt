/* eslint-disable vue/no-v-html */
<template>
  <div class="lesson">
    <div class="container">
      <div class="lesson__wrapper">
        <div class="lesson__sidebar sidebar">
          <LayoutBack title="Вернуться к списку уроков" />

          <div class="sidebar__box">
            <div class="sidebar__progress">
              <div class="sidebar__progress-title">Твой прогресс</div>
              <div class="sidebar__progress-indicator">
                <div class="sidebar__progress-number" :style="{ left: `calc(${data.progress}% - 18px)` }">
                  {{ data.progress }} %
                </div>
                <div class="sidebar__progress-inner" :style="{ width: `calc(${data.progress}% - 18px)` }"></div>
              </div>
            </div>

            <div class="sidebar__lessons">
              <div
                v-for="section in sections"
                :key="section.id"
                class="sidebar__lesson"
                :class="[
                  section.id === activeSection && 'is-current',
                  section.status === 3 && 'is-compleated',
                  section.status === 4 && 'is-locked',
                ]"
                @click="setFragment(section.id, section.status)"
              >
                <div class="sidebar__lesson-icon">
                  <UiSvgIcon name="checkmark" />
                </div>
                <div class="sidebar__lesson-name">{{ section.status }} {{ section.title }}</div>
              </div>
            </div>
            <div class="sidebar__question">
              <a href="#">
                <UiSvgIcon name="question-filled" />
                <span>Задать вопрос куратору</span>
              </a>
            </div>
          </div>
        </div>

        <div class="lesson__content">
          <div class="lesson__box">
            <template v-if="activeSection === 0">
              <h3 class="h3-title">У вас нет доступа к этому уроку</h3>
            </template>

            <template v-else-if="sections">
              <div class="lesson__nav nav">
                <div class="nav__title">
                  <span class="nav__title-count">{{ currentSectionIndex + 1 }}/{{ sectionsCount }}</span>
                  {{ data.title }}
                </div>
                <div class="nav__actions">
                  <a
                    href="#"
                    class="nav__actions-prev"
                    :class="[!isPrevAvailable && 'disabled']"
                    @click.prevent="setPrevFragment"
                  >
                    <UiSvgIcon name="arrow-left-filled" />
                    <span>предидущий</span>
                  </a>
                  <a href="#" class="nav__actions-next" @click.prevent="setNextFragment">
                    <span>следующий</span>
                    <UiSvgIcon name="arrow-right-filled" />
                  </a>
                </div>
              </div>

              <template v-if="fragmentVisible">
                <div
                  v-for="fragment in fragmentVisible"
                  :key="fragment.id"
                  class="lesson__section"
                  :class="[fragment.id === activeSection && 'is-active']"
                >
                  <div class="lesson__body" v-html="fragment.content"></div>

                  <div class="lesson__actions">
                    <UiButton @click.prevent="setNextFragment">Продолжить</UiButton>
                    <!-- <UiButton :disabled="true" theme="outline">Задать вопрос куратору</UiButton> -->
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
  </div>
</template>

<script>
export default {
  props: {
    data: Object,
    requestFragment: Function,
  },
  data() {
    return {
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
      if (section) {
        return section.id;
      }

      return null;
    },
    prevSectionId() {
      const section = this.sections[this.currentSectionIndex - 1];
      if (section) {
        return section.id;
      }

      return null;
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
  methods: {
    async setNextFragment() {
      await this.requestFragment({
        id: this.activeSection,
      }).then((res) => {
        if (res.id) {
          this.activeSection = res.id;
        } else if (res.course_id) {
          // eslint-disable-next-line no-console
          console.log('end of lesson');
        }
      });
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
  },
};
</script>

<style lang="scss" scoped>
.lesson {
  padding-top: 24px;
  &__wrapper {
    display: flex;
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

.sidebar {
  &__box {
    background: #fff;
    border-radius: 8px;
  }
  &__progress {
    padding: 20px 20px 0;
  }
  &__progress-title {
    font-weight: 500;
    font-size: 17px;
    line-height: 150%;
  }
  &__progress-indicator {
    position: relative;
    margin-top: 6px;
    background: rgba(23, 24, 24, 0.08);
    border-radius: 12px;
    height: 10px;
    font-size: 0;
  }
  &__progress-number {
    position: absolute;
    z-index: 2;
    top: 50%;
    left: 0;
    font-size: 13px;
    color: $colorGreen;
    background: white;
    padding: 4px;
    transform: translateY(-50%);
  }
  &__progress-inner {
    position: absolute;
    z-index: 1;
    top: 0;
    left: 0;
    bottom: 0;
    background: linear-gradient(270deg, #00dd58 0%, #00ad45 100%);
    border-radius: 12px;
  }
  &__lessons {
    margin-top: 24px;
  }
  &__lesson {
    display: flex;
    align-items: center;
    padding: 8px 20px;
    cursor: pointer;
    transition: background 0.25s $ease;
    &.is-current {
      background: rgba(155, 81, 224, 0.06);
    }
    &.is-compleated {
      .sidebar {
        &__lesson-icon {
          background: $colorGreen;
          border-color: $colorGreen;
          .svg-icon {
            opacity: 1;
          }
        }
        &__lesson-name {
          color: rgba($fontColor, 0.5);
        }
      }
    }
    &.is-locked {
      pointer-events: none;
      .sidebar {
        &__lesson-icon {
          background: $colorGray;
          border-color: $colorGray;
        }
        &__lesson-name {
          color: rgba($fontColor, 0.5);
        }
      }
    }
    &:hover {
      background: rgba(155, 81, 224, 0.06);
    }
  }
  &__lesson-icon {
    position: relative;
    flex: 0 0 auto;
    min-width: 18px;
    min-height: 18px;
    margin-right: 10px;
    border-radius: 50%;
    border: 1px solid rgba($fontColor, 0.3);
    transition: background 0.25s $ease, border 0.25s $ease;
    .svg-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 9px;
      color: white;
      opacity: 0;
      transition: opacity 0.25s $ease;
    }
  }
  &__lesson-name {
    font-size: 15px;
    line-height: 1.3;
  }
  &__question {
    border-top: 1px solid rgba(#171818, 0.1);
    padding: 16px 20px;
    margin-top: 16px;
    a {
      display: inline-flex;
      align-items: center;
      font-size: 15px;
      line-height: 1.5;
      color: $colorPrimary;
      cursor: pointer;
      transition: color 0.25s $ease;
      .svg-icon {
        font-size: 18px;
        margin-right: 10px;
      }
      &:hover {
        color: $fontColor;
      }
    }
  }
}

.nav {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(#171818, 0.1);
  &__title {
    font-size: 15px;
    line-height: 1.5;
  }
  &__title-count {
    color: $colorGray;
  }
  &__actions {
    margin-left: auto;
    display: flex;
    align-items: center;
    a {
      display: inline-flex;
      align-items: center;
      font-size: 15px;
      margin-right: 16px;
      line-height: 1.5;
      color: $colorPrimary;
      cursor: pointer;
      transition: color 0.25s $ease;
      &:hover {
        color: $fontColor;
      }
      &.disabled {
        color: $colorGray;
        pointer-events: none;
      }
      &:last-child {
        margin-right: 0;
      }
    }
  }
  &__actions-prev {
    .svg-icon {
      font-size: 18px;
      margin-right: 8px;
    }
  }
  &__actions-next {
    .svg-icon {
      font-size: 18px;
      margin-left: 8px;
    }
  }
}

.back {
  margin: 16px 0;
}
</style>
