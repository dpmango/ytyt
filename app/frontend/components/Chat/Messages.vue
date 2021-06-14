<template>
  <div class="messages">
    <template v-if="messages">
      <div v-for="group in messagesByDate" :key="group.date" class="messages__group">
        <div class="messages__date">
          <span>{{ group.date }}</span>
        </div>
        <ChatMessage v-for="message in group.messages" :key="message.id" :message="message" />
      </div>
    </template>

    <div v-else class="messages__loader">
      <UiLoader :loading="true" theme="block" />
    </div>
  </div>
</template>

<script>
import groupBy from 'lodash/groupBy';
import { djs } from '~/helpers/Date';

export default {
  name: 'ChatMessages',
  props: {
    messages: Array,
  },
  computed: {
    messagesByDate() {
      const formatMask = 'DD MMM';

      const dates = this.messages.map((x) => djs(x.date_created).format(formatMask));
      const datesGrouped = Object.keys(groupBy(dates));

      return datesGrouped.map((date) => {
        const messages = this.messages.filter((message) => djs(message.date_created).format(formatMask) === date);
        return {
          date,
          messages,
        };
      });
    },
  },
  mounted() {
    if (document) {
      document.addEventListener('click', this.hideViewerOnClick, false);
    }
  },
  beforeDestroy() {
    if (document) {
      document.removeEventListener('click', this.hideViewerOnClick, false);
    }
  },
  methods: {
    hideViewerOnClick(e) {
      if (e.target.closest('.viewer-canvas')) {
        if (window.$viewer) {
          window.$viewer.hide();
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.messages {
  position: relative;
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 24px 24px 16px;
  // &__loader {

  // }
  &__date {
    position: relative;
    margin: 8px 0 16px 0;
    span {
      position: relative;
      padding-right: 12px;
      z-index: 2;
      background: #fafafa;
      font-size: 13px;
      line-height: 150%;
      color: rgb(#171818, 0.5);
    }
  }
}

@include r($sm) {
  .messages {
    padding: 16px;
  }
}
</style>
