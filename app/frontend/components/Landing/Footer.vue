<template>
  <footer class="footer">
    <div class="footer__top container">
      <a href="#" class="footer__logo">
        <img src="~assets/landing/img/logo.svg" alt="" />
      </a>
      <div class="footer__information">
        <p>ИП Умаров Т. А.</p>
        <p>ИНН 745216229809 / ОГРНИП 315745200001358</p>
      </div>
      <ul class="footer__contacts contacts-footer">
        <li class="contacts-footer__item">
          <a href="tel:+71234567890" class="contacts-footer__link"
            ><img src="~assets/landing/img/icon-phone.svg" alt="" class="contacts-footer__icon" />+7 (123) 456-78-90</a
          >
        </li>
        <li class="contacts-footer__item">
          <a href="mailto:info@ytyt.school" class="contacts-footer__link"
            ><img src="~assets/landing/img/icon-envelope.svg" alt="" class="contacts-footer__icon" />info@ytyt.school</a
          >
        </li>
      </ul>
      <ul class="footer__soc soc-footer">
        <li class="soc-footer__item">
          <a href="#" class="soc-footer__link">
            <img src="~assets/landing/img/soc-youtube.svg" alt="YouTube" class="soc-footer__icon" />
          </a>
        </li>
        <li class="soc-footer__item">
          <a href="#" class="soc-footer__link">
            <img src="~assets/landing/img/soc-vk.svg" alt="VK" class="soc-footer__icon" />
          </a>
        </li>
        <li class="soc-footer__item">
          <a href="#" class="soc-footer__link">
            <img src="~assets/landing/img/soc-fb.svg" alt="Facebook" class="soc-footer__icon" />
          </a>
        </li>
        <li class="soc-footer__item">
          <a href="#" class="soc-footer__link">
            <img src="~assets/landing/img/soc-instagram.svg" alt="Instagram" class="soc-footer__icon" />
          </a>
        </li>
      </ul>
    </div>
    <hr />
    <div class="footer__bottom container">
      <span class="footer__copyright">© Онлайн-школа программирования</span>
      <div class="footer__links">
        <a href="#">Пользовательское соглашение</a>
        <a href="#">Политика конфиденциальности</a>
      </div>
    </div>
  </footer>
</template>

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
    margin: 0 auto;
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
    &:last-child {
      margin-right: 0;
    }
  }

  // &__link {
  // }

  // &__icon {
  // }
}

@media screen and (max-width: 1140px) {
  .footer {
    &__top {
      justify-content: space-between;
      flex-wrap: wrap;
    }
    &__logo {
      margin-right: 0;
      margin-bottom: 30px;
    }
    &__information {
      flex: 0 0 50%;
      order: 3;
    }
    &__contacts {
      margin: 0;
      order: 2;
      margin-bottom: 30px;
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

@media screen and (max-width: $md) {
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

@media screen and (max-width: 575px) {
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
      margin-bottom: 20px;
      text-align: center;
    }
    &__contacts {
      margin: 0;
      order: 1;
      margin-bottom: 25px;
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
  }
}
</style>
