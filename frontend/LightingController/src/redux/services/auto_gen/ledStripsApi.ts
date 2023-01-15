import { emptySplitApi as api } from "./emptyApi";
export const addTagTypes = ["strips", "leds"] as const;
const injectedRtkApi = api
  .enhanceEndpoints({
    addTagTypes,
  })
  .injectEndpoints({
    endpoints: (build) => ({
      readStripStripsStripIdGet: build.query<
        ReadStripStripsStripIdGetApiResponse,
        ReadStripStripsStripIdGetApiArg
      >({
        query: (queryArg) => ({ url: `/strips/${queryArg.stripId}` }),
        providesTags: ["strips"],
      }),
      postStripStripsStripIdPost: build.mutation<
        PostStripStripsStripIdPostApiResponse,
        PostStripStripsStripIdPostApiArg
      >({
        query: (queryArg) => ({
          url: `/strips/${queryArg.stripId}`,
          method: "POST",
          body: queryArg.strip,
        }),
        invalidatesTags: ["strips"],
      }),
      getStripAnimationsStripsStripIdAnimateGet: build.query<
        GetStripAnimationsStripsStripIdAnimateGetApiResponse,
        GetStripAnimationsStripsStripIdAnimateGetApiArg
      >({
        query: (queryArg) => ({ url: `/strips/${queryArg.stripId}/animate` }),
        providesTags: ["strips"],
      }),
      postStripAnimationStripsStripIdAnimatePost: build.mutation<
        PostStripAnimationStripsStripIdAnimatePostApiResponse,
        PostStripAnimationStripsStripIdAnimatePostApiArg
      >({
        query: (queryArg) => ({
          url: `/strips/${queryArg.stripId}/animate`,
          method: "POST",
          body: queryArg.animationDetails,
        }),
        invalidatesTags: ["strips"],
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
        invalidatesTags: ["strips", "leds"],
      }),
      readLedStripsStripIdLedsIndexIdGet: build.query<
        ReadLedStripsStripIdLedsIndexIdGetApiResponse,
        ReadLedStripsStripIdLedsIndexIdGetApiArg
      >({
        query: (queryArg) => ({
          url: `/strips/${queryArg.stripId}/leds/${queryArg.indexId}`,
        }),
        providesTags: ["strips", "leds"],
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
        invalidatesTags: ["strips", "leds"],
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
  strip: Strip;
};
export type GetStripAnimationsStripsStripIdAnimateGetApiResponse =
  /** status 200 Successful Response */ AnimationDetails[];
export type GetStripAnimationsStripsStripIdAnimateGetApiArg = {
  stripId: number;
};
export type PostStripAnimationStripsStripIdAnimatePostApiResponse =
  /** status 200 Successful Response */ AnimationDetails;
export type PostStripAnimationStripsStripIdAnimatePostApiArg = {
  stripId: number;
  animationDetails: AnimationDetails;
};
export type PostStripLedsStripsStripIdLedsPostApiResponse =
  /** status 201 Successful Response */ {
    [key: string]: Led;
  };
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
  /** status 201 Successful Response */ Led;
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
  id: number;
  brightness: number;
  number_of_leds: number;
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
export type AnimationType = "SHIFT" | "GRADIENT_POLYLINEAR_INTERPOLATION";
export type AnimationDetails = {
  animation_type: AnimationType;
  settings: object;
};
export const {
  useReadStripStripsStripIdGetQuery,
  usePostStripStripsStripIdPostMutation,
  useGetStripAnimationsStripsStripIdAnimateGetQuery,
  usePostStripAnimationStripsStripIdAnimatePostMutation,
  usePostStripLedsStripsStripIdLedsPostMutation,
  useReadLedStripsStripIdLedsIndexIdGetQuery,
  usePostLedStripsStripIdLedsIndexIdPostMutation,
} = injectedRtkApi;
