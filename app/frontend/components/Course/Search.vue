<template>
  <div class="search">
    <div class="search__trigger" @click="handleTriggerClick">
      <UiSvgIcon name="search" />
    </div>
    <div class="search__wrapper" :class="[visible && 'is-visible']">
      <div class="search__input">
        <UiInput
          :value="input"
          placeholder="Поиск..."
          icon="search"
          icon-position="left"
          type="search"
          clearable
          @focus="handleFocus"
          @onChange="handleChange"
        />
      </div>
      <div class="search__results" :class="[active && 'is-active']">
        <ul class="search__list" @click="handleSelect">
          <li v-for="course in list" :key="course.id">
            <NuxtLink class="card" :to="`/theme/${course.course_theme.id}/${course.course_lesson.id}`">
              <div class="card__content">
                <div class="card__course">{{ course.course_theme.title }}</div>
                <div class="card__title">{{ course.course_lesson.title }}</div>
                <div class="card__description">{{ course.course_lesson.description }}</div>
              </div>
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      input: '',
      active: false,
      visible: false,
      list: [],
    };
  },
  created() {
    // throught created because of this. context
    this.handleDebounced = debounce(async (v) => {
      const res = await this.search({ text: v })
        .then((res) => {
          this.list = res;
        })
        .catch((err) => {
          if (err.code === 403) {
            this.$toast.global.error({ message: err.data.detail });
            this.$router.push('/payment');
          }
        });

      return res;
    }, 500);
  },
  mounted() {
    this.outsideClickListeners = window.addEventListener('click', this.clickOutside, false);
  },
  destroyed() {
    this.outsideClickListeners = window.removeEventListener('click', this.clickOutside, false);
  },
  methods: {
    handleChange(v) {
      this.input = v;
      this.handleDebounced(v);
    },
    handleFocus(e) {
      e.stopPropagation();

      this.active = true;
    },
    handleClose() {
      this.active = false;
      this.visible = false;
    },
    clickOutside(e) {
      if (!e.target.closest('.header__search')) {
        this.handleClose();
      }
    },
    handleTriggerClick() {
      this.visible = !this.visible;
    },
    handleSelect(e) {
      this.input = '';
      this.list = [];
      this.handleClose();
    },
    ...mapActions('courses', ['search']),
  },
  beforeDestroyed() {
    this.handleDebounced = null;
  },
};
</script>

<style lang="scss" scoped>
.search {
  &__trigger {
    position: relative;
    display: none;
    width: 36px;
    height: 36px;
    background: $colorBg;
    color: $colorGray;
    border-radius: 50%;
    overflow: hidden;
    cursor: pointer;
    transition: background 0.25s $ease, color 0.25s $ease;
    &:hover {
      background: $colorPrimary;
      color: white;
    }
    .svg-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 18px;
    }
  }
  &__input {
    position: relative;
    z-index: 2;
    ::v-deep .input__input {
      input {
        background: #fafafa;
        border-radius: 100px;
        padding-top: 7px;
        padding-bottom: 7px;
        &:focus,
        &:active {
          background-color: white;
          outline: none;
          &::placeholder {
            color: transparent;
          }
        }
      }
    }
  }
  &__wrapper {
    position: relative;
  }
  &__results {
    position: absolute;
    z-index: 1;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 8px 24px -4px rgba(23, 24, 24, 0.12);
    border-radius: 4px;
    opacity: 0;
    pointer-events: none;
    max-height: calc(100vh - 60px - 120px);
    overflow-y: auto;
    transition: opacity 0.2s $ease;
    &.is-active {
      opacity: 1;
      pointer-events: all;
    }
  }
  &__list {
    list-style: none;
    padding: 0;
    margin: 0;
    li {
      display: block;
      &:last-child {
        .card {
          border-bottom: 0;
        }
      }
    }
  }
}

@include r($md) {
  .search {
    &__trigger {
      display: block;
    }
    &__wrapper {
      position: absolute;
      z-index: 3;
      top: 0;
      left: 0;
      right: 0;
      background: #fff;
      font-size: 0;
      transform: translate3d(0, -100%, 0);
      will-change: transform;
      backface-visibility: hidden;
      pointer-events: none;
      transition: transform 0.25s $ease;
      &.is-visible {
        transform: none;
        pointer-events: all;
      }
    }
    &__input {
      box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
      ::v-deep .input__input {
        input {
          padding-top: 17px;
          padding-bottom: 17px;
          background: transparent;
          border-radius: 0;
          &:focus,
          &:active {
            border-color: transparent;
          }
        }
      }
    }
  }
}

.card {
  display: flex;
  flex-direction: column;
  padding: 16px 16px;
  border-bottom: 1px solid $borderColor;
  transition: background 0.25s $ease;
  &__course {
    font-size: 14px;
    color: $colorGray;
  }
  &__title {
    font-weight: 500;
    font-size: 17px;
  }
  &__description {
    margin-top: 4px;
    font-size: 14px;
  }
  &:hover {
    background: rgba(155, 81, 224, 0.06);
  }
}
</style>
