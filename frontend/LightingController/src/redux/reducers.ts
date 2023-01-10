import { combineReducers } from '@reduxjs/toolkit';

import { ledStripsApi } from 'controller/redux/services/ledStripsApi';
import settingsReducer from 'controller/redux/slices/settingsSlice';

const rootReducer = combineReducers({
  [ledStripsApi.reducerPath]: ledStripsApi.reducer,
  settings: settingsReducer
  // TODO: #13 add global error state reducer
});

export default rootReducer;
