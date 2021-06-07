<template>
  <!-- <CourseThemes :list="courses" /> -->
  <CourseLessons :list="lessons" :themes="themes" />
</template>

<script>
export default {
  async asyncData({ params, store, error, ...context }) {
    const handleError = (err) => {
      if (err.code === 403) {
        context.redirect('/course');
        store.commit('ui/setModalPaymentStart2', true);
      }
    };

    // const courses = await store.dispatch('courses/themes', { id: params.id });
    const themes = await store.dispatch('courses/themes', { id: 1 }).catch(handleError);
    const lessons = await store.dispatch('courses/lessons', { course_id: 1, theme_id: params.id }).catch(handleError);

    return { themes, lessons };
  },
  head: {
    title: 'Уроки курса',
  },
};
</script>
