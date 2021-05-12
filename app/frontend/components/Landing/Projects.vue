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
            <div class="slide-project__preview">
              <img :src="slide.image" alt="" class="slide-project__bg" />
              <a :href="slide.video" data-fancybox class="slide-project__play button-play">
                <img src="~assets/landing/img/icon-play.svg" alt="" />
              </a>
            </div>
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
    position: relative;
    height: 280px;
    border-radius: 8px;
    margin-bottom: 15px;
    overflow: hidden;
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
    font-weight: normal;
  }
}
</style>
