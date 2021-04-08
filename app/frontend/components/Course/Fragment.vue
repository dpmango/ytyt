/* eslint-disable vue/no-v-html */
<template>
  <div class="lesson">
    <div class="container">
      <div class="lesson__wrapper">
        <div class="lesson__sidebar sidebar">
          <div class="back" @click="goBack">Вернуться к списку уроков</div>

          <div class="sidebar__box">
            <div class="sidebar__progress">
              <div class="sidebar__progress-title">Твой прогресс</div>
              <div class="sidebar__progress-indicator">
                <div class="sidebar__progress-inner" :style="{ width: '30%' }"></div>
              </div>
            </div>

            <div class="sidebar__lessons">
              <div
                v-for="section in sections"
                :key="section.id"
                class="sidebar__lesson"
                :class="[section.id === activeSection && 'is-current']"
                @click="setFragment(section.id)"
              >
                <span>{{ section.title }}</span>
              </div>
            </div>
            <div class="sidebar__question">
              <a href="#">Задать вопрос</a>
            </div>
          </div>
        </div>

        <div class="lesson__content">
          <div class="lesson__box">
            <template v-if="sections">
              <div class="lesson__nav nav">
                <div class="nav__title">{{ activeSection }}/{{ sectionsCount }}</div>
                <div class="nav__actions">
                  <a href="#" :class="[!isPrevAvailable && 'disabled']" @click.prevent="setPrevFragment"
                    >&lt; предидущий</a
                  >
                  <a href="#" :class="[!isNextAvailable && 'disabled']" @click.prevent="setNextFragment"
                    >следующий &gt;</a
                  >
                </div>
              </div>

              <div
                v-for="section in sections"
                :key="section.id"
                class="lesson__section"
                :class="[section.id === activeSection && 'is-active']"
              >
                <div class="lesson__body" v-html="section.description"></div>

                <div class="lesson__actions">
                  <UiButton :disabled="!isNextAvailable" @click.prevent="setNextFragment">Продолжить</UiButton>
                  <UiButton theme="outline">Задать вопрос куратору</UiButton>
                </div>
              </div>
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
  },
  data() {
    return {
      activeSection: 1,
    };
  },
  computed: {
    sections() {
      return this.data.lesson_fragments;
    },
    sectionsCount() {
      return this.sections.length;
    },
    isNextAvailable() {
      return this.sectionsCount > this.activeSection;
    },
    isPrevAvailable() {
      return this.activeSection > 1;
    },
  },
  created() {
    this.activeSection = this.data.lesson_fragments[0].id;
  },
  methods: {
    getFragment(id) {
      return this.sections.find((x) => x.id === id);
    },
    setFragment(id) {
      this.activeSection = id;
    },
    setNextFragment() {
      if (this.isNextAvailable) {
        this.setFragment(this.activeSection + 1);
      }
    },
    setPrevFragment() {
      if (this.isPrevAvailable) {
        this.setFragment(this.activeSection - 1);
      }
    },
    goBack() {
      return this.$router.go(-1);
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
  &__progress-inner {
    position: absolute;
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
    padding: 8px 20px;
    font-size: 15px;
    line-height: 1.3;
    cursor: pointer;
    transition: background 0.25s $ease;
    &.is-current {
      background: rgba(155, 81, 224, 0.06);
    }
    &:hover {
      background: rgba(155, 81, 224, 0.06);
    }
  }
  &__question {
    border-top: 1px solid rgba(#171818, 0.1);
    padding: 16px 20px;
    margin-top: 16px;
    a {
      font-size: 15px;
      line-height: 1.5;
      color: $colorPrimary;
      cursor: pointer;
      transition: color 0.25s $ease;
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
  &__actions {
    margin-left: auto;
    a {
      display: inline-block;
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
}
.back {
  display: inline-block;
  margin: 16px 0;
  font-size: 14px;
  line-height: 1.5;
  color: $colorPrimary;
  cursor: pointer;
  transition: color 0.25s $ease;
  &:hover {
    color: $fontColor;
  }
}
</style>
