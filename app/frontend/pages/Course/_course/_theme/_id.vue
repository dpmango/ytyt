<template>
  <CourseFragment :data="lesson" :request-fragment="requestFragment" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    const lesson = await store.dispatch('courses/lesson', {
      course_id: params.course,
      theme_id: params.theme,
      fragment_id: params.id,
    });

    return { lesson };
  },
  data() {
    return {};
  },
  head: {
    title: 'Урок курса',
  },
  methods: {
    async requestFragment({ id }) {
      const responce = await this.$store
        .dispatch('courses/compleate', {
          id,
        })
        .then((res) => {
          const { accessible_lesson_fragments: fragments } = this.lesson;

          // TODO move all logic in vuex state
          // Issue - asyncData + client
          const targetFragment = fragments.find((frag) => frag.id === res.id);
          const fragmentIndex = fragments.indexOf(targetFragment);

          if (fragmentIndex !== -1) {
            fragments[fragmentIndex] = {
              ...res,
            };
          } else {
            fragments.push(res);
          }

          this.lesson.accessible_lesson_fragments = fragments;

          return res;
        })
        .catch((_err) => {
          this.$toast.error(_err);
        });

      return responce;
    },
    async getData() {
      const { course, theme, id } = this.$route.params;

      const lesson = await this.$store.dispatch('courses/lesson', {
        course_id: course,
        theme_id: theme,
        fragment_id: id,
      });

      return { lesson };
    },
  },
};
</script>
