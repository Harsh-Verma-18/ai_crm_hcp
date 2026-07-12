import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { interactionApi } from '../api/client'

export const fetchInteractionsForHcp = createAsyncThunk(
  'interactions/fetchForHcp',
  async (hcpId) => {
    const data = await interactionApi.listForHcp(hcpId)
    return { hcpId, data }
  }
)

export const submitInteraction = createAsyncThunk(
  'interactions/submit',
  async (payload) => {
    return await interactionApi.create(payload)
  }
)

export const editInteraction = createAsyncThunk(
  'interactions/edit',
  async ({ id, payload }) => {
    return await interactionApi.update(id, payload)
  }
)

const interactionSlice = createSlice({
  name: 'interactions',
  initialState: {
    byHcpId: {}, // hcpId -> Interaction[]
    status: 'idle',
    submitStatus: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractionsForHcp.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(fetchInteractionsForHcp.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.byHcpId[action.payload.hcpId] = action.payload.data
      })
      .addCase(fetchInteractionsForHcp.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message
      })
      .addCase(submitInteraction.pending, (state) => {
        state.submitStatus = 'loading'
      })
      .addCase(submitInteraction.fulfilled, (state, action) => {
        state.submitStatus = 'succeeded'
        const hcpId = action.payload.hcp_id
        const existing = state.byHcpId[hcpId] || []
        state.byHcpId[hcpId] = [action.payload, ...existing]
      })
      .addCase(submitInteraction.rejected, (state, action) => {
        state.submitStatus = 'failed'
        state.error = action.error.message
      })
      .addCase(editInteraction.fulfilled, (state, action) => {
        const hcpId = action.payload.hcp_id
        const list = state.byHcpId[hcpId] || []
        state.byHcpId[hcpId] = list.map((i) =>
          i.id === action.payload.id ? action.payload : i
        )
      })
  },
})

export const selectInteractionsForHcp = (hcpId) => (state) =>
  state.interactions.byHcpId[hcpId] || []

export default interactionSlice.reducer
