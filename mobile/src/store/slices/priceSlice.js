/**
 * Price Data Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { priceAPI } from '../services/api';

const initialState = {
  currentPrices: {},
  priceHistory: [],
  forecast: null,
  volatility: null,
  isLoading: false,
  error: null,
};

export const fetchCurrentPrices = createAsyncThunk(
  'price/fetchCurrent',
  async (commodity, { rejectWithValue }) => {
    try {
      const response = await priceAPI.getCurrentPrice(commodity);
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchPriceHistory = createAsyncThunk(
  'price/fetchHistory',
  async ({ commodity, days }, { rejectWithValue }) => {
    try {
      const response = await priceAPI.getPriceHistory(commodity, days);
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchForecast = createAsyncThunk(
  'price/fetchForecast',
  async ({ commodity, days }, { rejectWithValue }) => {
    try {
      const response = await priceAPI.getForecast(commodity, days);
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const priceSlice = createSlice({
  name: 'price',
  initialState,
  reducers: {
    clearPriceData: (state) => {
      state.priceHistory = [];
      state.forecast = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCurrentPrices.fulfilled, (state, action) => {
        state.currentPrices = action.payload;
      })
      .addCase(fetchPriceHistory.fulfilled, (state, action) => {
        state.priceHistory = action.payload;
      })
      .addCase(fetchForecast.fulfilled, (state, action) => {
        state.forecast = action.payload;
      });
  },
});

export const { clearPriceData } = priceSlice.actions;
export default priceSlice.reducer;
