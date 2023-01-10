import { configureStore } from '@reduxjs/toolkit';

import rootReducer from 'controller/redux/reducers';
import { ledStripsApi } from 'controller/redux/services/ledStripsApi';

import { SettingsState } from './slices/settingsSlice';

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(ledStripsApi.middleware)
});

export type RootState = {
    settings: SettingsState;
};
export type AppDispatch = typeof store.dispatch;

export default store;
