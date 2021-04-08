<template>
  <CourseThemes :list="courses" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    const courses = await store.dispatch('courses/themes', { id: params.id });

    return { courses };
  },
  head: {
    title: 'Темы курса',
  },
};
</script>
