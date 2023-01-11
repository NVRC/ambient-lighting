import { emptySplitApi as api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    readStripStripsStripIdGet: build.query<
      ReadStripStripsStripIdGetApiResponse,
      ReadStripStripsStripIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/strips/${queryArg.stripId}` }),
    }),
    postStripStripsStripIdPost: build.mutation<
      PostStripStripsStripIdPostApiResponse,
      PostStripStripsStripIdPostApiArg
    >({
      query: (queryArg) => ({
        url: `/strips/${queryArg.stripId}`,
        method: "POST",
      }),
    }),
    postStripLedsStripsStripIdLedsPost: build.mutation<
      PostStripLedsStripsStripIdLedsPostApiResponse,
      PostStripLedsStripsStripIdLedsPostApiArg
    >({
      query: (queryArg) => ({
        url: `/strips/${queryArg.stripId}/leds`,
        method: "POST",
        body: queryArg.body,
      }),
    }),
    readLedStripsStripIdLedsIndexIdGet: build.query<
      ReadLedStripsStripIdLedsIndexIdGetApiResponse,
      ReadLedStripsStripIdLedsIndexIdGetApiArg
    >({
      query: (queryArg) => ({
        url: `/strips/${queryArg.stripId}/leds/${queryArg.indexId}`,
      }),
    }),
    postLedStripsStripIdLedsIndexIdPost: build.mutation<
      PostLedStripsStripIdLedsIndexIdPostApiResponse,
      PostLedStripsStripIdLedsIndexIdPostApiArg
    >({
      query: (queryArg) => ({
        url: `/strips/${queryArg.stripId}/leds/${queryArg.indexId}`,
        method: "POST",
        body: queryArg.led,
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as ledStripsApi };
export type ReadStripStripsStripIdGetApiResponse =
  /** status 200 Successful Response */ Strip;
export type ReadStripStripsStripIdGetApiArg = {
  stripId: number;
};
export type PostStripStripsStripIdPostApiResponse =
  /** status 201 Successful Response */ Strip;
export type PostStripStripsStripIdPostApiArg = {
  stripId: number;
};
export type PostStripLedsStripsStripIdLedsPostApiResponse =
  /** status 201 Successful Response */ any;
export type PostStripLedsStripsStripIdLedsPostApiArg = {
  stripId: number;
  body: {
    [key: string]: Led;
  };
};
export type ReadLedStripsStripIdLedsIndexIdGetApiResponse =
  /** status 200 Successful Response */ Led;
export type ReadLedStripsStripIdLedsIndexIdGetApiArg = {
  stripId: number;
  indexId: number;
};
export type PostLedStripsStripIdLedsIndexIdPostApiResponse =
  /** status 201 Successful Response */ any;
export type PostLedStripsStripIdLedsIndexIdPostApiArg = {
  stripId: number;
  indexId: number;
  led: Led;
};
export type Rgb = {
  red: number;
  green: number;
  blue: number;
};
export type Led = {
  color: Rgb;
};
export type Strip = {
  id?: number;
  brightness?: number;
  leds: {
    [key: string]: Led;
  };
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export const {
  useReadStripStripsStripIdGetQuery,
  usePostStripStripsStripIdPostMutation,
  usePostStripLedsStripsStripIdLedsPostMutation,
  useReadLedStripsStripIdLedsIndexIdGetQuery,
  usePostLedStripsStripIdLedsIndexIdPostMutation,
} = injectedRtkApi;
