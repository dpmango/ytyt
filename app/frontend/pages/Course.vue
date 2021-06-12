<template>
  <!-- <CourseCourses :list="list" /> -->
  <CourseThemes :list="courses" />
</template>

<script>
export default {
  async asyncData({ params, $sentry, store, error }) {
    // const list = await store.dispatch('courses/courses');
    // TODO - on MVP there is only one course
    try {
      const courses = await store.dispatch('courses/themes', { id: 1 });

      return { courses };
    } catch (error) {
      $sentry.captureException(error);
    }
  },
  head: {
    title: 'Главная | YtYt - понятные уроки программирования',
  },
};
</script>
