<template>
  <!-- <CourseCourses :list="list" /> -->
  <CourseThemes :list="courses" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    // const list = await store.dispatch('courses/courses');
    // TODO - on MVP there is only one course
    const courses = await store.dispatch('courses/themes', { id: 1 });

    return { courses };
  },
  head: {
    title: 'Темы Курса',
  },
};
</script>
