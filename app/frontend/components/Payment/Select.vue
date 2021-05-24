<template>
  <div class="row">
    <div class="col col-6 col-md-12 payment__form-wrapper">
      <div class="payment__form">
        <div class="payment__form-title">Есть вопросы?</div>
        <div class="payment__form-desc">Укажите номер телефона, менеджер свяжется с вами и ответит на все вопросы</div>
        <ValidationObserver
          ref="form"
          v-slot="{ invalid }"
          tag="form"
          class="profile__form"
          @submit.prevent="handleSubmit"
        >
          <ValidationProvider v-slot="{ errors }">
            <UiInput :value="phone" type="tel" :error="errors[0]" placeholder="+7" @onChange="(v) => (phone = v)" />
          </ValidationProvider>
          <UiButton theme="outline" block>Перезвоните мне</UiButton>
        </ValidationObserver>
      </div>
    </div>
    <div class="col col-6 col-md-12">
      <div class="payment__options">
        <h1 class="payment__title">Выберите удобный вариант оплаты</h1>
        <div class="payment__list">
          <div
            v-for="option in options"
            :key="option.id"
            class="card"
            :class="[activeVariant === option.id && 'is-active']"
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
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data() {
    return {
      phone: '',
      activeVariant: 1,
      options: [
        { id: 1, title: 'Вся сумма целиком', installment: false, price: '54 000', priceOld: '60 000' },
        { id: 2, title: 'Рассрочка на 4 месяца', installment: true, price: '15 000' },
        { id: 3, title: 'Рассрочка на 6 месяцев', installment: true, price: '10 000' },
        { id: 4, title: 'Рассрочка на 12 месяцев', installment: true, price: '5 000' },
      ],
    };
  },
  methods: {
    selectPayment(id) {
      this.activeVariant = id;
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
    },
    ...mapActions('payment', ['init', 'initInstallment']),
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
    form {
      margin-top: 24px;
    }
    .button {
      margin-top: 12px;
    }
    ::v-deep input {
      padding-top: 20px;
      padding-bottom: 20px;
      background: white;
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
  &.is-active {
    .card__checkbox {
      &::after {
        transform: translate(-50%, -50%) scale(1);
      }
    }
  }
}
</style>
