/**
 * Contract Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { contractAPI } from '../services/api';

const initialState = {
  contracts: [],
  activeContracts: [],
  summary: null,
  isLoading: false,
  error: null,
};

export const fetchContracts = createAsyncThunk(
  'contract/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await contractAPI.getUserContracts();
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const createContract = createAsyncThunk(
  'contract/create',
  async (contractData, { rejectWithValue }) => {
    try {
      const response = await contractAPI.createContract(contractData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchContractSummary = createAsyncThunk(
  'contract/fetchSummary',
  async (_, { rejectWithValue }) => {
    try {
      const response = await contractAPI.getContractSummary();
      return response;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const contractSlice = createSlice({
  name: 'contract',
  initialState,
  reducers: {
    clearContracts: (state) => {
      state.contracts = [];
      state.summary = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchContracts.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchContracts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.contracts = action.payload;
        state.activeContracts = action.payload.filter(c => c.status === 'active');
      })
      .addCase(fetchContracts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(createContract.fulfilled, (state, action) => {
        state.contracts.push(action.payload);
      })
      .addCase(fetchContractSummary.fulfilled, (state, action) => {
        state.summary = action.payload;
      });
  },
});

export const { clearContracts } = contractSlice.actions;
export default contractSlice.reducer;
