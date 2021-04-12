<template>
  <div class="search">
    <div class="search__input">
      <UiInput
        :value="input"
        placeholder="Поиск..."
        icon="search"
        icon-position="left"
        type="search"
        clearable
        @blur="handleBlur"
        @onChange="handleChange"
      />
    </div>
    <div class="search__results">
      <ul class="search__list">
        <li v-for="course in list" :key="course.id" class="list__row">
          <NuxtLink
            class="card"
            :to="`/course/${course.course_id}/${course.course_theme.id}/${course.course_lesson.id}`"
          >
            <div class="card__content">
              <div class="card__course">{{ course.course_title }}</div>
              <div class="card__title">{{ course.course_lesson.title }}</div>
              <div class="card__description">{{ course.course_lesson.description }}</div>
            </div>
          </NuxtLink>
        </li>
      </ul>
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
            this.$toast.error(err.data.detail);
            this.$router.push('/payment');
          }
        });

      return res;
    }, 500);
  },
  methods: {
    handleChange(v) {
      this.input = v;
      this.handleDebounced(v);
    },
    handleBlur(e) {
      this.list = [];
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
  position: relative;
  &__input {
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
        }
      }
    }
  }

  &__results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #fff;
    box-shadow: 0 8px 24px -4px rgba(23, 24, 24, 0.12);
    border-radius: 4px;
  }
  &__list {
    list-style: none;
    padding: 0;
    margin: 0;
    li {
      display: block;
    }
  }
}

.card {
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  border-bottom: 1px solid $borderColor;
  transition: background 0.25s $ease;
  &__course {
    font-size: 14px;
    line-height: 150%;
    color: $colorGray;
  }
  &__title {
    font-weight: 500;
    font-size: 17px;
    line-height: 150%;
  }
  &__description {
    margin-top: 4px;
    font-size: 14px;
    line-height: 150%;
  }
  &:hover {
    background: rgba(155, 81, 224, 0.06);
  }
  &:last-child {
    border-bottom: 0;
  }
}
</style>
