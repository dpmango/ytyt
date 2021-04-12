import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const listService = async ($api, request) => {
  try {
    const { data } = await $api.get(endpoints.course.courses);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const themesService = async ($api, request) => {
  try {
    const { data } = await $api.get(endpoints.course.themes.replace(':id', request.id));

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const lessonsService = async ($api, request) => {
  try {
    const { data } = await $api.get(
      endpoints.course.lessons.replace(':course_id', request.course_id).replace(':theme_id', request.theme_id)
    );

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const lessonService = async ($api, request) => {
  try {
    const { data } = await $api.get(
      endpoints.course.lesson
        .replace(':course_id', request.course_id)
        .replace(':theme_id', request.theme_id)
        .replace(':fragment_id', request.fragment_id)
    );

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const compleateService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.course.complete.replace(':id', request.id));

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
