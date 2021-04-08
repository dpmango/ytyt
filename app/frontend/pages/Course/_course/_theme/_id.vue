<template>
  <CourseFragment :data="lesson" />
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
  head: {
    title: 'Урок курса',
  },
};
</script>
