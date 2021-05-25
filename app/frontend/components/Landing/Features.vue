<template>
  <section class="features">
    <div class="container">
      <h2 class="features__title">Для тех, у кого <br />мало опыта</h2>
      <span class="features__subtitle">или совсем его нет</span>
      <div class="features__row">
        <div v-for="col in cols" :key="col.id" class="features__col">
          <div class="features__item">
            <img :src="`/landing/img/${col.icon}`" alt="" class="item-feature__icon" />
            <p class="item-feature__text" v-html="col.content" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      cols: [
        { id: 1, icon: 'feature__abc.svg', content: 'Простые объяснения вместо <br />заумных терминов' },
        { id: 2, icon: 'feature__search.svg', content: 'Много наглядных примеров <br />и практики' },
        { id: 3, icon: 'feature__chat.svg', content: 'Прямая связь <br />с персональным наставником' },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.features {
  text-align: center;
  margin-bottom: 70px;
  &__title {
    margin-bottom: 10px;
    br {
      display: none;
    }
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
    @include r(1100) {
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
@include r($md) {
  .features {
    margin-bottom: 50px;
    &__title {
      br {
        display: block;
      }
    }
    &__subtitle {
      font-size: 22px;
      margin-bottom: 40px;
    }
    &__item {
      img {
        max-width: 72px;
      }
    }
    &__col {
      width: 100%;
      margin-bottom: 32px;
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
@include r($md) {
  .item-feature {
    &__icon {
      margin-bottom: 20px;
    }
  }
}

@include r(425) {
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
