<template>
  <section class="skills">
    <div class="container">
      <h2 class="skills__title">Вы получите все необходимые знания, <br />востребованные у работодателей</h2>
      <ul class="skills__list">
        <li class="skills__item">Python</li>
        <li class="skills__item">IDE PyCharm</li>
        <li class="skills__item">Работа с сетью</li>
        <li class="skills__item">REST API</li>
        <li class="skills__item">Базы данных, SQL</li>
        <li class="skills__item">Django, DRF</li>
        <li class="skills__item">Тестирование и отладка</li>
        <li class="skills__item">Git, Docker, Jira</li>
        <li class="skills__item">Чтение чужого кода, разбор legacy</li>
        <li class="skills__item">Паттерны проектирования</li>
        <li class="skills__item">Алгоритмы</li>
        <li class="skills__item">Linux</li>
      </ul>
      <div class="skills__description">
        Этот список - результат анализа 700+ реальных вакансий с hh.ru
        <div class="skills__help">
          <div class="skills__help-wrapper">
            <span class="skills__help-arrow"></span>
          </div>
          <span class="skills__help-info">
            Вакансии по запросу «Junior Python» по всей РФ за период январь-март 2021 г.
          </span>
        </div>
      </div>
      <NuxtLink to="/auth/signup" class="skills__button button">Пройти бесплатный вводный курс</NuxtLink>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.skills {
  background-color: $fontColor;
  color: #fff;
  text-align: center;
  padding-top: 70px;
  padding-bottom: 80px;
  margin-bottom: 70px;
  @include r($md) {
    padding-top: 32px;
    padding-bottom: 32px;
    margin-bottom: 40px;
  }
  &__title {
    font-size: 36px;
    font-weight: 500;
    margin-bottom: 50px;
    @include r($sm) {
      font-size: 27px;
      margin-bottom: 25px;
    }
  }

  &__list {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    list-style: none;
    margin-bottom: 15px;
    padding: 0 50px;
    @include r($lg) {
      padding: 0;
    }
  }

  &__item {
    background-color: rgba(#fff, 0.08);
    padding: 16px 20px;
    margin-right: 8px;
    margin-bottom: 8px;
    border-radius: 4px;
    transition: 0.2s;
    &:last-child {
      margin-right: 0;
    }
    &:hover {
      background-color: rgba(#fff, 0.16);
    }
  }

  &__description {
    position: relative;
    margin-bottom: 45px;
    color: rgba(#fff, 0.5);
  }

  &__help {
    position: relative;
    display: inline-block;
    background-image: url('~assets/landing/img/help-button.svg');
    width: 18px;
    height: 18px;
    cursor: pointer;
    vertical-align: middle;
    margin-left: 5px;
    opacity: 0.5;
    transition: 0.2s;
    &:hover {
      opacity: 1;
      .skills__help-arrow {
        display: block;
      }
      .skills__help-info {
        opacity: 1;
        pointer-events: all;
      }
    }
    @include r($lg) {
      position: static;
    }
  }
  &__help-wrapper {
    position: relative;
    height: 18px;
  }
  &__help-arrow {
    display: none;
    position: absolute;
    top: calc(100% + 7px);
    left: 50%;
    transform: translateX(-50%);
    background: url('~assets/landing/img/help-polygon.svg') no-repeat 50% 50%;
    width: 22px;
    height: 14px;
  }

  &__help-info {
    font-family: $baseFont;
    position: absolute;
    top: 100%;
    right: 50%;
    transform: translate(50%, 16px);
    background-color: #fff;
    color: #000;
    padding: 20px;
    border-radius: 8px;
    width: 440px;
    text-align: left;
    z-index: 2;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    @include r($lg) {
      width: 70%;
      box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    }
    @include r($md) {
      width: 100%;
      // top: 85%;
    }
  }
}
</style>
