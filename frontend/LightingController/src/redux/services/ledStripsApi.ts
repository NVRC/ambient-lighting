import { ledStripsApi as _ledStripsApi } from "./auto_gen/ledStripsApi"

const TAG_UNKNOWN_ERROR = "UNKNOWN_ERROR";

// Configure endpoints to invalidate the cache per collection or id.
export const ledStripsApi = _ledStripsApi
    .enhanceEndpoints({
        addTagTypes: [TAG_UNKNOWN_ERROR],
    })
    .enhanceEndpoints({
        endpoints: {
            readStripStripsStripIdGet: {
                providesTags: (strip) => {
                    if (strip === undefined) {
                        return [ TAG_UNKNOWN_ERROR ]
                    }
                    let id = strip.id;
                    return [{ type: "strips" as const, id}, "strips"]
                }
            },
            postStripStripsStripIdPost: {
                invalidatesTags: (strip) => {
                    if (strip === undefined) {
                        return [ TAG_UNKNOWN_ERROR ]
                    }
                    let id = strip.id;
                    return [{ type: "strips" as const, id}, "strips"]
                }
            },
            postStripLedsStripsStripIdLedsPost: {
                invalidatesTags: (led_map, error, query_args) => {
                    if (led_map === undefined || error === undefined) {
                        return [ TAG_UNKNOWN_ERROR ]
                    }
                    const strip_id = query_args.stripId
                    return [{ type: "strips" as const, strip_id}, "leds"]

                }
            },
            postLedStripsStripIdLedsIndexIdPost: {
                invalidatesTags: (led, error, query_args) => {
                    if (led === undefined || error === undefined) {
                        return [ TAG_UNKNOWN_ERROR ]
                    }
                    const strip_id = query_args.stripId
                    return [{ type: "strips" as const, strip_id}, "leds"]
                }
            },
        }
    })

export const {
    useReadStripStripsStripIdGetQuery,
    usePostStripStripsStripIdPostMutation,
    useGetStripAnimationsStripsStripIdAnimateGetQuery,
    usePostStripAnimationStripsStripIdAnimatePostMutation,
    usePostStripLedsStripsStripIdLedsPostMutation,
    useReadLedStripsStripIdLedsIndexIdGetQuery,
    usePostLedStripsStripIdLedsIndexIdPostMutation,
    } = ledStripsApi;
      