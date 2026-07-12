import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { hcpApi } from '../api/client'

export const fetchHcps = createAsyncThunk('hcps/fetchAll', async () => {
  return await hcpApi.list()
})

const hcpSlice = createSlice({
  name: 'hcps',
  initialState: {
    items: [],
    selectedId: null,
    status: 'idle', // idle | loading | succeeded | failed
    error: null,
  },
  reducers: {
    selectHcp(state, action) {
      state.selectedId = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHcps.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(fetchHcps.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.items = action.payload
        if (!state.selectedId && action.payload.length > 0) {
          state.selectedId = action.payload[0].id
        }
      })
      .addCase(fetchHcps.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message
      })
  },
})

export const { selectHcp } = hcpSlice.actions
export const selectHcps = (state) => state.hcps.items
export const selectSelectedHcp = (state) =>
  state.hcps.items.find((h) => h.id === state.hcps.selectedId) || null

export default hcpSlice.reducer
