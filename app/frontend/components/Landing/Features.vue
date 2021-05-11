<template>
  <section class="features">
    <div class="container">
      <h2 class="features__title">Для тех, у кого мало опыта</h2>
      <span class="features__subtitle">или совсем его нет</span>
      <div class="features__row">
        <div class="features__col">
          <div class="features__item">
            <img src="~assets/landing/img/feature__abc.svg" alt="" class="item-feature__icon" />
            <p class="item-feature__text">Простые объяснения вместо <br />заумных терминов</p>
          </div>
        </div>
        <div class="features__col">
          <div class="features__item">
            <img src="~assets/landing/img/feature__search.svg" alt="" class="item-feature__icon" />
            <p class="item-feature__text">Много наглядных примеров <br />и практики</p>
          </div>
        </div>
        <div class="features__col">
          <div class="features__item">
            <img src="~assets/landing/img/feature__chat.svg" alt="" class="item-feature__icon" />
            <p class="item-feature__text">Прямая связь <br />с персональным наставником</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.features {
  text-align: center;
  margin-bottom: 70px;
  &__title {
    margin-bottom: 10px;
  }

  &__subtitle {
    display: block;
    font-size: 26px;
    margin-bottom: 70px;
  }

  &__row {
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    margin: 0 -15px;
    padding: 0 55px;
    @media screen and (max-width: 1100px) {
      padding: 0;
    }
  }

  &__col {
    flex: 0 0 auto;
    width: 33.333%;
    padding: 0 15px;
  }

  // &__item {
  // }
}
@media screen and (max-width: $md) {
  .features {
    margin-bottom: 50px;
    &__subtitle {
      font-size: 22px;
      margin-bottom: 40px;
    }
    &__col {
      width: 100%;
      margin-bottom: 40px;
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.item-feature {
  text-align: center;
  padding: 0 30px;
  &__icon {
    margin-bottom: 40px;
  }

  &__text {
    font-size: 20px;
    line-height: 1.5;
  }
}
@media screen and (max-width: $md) {
  .item-feature {
    &__icon {
      margin-bottom: 25px;
    }
  }
}
@media screen and (max-width: 425px) {
  .item-feature {
    padding: 0;
    &__text {
      font-size: 18px;
      br {
        display: none;
      }
    }
  }
}
</style>
