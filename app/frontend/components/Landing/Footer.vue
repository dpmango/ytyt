<template>
  <footer class="footer">
    <div class="footer__top container">
      <a href="#" class="footer__logo">
        <img src="~assets/landing/img/logo.png" srcset="~assets/landing/img/logo@2x.png 2x" alt="YTYT Logo" />
      </a>
      <div class="footer__information">
        <p>ИП Умаров Т. А.</p>
        <p>ИНН 745216229809 / ОГРНИП 315745200001358</p>
      </div>
      <ul class="footer__contacts contacts-footer">
        <li class="contacts-footer__item">
          <a :href="`tel:${phone.trim()}`" class="contacts-footer__link">
            <img src="~assets/landing/img/icon-phone.svg" alt="" class="contacts-footer__icon" />
            <span>{{ phone }}</span>
          </a>
        </li>
        <li class="contacts-footer__item">
          <a :href="`mailto:${mail}`" class="contacts-footer__link">
            <img src="~assets/landing/img/icon-envelope.svg" alt="" class="contacts-footer__icon" />
            <span>{{ mail }}</span>
          </a>
        </li>
      </ul>
      <!-- <ul class="footer__soc soc-footer">
        <li v-for="social in socials" :key="social.id" class="soc-footer__item">
          <a :href="social.href" target="_blank" class="soc-footer__link">
            <img :src="social.icon" :alt="social.title" class="soc-footer__icon" />
          </a>
        </li>
      </ul> -->
    </div>
    <hr />
    <div class="footer__bottom container">
      <span class="footer__copyright">Онлайн-школа программирования YtYt</span>
      <div class="footer__links">
        <a href="landing/files/terms_of_service.pdf" target="_blank">Пользовательское соглашение</a>
        <a href="landing/files/confidentiality_policy.pdf" target="_blank">Политика конфиденциальности</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      phone: '+7 (499) 348-93-96',
      mail: 'info@ytyt.ru',
      socials: [
        {
          id: 1,
          title: 'YouTube',
          href: 'https://www.youtube.com/channel/UCj-OyxAtGEW4uERbY23VzrQ',
          icon: '/landing/img/soc-youtube.svg',
        },
        {
          id: 2,
          title: 'VK.com',
          href: 'https://vk.com/ytyt_programming',
          icon: '/landing/img/soc-vk.svg',
        },
        {
          id: 3,
          title: 'Facebook',
          href: 'https://www.facebook.com/groups/ytyt.programming',
          icon: '/landing/img/soc-fb.svg',
        },
        {
          id: 4,
          title: 'Instagram',
          href: 'https://www.instagram.com/ytyt_programming/',
          icon: '/landing/img/soc-instagram.svg',
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.footer {
  position: relative;
  background-color: $fontColor;
  color: #fff;
  hr {
    background-color: rgba(#fff, 0.1);
    height: 1px;
  }
  &__top {
    display: flex;
    align-items: center;
    padding-top: 30px;
    padding-bottom: 30px;
  }

  &__logo {
    margin-right: 60px;
  }

  &__information {
    p:nth-child(1) {
      opacity: 0.5;
    }
    p:nth-child(2) {
      font-size: 14px;
      opacity: 0.3;
    }
  }

  &__contacts {
    // margin: 0 auto;
    margin: 0 0 0 auto;
  }

  // &__soc {
  // }

  &__bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    padding-bottom: 20px;
  }

  &__copyright {
    font-size: 14px;
    line-height: 1.3;
    color: rgba(#fff, 0.5);
  }

  &__links {
    display: flex;
    a {
      font-size: 14px;
      color: rgba(#fff, 0.5);
      margin-right: 24px;
      transition: color 0.2s;
      &:hover {
        opacity: 1;
        color: rgba(#fff, 1);
      }
      &:last-child {
        margin-right: 0;
      }
    }
  }
}
.contacts-footer {
  display: flex;
  list-style: none;
  &__item {
    flex: 0 0 auto;
    margin-right: 32px;
    &:last-child {
      margin-right: 0;
    }
  }

  &__link {
    font-family: $baseFont;
    font-size: 18px;
    color: #fff;
    &:hover {
      .contacts-footer__icon {
        opacity: 1;
      }
    }
  }

  &__icon {
    vertical-align: middle;
    opacity: 0.5;
    margin-right: 12px;
    transition: 0.2s;
  }
}
.soc-footer {
  display: flex;
  align-items: center;
  list-style: none;
  &__item {
    margin-right: 8px;
    transition: opacity 0.25s $ease;
    &:last-child {
      margin-right: 0;
    }
    &:hover {
      opacity: 0.7;
    }
  }

  // &__link {
  // }

  // &__icon {
  // }
}

@include r(1140) {
  .footer {
    &__top {
      justify-content: space-between;
      flex-wrap: wrap;
    }
    &__logo {
      margin-right: 0;
      // margin-bottom: 30px;
    }
    &__information {
      // flex: 0 0 50%;
      flex: 0 0 auto;
      margin: 0 0 0 auto;
      order: 3;
    }
    &__contacts {
      margin: 0;
      order: 2;
      // margin-bottom: 30px;
      margin-bottom: 0;
      padding-left: 30px;
    }
    &__soc {
      flex: 0 0 50%;
      order: 4;
    }
  }
  .contacts-footer {
    justify-content: flex-end;
  }
  .soc-footer {
    justify-content: flex-end;
  }
}

@include r($md) {
  .footer {
    &__top {
      padding-top: 25px;
      padding-bottom: 25px;
    }
    &__bottom {
      padding-top: 25px;
      padding-bottom: 25px;
    }
  }
}

@include r($sm) {
  .footer {
    &__top {
      flex-direction: column;
      padding-bottom: 0;
    }
    &__logo {
      margin-right: 0;
      margin-bottom: 20px;
      order: 4;
    }
    &__information {
      order: 3;
      margin: 0 0 20px 0;
      text-align: center;
    }
    &__contacts {
      margin: 0;
      order: 1;
      margin-bottom: 25px;
      padding-left: 0;
    }
    &__soc {
      order: 2;
      margin-bottom: 20px;
    }
    hr {
      display: none;
    }
    &__bottom {
      flex-direction: column;
      text-align: center;
      padding-top: 0;
    }
    &__copyright {
      order: 0;
      margin-bottom: 20px;
    }
    &__links {
      flex-direction: column;
      margin-bottom: 20px;
      a {
        margin-right: 0;
        margin-bottom: 15px;
        &:last-child {
          margin-bottom: 0;
        }
      }
    }
  }
  .contacts-footer {
    flex-direction: column;
    align-items: center;
    &__item {
      margin-right: 0;
      margin-bottom: 15px;
      &:last-child {
        margin-bottom: 0;
      }
    }
    &__link {
      font-size: 16px;
    }
    &__icon {
      max-width: 24px;
    }
  }
}
</style>
