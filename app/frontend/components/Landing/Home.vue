<template>
  <div class="page page--homepage">
    <LandingHero />
    <LandingFeatures />
    <LandingStart />
    <LandingStudy />
    <LandingProjects />
    <LandingBenefits />
    <LandingSkills />
    <LandingReviews />
    <LandingPrice />
    <LandingFooter />
  </div>
</template>

<script>
export default {
  head() {
    return {
      link: [{ rel: 'stylesheet', href: '/landing/jquery.fancybox.min.css' }],
      script: [
        {
          src: '/landing/jquery-3.5.1.min.js',
        },
        {
          src: '/landing/jquery.fancybox.min.js',
        },
      ],
    };
  },
};
</script>

<style lang="scss">
@mixin font($font_name, $file_name, $weight, $style) {
  @font-face {
    font-family: $font_name;
    font-display: swap;
    src: url('~assets/landing/fonts/#{$file_name}.woff') format('woff'),
      url('~assets/landing/fonts/#{$file_name}.woff2') format('woff2');
    font-weight: #{$weight};
    font-style: #{$style};
  }
}

@include font('PTRootUI', 'PT-Root-UI_Regular', '400', 'normal');
@include font('PTRootUI', 'PT-Root-UI_Medium', '500', 'normal');
@include font('PTRootUI', 'PT-Root-UI_Bold', '700', 'normal');

body._lock {
  overflow: hidden;
}

.page--homepage {
  display: block;
  font-family: 'PTRootUI', 'Arial', sans-serif;
  font-size: 16px;
  line-height: normal;
  background-color: #fafafa;

  * {
    padding: 0;
    margin: 0;
    border: 0;
  }

  .container {
    max-width: 1320px;
    padding-left: 20px;
    padding-right: 20px;
    margin: 0 auto;
    @include r($md) {
      padding-left: 16px;
      padding-right: 16px;
    }
  }
  .visually-hidden {
    position: absolute;
    clip: rect(0 0 0 0);
    width: 1px;
    height: 1px;
    margin: -1px;
  }

  a {
    text-decoration: none;
  }
  h2 {
    font-size: 48px;
    @include r($md) {
      font-size: 34px;
      line-height: 1.1;
    }
  }

  .button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 64px;
    padding: 0 32px;
    background-color: $colorPrimary;
    color: #fff;
    font-size: 18px;
    font-weight: 500;
    border-radius: 8px;
    transition: 0.2s;
    &:hover {
      background-color: $colorPrimaryHover;
    }
  }

  .button-play {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    height: 85px;
    width: 85px;
    background-color: $colorPrimary;
    box-shadow: 0 0 0 16px rgba($colorPrimary, 0.5), 0 0 0 8px rgba($colorPrimary, 0.5);
    transition: background-color 0.2s;
    animation-name: button-shadow-start;
    animation-duration: 0.8s;
    animation-direction: alternate;
    animation-fill-mode: both;

    animation-iteration-count: infinite;
    animation-play-state: paused;
    &:hover {
      // animation-name: button-shadow-start;
      // animation-iteration-count: infinite;
      animation-play-state: running;
      background-color: $colorPrimaryHover;
    }

    @include r($md) {
      width: 52px;
      height: 52px;
      img {
        width: 18px;
      }
    }
  }

  .tabs {
    &__header {
      margin-bottom: 13px;
    }

    // &__content {
    // }
  }
  .header-tabs {
    display: flex;
    list-style: none;
    padding: 0;
    &__item {
      font-family: $baseFont;
      cursor: pointer;
      padding: 7px 16px;
      border-radius: 4px;
      transition: 0.2s;
      &.active {
        background-color: $fontColor;
        color: #fff;
      }
      &:hover:not(.active) {
        background-color: rgba($fontColor, 0.05);
      }
      @include r($mobile-s) {
        padding: 7px 12px;
      }
    }
  }
  .content-tabs {
    list-style: none;
    padding: 0;
    &__item {
      display: none;
      font-family: $baseFont;
      color: $fontColor;
      font-size: 54px;
      font-weight: 300;
      &.active {
        display: flex;
      }
      span {
        display: inline-block;
        color: $fontColor;
        opacity: 0.5;
        margin-left: 20px;
      }
    }

    @include r($mobile-s) {
      &__item {
        font-size: 30px;
      }
    }
  }

  .slider {
    &__header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 50px;
      @include r($md) {
        justify-content: flex-start;
        margin-bottom: 30px;
      }
    }
    &__slide {
      width: 360px;
      @include r(425) {
        width: 292px;
      }
    }
  }
  .header-slider {
    //  &__title {
    //  }

    &__nav {
      display: flex;
    }
    @include r($md) {
      &__nav {
        display: none;
      }
    }
  }
  .swiper-container {
    overflow: visible;
  }

  .slider-button-prev {
    background-image: url('~assets/landing/img/arrow-left.svg');
    width: 44px;
    height: 44px;
    cursor: pointer;
    margin-right: 18px;
    transition: 0.2s;
    &.swiper-button-disabled {
      opacity: 0.3;
    }
    &:hover {
      filter: brightness(87%);
    }
  }
  .slider-button-next {
    background-image: url('~assets/landing/img/arrow-right.svg');
    width: 44px;
    height: 44px;
    cursor: pointer;
    transition: 0.2s;
    &.swiper-button-disabled {
      opacity: 0.3;
    }
    &:hover {
      filter: brightness(87%);
    }
  }
  @keyframes button-shadow-start {
    0% {
      box-shadow: 0 0 0 16px rgba($colorPrimary, 0.5), 0 0 0 8px rgba($colorPrimary, 0.5);
    }
    100% {
      box-shadow: 0 0 0 24px rgba($colorPrimary, 0.1), 0 0 0 12px rgba($colorPrimary, 0.1);
    }
  }
  @keyframes button-shadow-end {
    0% {
      box-shadow: 0 0 0 24px rgba($colorPrimary, 0.1), 0 0 0 12px rgba($colorPrimary, 0.1);
    }
    100% {
      box-shadow: 0 0 0 16px rgba($colorPrimary, 0.5), 0 0 0 8px rgba($colorPrimary, 0.5);
    }
  }
}
</style>
