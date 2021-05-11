<template>
  <header class="header hero__header">
    <div class="header__container container">
      <a href="index.html" class="header__logo">
        <img src="~assets/landing/img/logo.svg" alt="YTYT Logo" />
      </a>
      <div class="header__menu menu">
        <div class="menu__icon">
          <span></span>
        </div>
        <nav class="menu__body">
          <ul class="menu__list">
            <li class="menu__item"><a data-goto=".study" href="#" class="menu__link">Формат обучения</a></li>
            <li class="menu__item"><a data-goto=".projects" href="#" class="menu__link">Результаты</a></li>
            <li class="menu__item"><a data-goto=".reviews" href="#" class="menu__link">Отзывы</a></li>
            <li class="menu__item"><a data-goto=".price" href="#" class="menu__link">Стоимость</a></li>
            <li class="menu__item"><a data-goto=".footer" href="#" class="menu__link">Контакты</a></li>
            <li class="menu__item menu__item-sign">
              <NuxtLink to="/auth/signup" class="menu__link">Вход/Зарегистрироваться</NuxtLink>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  mounted() {
    // Меню бургер
    const iconMenu = document.querySelector('.menu__icon');
    const menuBody = document.querySelector('.menu__body');
    if (iconMenu) {
      iconMenu.addEventListener('click', function (e) {
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
      });
    }

    // Плавная прокрутка к нужному разделу
    const menuLinks = document.querySelectorAll('.menu__link[data-goto]');
    if (menuLinks.length > 0) {
      menuLinks.forEach((menuLink) => {
        menuLink.addEventListener('click', onMenuLinkClick);
      });

      function onMenuLinkClick(e) {
        const menuLink = e.target;
        if (menuLink.dataset.goto && document.querySelector(menuLink.dataset.goto)) {
          const gotoBlock = document.querySelector(menuLink.dataset.goto);
          const gotoBlockValue = gotoBlock.getBoundingClientRect().top + pageYOffset;

          if (iconMenu.classList.contains('_active')) {
            document.body.classList.remove('_lock');
            iconMenu.classList.remove('_active');
            menuBody.classList.remove('_active');
          }

          window.scrollTo({
            top: gotoBlockValue,
            behavior: 'smooth',
          });
          e.preventDefault();
        }
      }
    }
  },
};
</script>
<style lang="scss" scoped>
.header {
  padding-top: 25px;
  margin-bottom: 35px;
  &__container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__logo {
    z-index: 5;
  }
}

.menu {
  &__icon {
    display: none;
  }

  &__body {
    display: flex;
  }

  &__list {
    display: flex;
    list-style: none;
  }

  &__item {
    margin-right: 25px;
    &:last-child {
      margin-right: 0;
    }
  }

  &__item-sign {
    display: none;
  }

  &__link {
    font-family: $baseFont;
    position: relative;
    color: #fff;
    font-size: 16px;
    text-decoration: none;
    opacity: 0.6;
    transition: 0.3s;
    &:hover {
      opacity: 1;
    }
    @media screen and (max-width: $lg) {
      font-size: 16px;
    }
  }
}

@media screen and (max-width: $md) {
  .menu__icon {
    display: block;
    position: relative;
    width: 30px;
    height: 18px;
    cursor: pointer;
    z-index: 5;
  }
  .menu__icon span,
  .menu__icon::before,
  .menu__icon::after {
    position: absolute;
    left: 0;
    width: 100%;
    height: 3px;
    border-radius: 5px;
    background-color: #8b8b8c;
    transition: 0.2s;
  }
  .menu__icon::before,
  .menu__icon::after {
    content: '';
  }
  .menu__icon::before {
    top: 0;
  }
  .menu__icon::after {
    bottom: 0;
  }
  .menu__icon span {
    top: 50%;
    transform: scale(1) translateY(-50%);
  }

  .menu__icon._active span {
    transform: scale(0) translateY(-50%);
  }
  .menu__icon._active::before {
    top: 50%;
    transform: rotate(45deg) translateY(-50%);
  }
  .menu__icon._active::after {
    top: 50%;
    transform: rotate(-45deg) translateY(-50%);
  }

  .menu {
    &__body {
      position: fixed;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.96);
      z-index: 4;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: flex-start;
      padding-top: 100px;
      padding-left: 15px;
      transition: left 0.3s ease 0s;
      overflow: auto;
      &._active {
        left: 0;
      }
    }
    &__list {
      flex-direction: column;
      margin-right: 0;
      margin-bottom: 50px;
    }
    &__item {
      margin-right: 0;
      margin-bottom: 25px;
      &:last-child {
        margin-bottom: 0;
      }
    }
    &__item-sign {
      display: block;
    }
    &__link {
      font-size: 18px;
    }
    &__call {
      font-size: 22px;
      padding-left: 38px;
      &::before {
        left: 0;
      }
    }
  }
}
</style>
