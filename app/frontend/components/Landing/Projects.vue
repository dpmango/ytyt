<template>
  <section class="projects">
    <div class="projects__container container">
      <div v-swiper="swiperConfig" class="slider swiper-container">
        <div class="slider__header header-slider">
          <h2 class="header-slider__title">Проекты, которые вы создадите</h2>
          <div slot="navigation" class="header-slider__nav">
            <div class="slider-button-prev"></div>
            <div class="slider-button-next"></div>
          </div>
        </div>
        <div class="projects__slider swiper-wrapper">
          <div v-for="slide in slides" :key="slide.id" class="swiper-slide projects__slide slide-project slider__slide">
            <a :href="slide.video" data-fancybox class="slide-project__preview">
              <img :src="slide.image" alt="" class="slide-project__bg" />
              <span class="slide-project__play button-play">
                <img src="~assets/landing/img/icon-play.svg" alt="" />
              </span>
            </a>
            <h3 class="slide-project__title">{{ slide.title }}</h3>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { directive } from 'vue-awesome-swiper';

export default {
  directives: {
    swiper: directive,
  },
  data() {
    return {
      swiperConfig: {
        setWrapperSize: false,
        normalizeSlideIndex: true,
        slideToClickedSlide: true,
        slidesPerView: 'auto',
        watchOverflow: true,
        threshold: 10,
        navigation: {
          nextEl: '.slider-button-next',
          prevEl: '.slider-button-prev',
        },
        breakpoints: {
          320: {
            spaceBetween: 15,
          },
          767: {
            spaceBetween: 25,
          },
          992: {
            spaceBetween: 40,
          },
        },
      },
      slides: [
        {
          id: 1,
          image: '/landing/img/project__img-1.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
        {
          id: 2,
          image: '/landing/img/project__img-2.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
        {
          id: 3,
          image: '/landing/img/project__img-3.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
        {
          id: 4,
          image: '/landing/img/project__img-1.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
        {
          id: 5,
          image: '/landing/img/project__img-3.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
        {
          id: 6,
          image: '/landing/img/project__img-2.png',
          video: 'https://www.youtube.com/watch?v=Zv11L-ZfrSg',
          title: 'Пишем первую программу на Python со сложными функциями',
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.projects {
  padding-top: 60px;
  margin-bottom: 70px;
  @include r($md) {
    margin-bottom: 40px;
    padding-top: 40px;
  }
  &__container {
    min-width: 0;
  }
}
.slide-project {
  &__preview {
    display: block;
    position: relative;
    height: 280px;
    border-radius: 8px;
    margin-bottom: 15px;
    overflow: hidden;
    &::before {
      display: inline-block;
      content: ' ';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(black, 0.3);
      opacity: 0;
      will-change: opacity;
      transition: opacity 0.25s $ease;
    }
    &:hover {
      &::before {
        opacity: 1;
      }
      .button-play {
        // animation-name: button-shadow-start;
        // animation-iteration-count: infinite;
        animation-play-state: running;
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
  }

  &__title {
    font-size: 20px;
    line-height: 1.5;
    font-weight: normal;
  }
}
</style>
