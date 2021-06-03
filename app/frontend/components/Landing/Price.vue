<template>
  <section class="price">
    <div class="price__container container">
      <div class="price__row">
        <div class="price__info info-price">
          <h2 class="info-price__title">Стоимость обучения</h2>
          <div class="info-price__full">
            <h3 class="info-price__label">Разовый платеж</h3>
            <span class="info-price__current">54 000 <span>₽</span></span>
            <span class="info-price__old">60 000 <span>₽</span></span>
          </div>
          <div class="info-price__part">
            <h3 class="info-price__label">Рассрочка с ежемесячным платежом</h3>
            <div class="info-price__tabs tabs">
              <ul class="tabs__header header-tabs">
                <li
                  v-for="price in prices"
                  :key="price.id"
                  class="header-tabs__item"
                  :class="[price.id === activePrice && 'active']"
                  @click="setTab(price.id)"
                >
                  {{ price.title }}
                </li>
              </ul>
              <ul class="tabs__content content-tabs">
                <li
                  v-for="price in prices"
                  :key="price.id"
                  class="content-tabs__item"
                  :class="[price.id === activePrice && 'active']"
                >
                  {{ price.price }} <span>₽/мес</span>
                </li>
              </ul>
            </div>
          </div>
          <div class="info-price__extra">
            <p>Рассрочка предоставляется банком Тинькофф</p>
            <a href="landing/files/installment_terms.pdf" target="_blank" class="info-price__link">Условия рассрочки</a>
          </div>
        </div>
        <div class="price__join join-price">
          <h2 class="join-price__title">Записаться на курс или получить бесплатную консультацию</h2>
          <ValidationObserver
            ref="form"
            v-slot="{ invalid }"
            tag="form"
            class="join-price__form form"
            @submit.prevent="handleSubmit"
          >
            <UiError :error="error" />

            <ValidationProvider v-slot="{ errors }" class="ui-group" rules="required">
              <UiInput
                :value="name"
                theme="dynamic"
                label="Имя"
                type="text"
                :error="errors[0]"
                @onChange="(v) => (name = v)"
              />
            </ValidationProvider>

            <ValidationProvider v-slot="{ errors }" class="ui-group" rules="email|required">
              <UiInput
                :value="email"
                theme="dynamic"
                label="Email"
                type="email"
                :error="errors[0]"
                @onChange="(v) => (email = v)"
              />
            </ValidationProvider>

            <ValidationProvider v-slot="{ errors }" class="ui-group" rules="required">
              <UiInput
                :value="phone"
                theme="dynamic"
                label="Телефон"
                type="tel"
                :error="errors[0]"
                @onChange="(v) => (phone = v)"
              />
            </ValidationProvider>

            <UiButton type="submit" block>Отправить заявку</UiButton>
          </ValidationObserver>

          <p class="join-price__extra">
            Отправляя заявку, вы даете согласие на обработку своих персональных данных в соответствии с
            <a href="landing/files/confidentiality_policy.pdf" target="_blank">политикой конфиденциальности</a>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      activePrice: 1,
      prices: [
        {
          id: 1,
          title: '12 мес.',
          price: '5 000',
        },
        {
          id: 2,
          title: '6 мес.',
          price: '6 000',
        },
        {
          id: 3,
          title: '4 мес.',
          price: '15 000',
        },
      ],
      name: null,
      email: null,
      phone: null,
      error: null,
    };
  },

  methods: {
    setTab(id) {
      this.activePrice = id;
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      const { name, email, phone } = this;
      await this.login({ name, email, phone })
        .then((_res) => {
          this.error = null;
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 401) {
            Object.keys(data).forEach((key) => {
              this.error = data[key];
            });
          }
        });
    },
    // ...mapActions('auth', ['login']),
  },
};
</script>

<style lang="scss" scoped>
.price {
  margin-bottom: 80px;
  &__row {
    display: flex;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    border-radius: 8px;
    width: 100%;
  }

  &__info {
    flex: 0 0 auto;
    width: 50%;
  }
  &__join {
    flex: 0 0 auto;
    width: 50%;
  }
  @include r($lg) {
    margin-bottom: 0;
    .container {
      padding: 0;
    }
    &__row {
      flex-wrap: wrap;
    }
    &__info {
      width: 100%;
    }
    &__join {
      width: 100%;
    }
  }
}

.info-price {
  background-color: #fff;
  padding: 40px 50px 60px;
  &__title {
    margin-bottom: 50px;
  }

  &__full {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 38px;
  }

  &__label {
    flex: 0 0 100%;
    font-size: 20px;
    line-height: 1.5;
    font-weight: normal;
    margin-bottom: 12px;
  }

  &__current {
    font-family: $baseFont;
    font-size: 48px;
    color: $fontColor;
    margin-right: 16px;
    span {
      display: inline-block;
      margin-left: 5px;
      opacity: 0.5;
    }
  }

  &__old {
    font-family: $baseFont;
    font-size: 24px;
    color: $fontColor;
    opacity: 0.5;
    text-decoration: line-through;
    span {
      opacity: 0.5;
    }
  }

  &__part {
    margin-bottom: 24px;
  }

  // &__tabs {
  // }
  &__extra {
    p {
      font-family: $baseFont;
      font-size: 14px;
      color: $fontColor;
      opacity: 0.5;
      margin-bottom: 2px;
    }
  }
  &__link {
    font-family: $baseFont;
    color: $colorPrimary;
    font-size: 14px;
    border-bottom: 1px solid transparent;
    transition: 0.2s;
    &:hover {
      border-bottom-color: $colorPrimary;
    }
  }
  @include r($lg) {
    &__title {
      margin-bottom: 30px;
    }
  }
  @include r($md) {
    padding: 30px 15px 25px;
    &__title {
      font-size: 28px;
      margin-bottom: 25px;
    }
    &__full {
      margin-bottom: 16px;
    }
  }
  @include r($mobile-s) {
    &__label {
      font-size: 18px;
    }
    &__current {
      font-size: 30px;
    }
    &__old {
      font-size: 16px;
    }
    &__extra {
      p {
        font-size: 14px;
      }
    }
  }
}
.join-price {
  background-color: #f2f2f2;
  text-align: center;
  padding: 40px 100px;
  &__title {
    font-size: 32px;
    margin-bottom: 32px;
  }
  &__form {
    margin-bottom: 16px;
  }
  &__extra {
    font-family: $baseFont;
    text-align: center;
    line-height: 1.5;
    opacity: 0.5;
    margin: 0 auto;
    a {
      color: #000;
      text-decoration: underline;
    }
  }
  @include r($xl) {
    padding: 40px 50px;
  }
  @include r($md) {
    padding: 30px 15px;
    &__title {
      font-size: 22px;
    }
    &__extra {
      font-size: 14px;
    }
  }
}

.form {
  display: flex;
  flex-direction: column;
  .ui-group {
    margin-bottom: 24px;
    ::v-deep .input .input__input input {
      padding-top: 25px;
      padding-bottom: 12px;
    }
    &:last-of-type {
      margin-bottom: 32px;
    }
  }
  &__button {
    display: flex;
  }
}
</style>
