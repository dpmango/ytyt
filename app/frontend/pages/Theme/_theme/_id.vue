<template>
  <CourseFragment :data="lesson" :request-fragment="requestFragment" />
</template>

<script>
export default {
  async asyncData({ params, store, error, ...context }) {
    const lesson = await store
      .dispatch('courses/lesson', {
        course_id: 1,
        theme_id: params.theme,
        fragment_id: params.id,
      })
      .catch((err) => {
        if (err.code === 403) {
          // this.$toast.global.error({ message: err.data.detail });
          context.redirect('/course');
          store.commit('ui/setModalPaymentStart2', true);
        }
      });

    return { lesson };
  },
  data() {
    return {};
  },
  head: {
    title: 'Урок курса',
  },
  methods: {
    async requestFragment({ id }) {
      const responce = await this.$store
        .dispatch('courses/compleate', {
          id,
        })
        .then((res) => {
          let { lesson_fragments: titles } = this.lesson;
          const { accessible_lesson_fragments: fragments } = this.lesson;

          // TODO move all logic in vuex state
          // @issue - asyncData + client

          // RESPONSE IS EITHER fragment meta or URL meta
          if (res.course_id) {
            // @issue one course only
            // TODO - because of TMP removed /course routing
            if (res.course_theme_id) {
              this.$router.push(`/theme/${res.course_theme_id}`);
            } else {
              this.$router.push('/course');
            }
          } else {
            // State updater
            const targetFragmentIndex = fragments.findIndex((frag) => frag.id === res.id);
            const targetTitleIndex = titles.findIndex((x) => x.id === res.id);

            if (targetFragmentIndex !== -1) {
              fragments[targetFragmentIndex] = {
                ...res,
              };
            } else {
              fragments.push(res);
            }

            titles = titles.map((x, idx) => {
              // update previous with compleated status
              if (idx < targetTitleIndex && [1, 2].includes(x.status)) {
                x.status = 3;
              }
              if (idx === targetTitleIndex) {
                x.status = res.status;
              }

              return x;
            });

            this.lesson = {
              ...this.lesson,
              ...{
                lesson_fragments: titles,
                accessible_lesson_fragments: fragments,
                progress: res.progress,
              },
            };
          }

          return res;
        })
        .catch((err) => {
          if (err.code === 403) {
            // this.$toast.global.error({ message: err.data.detail });
            this.$router.push('/course');
            this.$vfm.show('paymentStart');
          }
        });

      return responce;
    },
  },
};
</script>
