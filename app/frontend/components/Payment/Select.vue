<template>
  <div class="row payment">
    <div class="col col-6 col-md-12 payment__form-wrapper" :class="[!isMobileFormVisible && 'is-mobile-visible']">
      <div v-if="formSubmited" class="payment__form">
        <div class="payment__form-status">
          <UiSvgIcon name="status-success" />
        </div>
        <div class="payment__form-title">Спасибо за заявку</div>
        <div class="payment__form-desc">Наш менеджер свяжется с вами в ближайшее время</div>
        <div class="payment__cta-mobile">
          <UiButton block @click="isMobileFormVisible = true">Оплатить</UiButton>
          <UiButton theme="outline" block @click="resetModals">Закрыть</UiButton>
        </div>
      </div>

      <div v-else-if="installmentRefused && !failedInstallmentRequest" class="payment__form">
        <div class="payment__form-status">
          <UiSvgIcon name="status-cancel" />
        </div>
        <div class="payment__form-title">Банк отклонил заявку на рассрочку</div>
        <div class="payment__form-desc">
          Вы можете оплатить сумму целикомили оставить заявку для обсуждения других вариантов.
        </div>
        <div class="payment__form-cta">
          <a href="#" @click.prevent="failedInstallmentRequest = true">Подберите другие варианты</a>
        </div>
        <div class="payment__cta-mobile">
          <UiButton block @click="isMobileFormVisible = true">Оплатить целиком</UiButton>
          <UiButton theme="outline" block @click="failedInstallmentRequest = true">Подберите другие варианты</UiButton>
          <UiButton theme="outline" block @click="resetModals">Закрыть</UiButton>
        </div>
      </div>

      <div v-else class="payment__form">
        <template v-if="failedInstallmentRequest">
          <div class="payment__form-desc">
            Укажите номер телефона, менеджер свяжется с вами для обсуждения вариантов оплаты
          </div>
        </template>
        <template v-else>
          <div class="payment__form-title">Есть вопросы?</div>
          <div class="payment__form-desc">
            Укажите номер телефона, менеджер свяжется с вами и ответит на все вопросы
          </div>
        </template>
        <client-only>
          <template slot="placeholder">
            <UiLoader :loading="true" theme="block" />
          </template>
          <ValidationObserver
            ref="form"
            v-slot="{ invalid }"
            tag="form"
            class="profile__form"
            @submit.prevent="handleSubmit"
          >
            <UiError :error="error" />

            <ValidationProvider v-slot="{ errors }">
              <UiInput
                v-mask="'+7 (###) ###-####'"
                :value="phone"
                type="tel"
                :error="errors[0]"
                placeholder="+7"
                @onChange="(v) => (phone = v)"
              />
            </ValidationProvider>
            <div class="payment__cta">
              <UiButton type="submit" theme="outline" block>Перезвоните мне</UiButton>
            </div>
            <div class="payment__cta-mobile">
              <UiButton type="submit" block>Перезвоните мне</UiButton>
              <UiButton theme="outline" block @click="resetModals">Отмена</UiButton>
            </div>
          </ValidationObserver>
        </client-only>
      </div>
    </div>
    <div class="col col-6 col-md-12" :class="[isMobileFormVisible && 'is-mobile-visible']">
      <div class="payment__options">
        <h1 class="payment__title">Выберите удобный <br />вариант оплаты</h1>
        <div class="payment__list">
          <div
            v-for="option in options"
            :key="option.id"
            class="card"
            :class="[
              activeVariant === option.id && 'is-active',
              option.id !== 1 && installmentRefused && 'is-disabled',
            ]"
            @click="() => selectPayment(option.id)"
          >
            <div class="card__checkbox"></div>
            <div class="card__content">
              <div class="card__name">{{ option.title }}</div>
              <div class="card__price">
                <span v-if="option.priceOld" class="card__price-old">{{ option.priceOld }} ₽</span>
                {{ option.price }} ₽
                <span v-if="option.installment">/мес</span>
              </div>
            </div>
          </div>
        </div>
        <div class="payment__cta">
          <UiButton block @click="submitPayment">Оплатить</UiButton>
        </div>
        <div class="payment__cta-mobile">
          <UiButton block @click="submitPayment">Оплатить</UiButton>
          <UiButton theme="outline" block @click="isMobileFormVisible = false">Нужна консультация</UiButton>
          <UiButton theme="outline" block @click="resetModals">Отмена</UiButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapGetters } from 'vuex';

