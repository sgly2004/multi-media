<template>
  <div class="chat-container">
    <div class="chat-header">
      <h3>与{{ artist.name }}对话</h3>
      <p class="artist-title">{{ artist.title }}</p>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(msg, index) in chatHistory" 
        :key="index"
        :class="['message', msg.type]"
      >
        <div class="message-content">{{ msg.content }}</div>
      </div>
    </div>
    
    <div class="chat-input">
      <select v-model="selectedQuestion">
        <option value="">选择一个问题...</option>
        <option 
          v-for="(conv, index) in artist.conversations" 
          :key="index" 
          :value="conv.question"
        >
          {{ conv.question }}
        </option>
      </select>
      <button 
        @click="sendMessage" 
        :disabled="!selectedQuestion"
      >发送</button>
    </div>
  </div>
</template>

<script>
import { mockArtists } from '../mock_data/artists'

export default {
  name: 'ArtistChat',
  props: {
    artistId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      artist: null,
      selectedQuestion: '',
      chatHistory: []
    }
  },
  methods: {
    sendMessage() {
      if (!this.selectedQuestion) return
      
      // 添加用户问题
      this.chatHistory.push({
        type: 'user',
        content: this.selectedQuestion
      })
      
      // 查找对应答案
      const conversation = this.artist.conversations.find(
        conv => conv.question === this.selectedQuestion
      )
      
      // 添加画师回答
      setTimeout(() => {
        this.chatHistory.push({
          type: 'artist',
          content: conversation.answer
        })
        this.scrollToBottom()
      }, 500)
      
      this.selectedQuestion = ''
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        container.scrollTop = container.scrollHeight
      })
    }
  },
  created() {
    this.artist = mockArtists.find(a => a.id === this.artistId)
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
}

.chat-header {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  background: #f5f5f5;
  border-radius: 8px 8px 0 0;
  flex-shrink: 0;
}

.chat-header h3 {
  margin: 0;
  color: #2c3e50;
  font-family: "KaiTi", serif;
}

.artist-title {
  margin: 5px 0 0 0;
  font-size: 12px;
  color: #666;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 200px;
}

.message {
  max-width: 80%;
}

.message.user {
  margin-left: auto;
}

.message-content {
  padding: 10px 15px;
  border-radius: 8px;
  background: #f0f0f0;
  line-height: 1.4;
}

.message.user .message-content {
  background: #8b0000;
  color: white;
}

.chat-input {
  padding: 15px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 10px;
  background: #fff;
  flex-shrink: 0;
}

select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  background: #fff;
  font-family: "KaiTi", serif;
}

select:focus {
  outline: none;
  border-color: #8b0000;
}

button {
  padding: 8px 20px;
  background: #8b0000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  font-family: "KaiTi", serif;
}

button:hover:not(:disabled) {
  background: #a00000;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style> 