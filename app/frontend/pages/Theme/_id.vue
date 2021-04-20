<template>
  <!-- <CourseThemes :list="courses" /> -->
  <CourseLessons :list="lessons" :themes="themes" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    // const courses = await store.dispatch('courses/themes', { id: params.id });
    const themes = await store.dispatch('courses/themes', { id: 1 });
    const lessons = await store.dispatch('courses/lessons', { course_id: 1, theme_id: params.id });

    return { themes, lessons };
  },
  head: {
    title: 'Уроки курса',
  },
};
</script>
