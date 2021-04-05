<template>
  <div class="container">
    <input type="text" placeholder="What needs to be done?" @keyup.enter="addTodo" />
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        <input :id="todo.id" :checked="todo.done" type="checkbox" @change="toggle(todo)" />
        <label :class="{ done: todo.done }" :for="todo.id">{{ todo.text }}</label>
        <button @click="removeTodo(todo)">remove</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  computed: {
    todos() {
      return this.$store.state.todos.list;
    },
  },
  methods: {
    addTodo(event) {
      this.$store.commit('todos/add', event.target.value);
      event.target.value = '';
    },
    ...mapMutations({
      toggle: 'todos/toggle',
    }),
    removeTodo(todo) {
      this.$store.commit('todos/remove', todo);
    },
  },
};
</script>

<style scoped>
ul {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

input[type='checkbox'] {
  margin: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.done {
  text-decoration: line-through;
}
</style>
