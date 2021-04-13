<template>
  <!-- <CourseThemes :list="courses" /> -->
  <CourseLessons :list="lessons" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    // const courses = await store.dispatch('courses/themes', { id: params.id });
    const lessons = await store.dispatch('courses/lessons', { course_id: 1, theme_id: params.id });

    return { lessons };
  },
  head: {
    title: 'Уроки курса',
  },
};
</script>
