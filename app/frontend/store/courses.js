import { listService, themesService, lessonsService, lessonService, compleateService } from '~/api/courses';

export const state = () => ({
  courses: [],
  // courses: new Map(),
});

export const getters = {
  courses: (state) => {
    return state.courses;
  },
};

export const mutations = {
  setCourses(state, courses) {
    state.courses = courses;
  },
  setThemes(state, { course_id, themes }) {
    // state.courses = [
    //   ...state.courses,
    // ]
  },
  add(state, course) {
    state.courses.push(course);
  },
  remove(state, id) {
    state.courses = state.courses.filter((course) => course.id !== id);
  },
};

export const actions = {
  async list({ commit }, request) {
    const [err, result] = await listService(this.$api, request);

    if (err) throw err;

    commit('setCourses', result);

    return result;
  },
  async themes({ commit }, request) {
    const [err, result] = await themesService(this.$api, request);

    if (err) throw err;

    // commit('setThemes', { course_id: request.id, themes: result });

    return result;
  },
  async lessons({ commit }, request) {
    const [err, result] = await lessonsService(this.$api, request);

    if (err) throw err;

    // commit('setThemes', { course_id: request.id, themes: result });

    return result;
  },
  async lesson({ commit }, request) {
    const [err, result] = await lessonService(this.$api, request);

    if (err) throw err;

    // commit('setThemes', { course_id: request.id, themes: result });

    return result;
  },
  async compleate({ commit }, request) {
    const [err, result] = await compleateService(this.$api, request);

    if (err) throw err;

    // commit('setThemes', { course_id: request.id, themes: result });

    return result;
  },
};