export default {
  data() {
    return {
      phone: '',
      error: null,
      formSubmited: false,
      failedInstallmentRequest: false,
      isMobileFormVisible: true,
      activeVariant: 1,
      options: [
        { id: 1, title: 'Вся сумма целиком', installment: false, price: '54 000', priceOld: '60 000' },
        { id: 2, title: 'Рассрочка на 4 месяца', installment: true, price: '15 000' },
        { id: 3, title: 'Рассрочка на 6 месяцев', installment: true, price: '10 000' },
        { id: 4, title: 'Рассрочка на 12 месяцев', installment: true, price: '5 000' },
      ],
    };
  },
  computed: {
    installmentRefused() {
      return !this.user.installment_available;
    },
    ...mapGetters('auth', ['user']),
  },
  mounted() {
    if (this.installmentRefused) {
      this.isMobileFormVisible = false;
    }
  },
  methods: {
    selectPayment(id) {
      this.activeVariant = id;
    },
    resetForm() {
      this.phone = '';
      // this.formSubmited = false;
      this.activeVariant = 1;
    },
    async submitPayment() {
      if (this.activeVariant === 1) {
        await this.init()
          .then((res) => {
            window.open(res.url);
          })
          .catch((err) => {
            this.$toast.global.error({ message: err.data });
          });
      } else {
        await this.initInstallment({ id: this.activeVariant })
          .then((res) => {
            window.open(res.url);
          })
          .catch((err) => {
            const { data, code } = err;

            if (data && code === 400) {
              this.$toast.global.error({ message: data.error.errors[0] });
            }
          });
      }
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      const { phone } = this;
      await this.feedback({ phone })
        .then((_res) => {
          this.error = null;
          this.phone = '';
          this.formSubmited = true;
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 400) {
            Object.keys(data).forEach((key) => {
              this.error = data[key][0];
            });
          }
        });
    },
    ...mapActions('payment', ['init', 'initInstallment']),
    ...mapActions('feedback', ['feedback']),
    ...mapMutations('ui', ['resetModals']),
  },
};
</script>

<style lang="scss" scoped>
.payment {
  &__form-wrapper {
    background: #f2f2f2;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  &__form {
    padding: 20px 40px 50px 40px;
    text-align: center;
    overflow: hidden;
    form {
      margin-top: 24px;
    }
    .button {
      margin-top: 12px;
    }
    ::v-deep .input__input input {
      padding-top: 19px;
      padding-bottom: 18px;
      background: white;
    }
  }
  &__form-status {
    font-size: 0;
    color: $colorRed;
    margin-bottom: 24px;
    .svg-icon {
      font-size: 100px;
    }
  }
  &__form-title {
    font-weight: bold;
    font-size: 32px;
    line-height: 1.5;
  }
  &__form-desc {
    margin-top: 12px;
    font-size: 18px;
    line-height: 1.5;
  }
  &__form-cta {
    margin-top: 12px;
    a {
      font-size: 18px;
      line-height: 150%;
      color: $colorPrimary;
      transition: color 0.25s $ease;
      &:hover {
        color: $colorPrimaryHover;
      }
    }
  }
  &__title {
    font-weight: bold;
    font-size: 24px;
    line-height: 130%;
  }
  &__list {
    margin: 24px 0 20px;
  }
  &__options {
    padding: 30px 40px;
  }
  // &__cta{

  // }
  &__cta-mobile {
    display: none;
    margin-top: 24px;
    .button {
      margin-bottom: 8px;
      padding-top: 14px;
      padding-bottom: 13px;
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.card {
  position: relative;
  display: flex;
  border-radius: 8px;
  background: white;
  border: 1px solid rgba($fontColor, 0.15);
  margin-bottom: 8px;
  padding: 10px 12px;
  cursor: pointer;
  transition: box-shadow 0.25s $ease;
  &:last-child {
    margin-bottom: 0;
  }
  &:hover {
    border-color: $colorPrimary;
  }
  &__checkbox {
    flex: 0 0 20px;
    position: relative;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid $colorPrimary;
    &::after {
      display: inline-block;
      content: ' ';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0);
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: $colorPrimary;
      transition: transform 0.25s $ease;
    }
  }
  &__content {
    padding-left: 12px;
    margin-top: -4px;
  }
  &__name {
    font-size: 18px;
    // font-weight: 500;
    line-height: 1.5;
  }
  &__price {
    margin-top: 4px;
    font-size: 14px;
    line-height: 150%;
    color: rgba($fontColor, 0.5);
  }
  &__price-old {
    text-decoration: line-through;
  }
  &.is-active {
    .card__checkbox {
      &::after {
        transform: translate(-50%, -50%) scale(1);
      }
    }
  }
  &.is-disabled {
    pointer-events: none;
    opacity: 0.3;
  }
}

@include r($md) {
  .payment {
    .col {
      display: none;
      &.is-mobile-visible {
        display: block;
      }
    }
    &__form-wrapper {
      background: white;
    }
    &__form {
      margin-top: 20px;
      padding: 24px;
      ::v-deep .input__input input {
        padding-top: 13px;
        padding-bottom: 12px;
        background: #f2f2f2;
      }
    }
    &__form-status {
      margin-bottom: 20px;
      .svg-icon {
        font-size: 72px;
      }
    }
    &__form-title {
      font-size: 24px;
    }
    &__form-desc {
      margin-top: 8px;
      max-width: 280px;
      margin-left: auto;
      margin-right: auto;
    }
    &__form-cta {
      display: none;
    }
    &__options {
      padding: 24px;
    }
    &__list {
      margin-bottom: 24px;
    }
    &__title {
      font-size: 20px;
    }
    &__cta {
      display: none;
    }
    &__cta-mobile {
      display: block;
    }
  }

  .card {
    &__name {
      font-size: 16px;
    }
  }
}
</style>
