<template>
  <CourseLessons :list="lessons" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    const lessons = await store.dispatch('courses/lessons', { course_id: params.course, theme_id: params.id });

    return { lessons };
  },
  head: {
    title: 'Уроки курса',
  },
};
</script>
