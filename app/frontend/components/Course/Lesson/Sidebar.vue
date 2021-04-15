<template>
  <div class="lesson__sidebar sidebar">
    <LayoutBack :to="`/theme/${$route.params.theme}`" title="Вернуться к списку уроков" />

    <div class="sidebar__box">
      <div class="sidebar__nav lg-visible">
        <span class="sidebar__nav-count">{{ currentSectionIndex + 1 }}/{{ sectionsCount }}</span>
        {{ title }}
      </div>

      <div class="sidebar__progress">
        <div class="sidebar__progress-title">Твой прогресс</div>
        <div class="sidebar__progress-indicator">
          <div class="sidebar__progress-number" :style="{ left: `calc(${progress}% - 18px)` }">{{ progress }} %</div>
          <div class="sidebar__progress-inner" :style="{ width: `calc(${progress}% - 18px)` }"></div>
        </div>
      </div>

      <div class="sidebar__lessons" :class="[visible && 'is-visible']">
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
        <a href="#" class="lg-visible" @click="toggleTopicsVisibility">
          <UiSvgIcon name="menu" />
          <span>Содержание</span>
        </a>
        <a href="#">
          <UiSvgIcon name="question-filled" />
          <span>Задать вопрос куратору</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    progress: Number,
    title: String,
    currentSectionIndex: Number,
    sectionsCount: Number,
    sections: Array,
    activeSection: Number,
    setFragment: Function,
  },
  data() {
    return {
      visible: false,
    };
  },
  methods: {
    toggleTopicsVisibility() {
      this.visible = !this.visible;
    },
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  &__box {
    background: #fff;
    border-radius: 8px;
  }
  &__nav {
    font-size: 15px;
    padding-left: 14px;
    padding-right: 14px;
  }
  &__nav-count {
    color: $colorGray;
  }
  &__progress {
    padding: 20px 20px 0;
  }
  &__progress-title {
    font-weight: 500;
    font-size: 17px;
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
    display: flex;
    align-items: center;
    border-top: 1px solid rgba(#171818, 0.1);
    padding: 16px 20px;
    margin-top: 16px;
    a {
      display: inline-flex;
      align-items: center;
      font-size: 15px;
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

.back {
  margin: 16px 0;
}

@include r($lg) {
  .sidebar {
    &__box {
      display: flex;
      flex-direction: column;
      max-width: 400px;
      box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
      padding: 12px 0 8px;
    }
    &__progress {
      order: 1;
      padding: 12px 14px 0;
    }
    &__progress-indicator {
      margin-top: 0;
    }
    &__lessons {
      order: 3;
      margin-top: 0;
      padding: 4px 0 8px;
      border-top: 1px solid $borderColor;
      display: none;
      &.is-visible {
        display: block;
      }
    }
    &__lesson {
      padding-left: 14px;
      padding-right: 14px;
    }
    &__question {
      order: 2;
      border-top: 0;
      margin-top: 0;
      padding: 12px 14px;
      a {
        font-size: 14px;
        margin-right: 12px;
        &:last-child {
          margin-right: 0;
        }
        .svg-icon {
          font-size: 16px;
          margin-right: 6px;
        }
        .svg-icon--menu {
          font-size: 9px;
        }
      }
    }
    &__progress-title {
      display: none;
    }
  }

  .back {
    margin: 0 0 12px;
  }
}
</style>
