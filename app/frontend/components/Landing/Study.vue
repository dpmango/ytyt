<template>
  <section class="study">
    <h2 class="visually-hidden">Формат обучения</h2>
    <div class="study__container container">
      <div class="study__video video-study">
        <a class="video-study__preview" href="https://www.youtube.com/watch?v=Zv11L-ZfrSg" data-fancybox>
          <img src="~assets/landing/img/video__preview.png" class="video-study__bg" alt="" />
          <span class="video-study__play button-play">
            <img src="~assets/landing/img/icon-play.svg" alt="" />
          </span>
        </a>
        <p class="video-study__description">Процесс обучения на&nbsp;нашей платформе</p>
      </div>
      <ul class="study__features features-study">
        <li class="features-study__item">
          <strong>Учитесь, когда вам удобно.</strong> Никаких &laquo;потоков&raquo;, &laquo;групп&raquo;
          и&nbsp;временных рамок.
        </li>
        <li class="features-study__item">
          <strong>Занимайтесь с&nbsp;любого устройства</strong>&nbsp;&mdash; компьютер, планшет, телефон.
        </li>
        <li class="features-study__item">
          <strong>От&nbsp;30&nbsp;минут в&nbsp;день</strong>&nbsp;&mdash; весь материал разбит на&nbsp;короткие
          структурированные уроки.
        </li>
        <li class="features-study__item">
          <strong>Задавайте вопросы</strong>&nbsp;&mdash; наставник ответит вам в&nbsp;чате.
        </li>
      </ul>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.study {
  background-color: #fff;
  padding-top: 120px;
  padding-bottom: 70px;
  @include r($lg) {
    padding-top: 90px;
  }
  @include r($md) {
    padding-bottom: 50px;
  }
  &__container {
    display: flex;
    align-items: center;
  }

  &__video {
    flex: 0 0 50%;
  }

  &__features {
    margin-left: 50px;
  }
}
.video-study {
  &__preview {
    display: block;
    position: relative;
    z-index: 1;
    border-radius: 8px;
    padding-bottom: 55.9%;
    margin-bottom: 12px;
    overflow: hidden;
    &::before {
      display: inline-block;
      content: ' ';
      position: absolute;
      z-index: 2;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(black, 0.3);
      opacity: 0;
      will-change: opacity;
      transition: opacity 0.25s $ease;
    }
    > img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      z-index: 1;
    }
    &:hover {
      &::before {
        opacity: 1;
      }
      .button-play {
        animation-play-state: running;
        // animation-name: button-shadow-start;
        // animation-iteration-count: infinite;
        background-color: $colorPrimaryHover;
      }
    }
  }

  &__bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &__play {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
  }

  &__description {
    color: #171818;
    font-family: 'Roboto', sans-serif;
    opacity: 0.5;
    @include r($sm) {
      font-size: 14px;
      text-align: center;
    }
  }
}
.features-study {
  list-style: none;
  max-width: 40%;
  @include r($lg) {
    max-width: 100%;
  }
  &__item {
    position: relative;
    font-size: 20px;
    line-height: 1.5;
    margin-bottom: 20px;
    padding-left: 44px;
    @include r($lg) {
      font-size: 18px;
      padding-left: 36px;
    }
    &:last-child {
      margin-bottom: 0;
    }
    &::before {
      content: '';
      position: absolute;
      top: 5px;
      left: 0;
      border-radius: 50%;
      border: 2px solid $colorRed;
      width: 24px;
      height: 24px;
      @include r($lg) {
        width: 20px;
        height: 20px;
      }
    }
  }
}

@include r($lg) {
  .study {
    &__container {
      flex-wrap: wrap;
    }
    &__video {
      flex: 0 0 100%;
      order: 2;
    }
    &__features {
      margin-left: 0;
      margin-bottom: 24px;
      order: 1;
    }
  }
}
</style>
