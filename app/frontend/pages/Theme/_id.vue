<template>
  <!-- <CourseThemes :list="courses" /> -->
  <CourseLessons :list="lessons" :themes="themes" />
</template>

<script>
export default {
  async asyncData({ params, $sentry, store, route, error, ...context }) {
    const handleError = (err) => {
      if (err.code === 403) {
        context.redirect('/course');
        store.commit('ui/setModalPaymentStart2', true);
      }
    };

    try {
      // const courses = await store.dispatch('courses/themes', { id: params.id });
      const themes = await store.dispatch('courses/themes', { id: 1 }).catch(handleError);
      const lessons = await store.dispatch('courses/lessons', { course_id: 1, theme_id: params.id }).catch(handleError);
      const theme = themes.find((x) => x.id === parseInt(route.params.id));

      // console.log('context route', route);
      return { themes, lessons, name: theme.title };
    } catch (error) {
      $sentry.captureException(error);
    }
  },
  data() {
    return {
      name: '',
    };
  },
  head() {
    return { title: `${this.name} | YtYt - понятные уроки программирования` };
  },
};
</script>
