import { createSlice, createAsyncThunk, nanoid } from '@reduxjs/toolkit'
import { chatApi } from '../api/client'

export const sendChatMessage = createAsyncThunk(
  'chat/send',
  async ({ message, threadId }) => {
    const data = await chatApi.send(message, threadId)
    return data
  }
)

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    threadId: nanoid(),
    messages: [], // { id, role: 'user' | 'assistant', text }
    status: 'idle', // idle | sending | failed
    error: null,
  },
  reducers: {
    resetThread(state) {
      state.threadId = nanoid()
      state.messages = []
      state.status = 'idle'
      state.error = null
    },
    queueUserMessage(state, action) {
      state.messages.push({ id: nanoid(), role: 'user', text: action.payload })
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.status = 'sending'
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = 'idle'
        state.messages.push({
          id: nanoid(),
          role: 'assistant',
          text: action.payload.answer,
        })
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message
        state.messages.push({
          id: nanoid(),
          role: 'assistant',
          text: "Something went wrong reaching the assistant. Check that the backend and Groq key are working, then try again.",
        })
      })
  },
})

export const { resetThread, queueUserMessage } = chatSlice.actions
export default chatSlice.reducer
