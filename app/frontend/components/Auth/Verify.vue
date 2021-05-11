<template>
  <div class="verification">
    <div class="h2-title">Подтверждение email</div>
    <div class="verification__status">
      <div v-if="verified" class="verification__status-text">
        Email подтвержден, перенаправляю на главную страницу...
      </div>
      <template v-else-if="error">
        <div class="verification__status-text verification__status-text--error">{{ error }}</div>
        <NuxtLink to="/course" class="verification__status-link"> Вернуться на главную </NuxtLink>
      </template>
      <template v-else>
        <UiLoader :loading="true" theme="block" />
      </template>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      query: null,
      verified: false,
      error: null,
    };
  },
  computed: {},
  created() {
    // store in state is much safer
    this.query = this.$route.query;
  },
  mounted() {
    this.verifyEmail();
  },
  methods: {
    async verifyEmail() {
      await this.verifyGet(this.query)
        .then((res) => {
          this.error = null;
          this.verified = true;
          this.$toast.global.default({ message: res.detail });
          setTimeout(() => {
            this.$router.push('/course');
          }, 500);
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 400) {
            Object.keys(data).forEach((key) => {
              this.error = data[key][0];
              this.$toast.global.error({ message: data[key][0] });
            });
          }
        });
    },
    ...mapActions('auth', ['verifyGet']),
  },
};
</script>

<style lang="scss" scoped>
.verification {
  padding: 32px;
  text-align: center;
  &__status {
    text-align: center;
    margin: 16px 0;
  }
  &__status-text {
    font-weight: 500;
    font-size: 16px;
    &--error {
      color: $colorRed;
    }
  }
  &__status-link {
    display: block;
    margin-top: 16px;
    color: $colorPrimary;
    transition: color 0.25s $ease;
    &:hover {
      color: $fontColor;
    }
  }
}
</style>
