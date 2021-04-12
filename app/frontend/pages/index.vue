<template>
  <CourseCourses :list="list" />
</template>

<script>
export default {
  async asyncData({ params, store, error }) {
    const list = await store.dispatch('courses/courses');

    return { list };
  },
  head: {
    title: 'Курсы',
  },
};
</script>
