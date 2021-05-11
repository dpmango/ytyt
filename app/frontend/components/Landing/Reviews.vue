<template>
  <section class="reviews">
    <div class="reviews__container container">
      <div v-swiper="swiperConfig" class="slider swiper-container">
        <div class="slider__header header-slider">
          <h2 class="header-slider__title">Отзывы учеников</h2>
          <div class="header-slider__nav">
            <div class="slider-button-prev"></div>
            <div class="slider-button-next"></div>
          </div>
        </div>
        <div class="reviews__slider swiper-wrapper">
          <div v-for="slide in slides" :key="slide.id" class="swiper-slide reviews__slide slide-reviews slider__slide">
            <div class="slide-reviews__photo">
              <img :src="slide.avatar" :alt="slide.name" class="slide-reviews__img" />
            </div>
            <span class="slide-reviews__name">{{ slide.name }}</span>
            <div class="slide-reviews__text">
              <p v-html="slide.text"></p>
            </div>

            <a target="_blank" :href="slide.link" class="slide-reviews__link">{{ slide.link }}</a>
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
          avatar: '/landing/img/reviews__avatar.png',
          name: 'Александр Сидоров',
          text:
            'Таким образом рамки и место обучения кадров обеспечивает широкому кругу (специалистов) участие в формировании новых предложений. Не следует, однако забывать, что новая модель организационной деятельности влече.',
          link: 'https://sitename.com/url_1234567890',
        },
        {
          id: 2,
          avatar: '/landing/img/reviews__avatar.png',
          name: 'Александр Сидоров',
          text:
            'Таким образом рамки и место обучения кадров обеспечивает широкому кругу (специалистов) участие в формировании новых предложений. Не следует, однако забывать, что новая модель организационной деятельности влече.',
          link: 'https://sitename.com/url_1234567890',
        },
        {
          id: 3,
          avatar: '/landing/img/reviews__avatar.png',
          name: 'Александр Сидоров',
          text:
            'Таким образом рамки и место обучения кадров обеспечивает широкому кругу (специалистов) участие в формировании новых предложений. Не следует, однако забывать, что новая модель организационной деятельности влече.',
          link: 'https://sitename.com/url_1234567890',
        },
        {
          id: 4,
          avatar: '/landing/img/reviews__avatar.png',
          name: 'Александр Сидоров',
          text:
            'Таким образом рамки и место обучения кадров обеспечивает широкому кругу (специалистов) участие в формировании новых предложений. Не следует, однако забывать, что новая модель организационной деятельности влече.',
          link: 'https://sitename.com/url_1234567890',
        },
        {
          id: 5,
          avatar: '/landing/img/reviews__avatar.png',
          name: 'Александр Сидоров',
          text:
            'Таким образом рамки и место обучения кадров обеспечивает широкому кругу (специалистов) участие в формировании новых предложений. Не следует, однако забывать, что новая модель организационной деятельности влече.',
          link: 'https://sitename.com/url_1234567890',
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.reviews {
  margin-bottom: 70px;
  @media screen and (max-width: $md) {
    margin-bottom: 50px;
  }
}
.slide-reviews {
  &__photo {
    border-radius: 50%;
    overflow: hidden;
    height: 92px;
    width: 92px;
    margin-bottom: 16px;
  }

  &__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &__name {
    display: block;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 12px;
  }

  &__text {
    margin-bottom: 12px;
    p {
      line-height: 1.5;
    }
  }

  &__link {
    color: $colorPrimary;
    border-bottom: 1px solid transparent;
    transition: 0.2s;
    &:hover {
      border-bottom-color: $colorPrimary;
    }
  }
  @media screen and (max-width: 425px) {
    &__photo {
      margin-bottom: 15px;
    }
  }
}
</style>
