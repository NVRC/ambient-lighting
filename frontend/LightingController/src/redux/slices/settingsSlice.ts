import { createSlice } from "@reduxjs/toolkit";
import { useColorScheme as _useColorScheme, ColorSchemeName } from "react-native";
import { RootState } from "../store";



export type SettingsState = {
    loading: boolean;
    colorScheme: NonNullable<ColorSchemeName>;
};

const initialState: SettingsState = {
    colorScheme: "light",
    loading: true
}

const settingsSlice = createSlice({
    name: "settings",
    initialState,
    reducers: {},
    extraReducers(builder) {
        
    },
});

export const getSettings = (state: RootState): SettingsState => {
    return state.settings;
};

export default settingsSlice.reducer;