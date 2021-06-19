<template>
  <div class="login">
    <div class="login__title h2-title">
      <slot name="title"></slot>
    </div>

    <client-only>
      <template slot="placeholder">
        <UiLoader :loading="true" theme="block" />
      </template>

      <slot name="form"></slot>
    </client-only>

    <div class="login__actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {},
};
</script>

<style lang="scss" scoped>
.login {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin: 0 auto;
  padding: 36px 20px;
  &__title {
    text-align: center;
  }
  &__actions {
    margin-top: 20px;
    font-size: 15px;
    text-align: center;
    a {
      position: relative;
      color: $colorPrimary;
      &::after {
        display: inline-block;
        content: '|';
        color: rgba(23, 24, 24, 0.3);
        margin: 0 2px 0 6px;
      }
      &:last-child {
        &::after {
          display: none;
        }
      }
    }
  }
}

::v-deep .login__form {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  margin-top: 24px;
  .input {
    margin-top: 16px;
  }
  .button {
    margin-top: 24px;
  }
}

.login ::v-deep {
  .input {
    &.dynamic {
      .input__label {
        top: 20px;
        font-size: 16px;
      }
      .input__input {
        input,
        textarea {
          padding-top: 22px;
          padding-bottom: 9px;
        }
      }
      // &.is-focused {
      //   .input__label {
      //     top: 8px;
      //     font-size: 12px;
      //   }
      // }
      // &.has-error {
      //   .input__label {
      //     top: 8px;
      //     font-size: 12px;
      //   }
      // }
    }
  }
}

@include r($sm) {
  .login {
    max-width: 100%;
    width: 100%;
    padding: 0;
  }

  ::v-deep .login__form {
    .button {
      margin-top: auto;
    }
  }
}
</style>
