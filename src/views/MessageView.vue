<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from "vue";
import {
  getMessages,
  sendMessage,
  getMatches,
  getCurrentUser,
} from "../services/api";

const props = defineProps({
  userId: {
    type: [String, Number],
    required: true,
  },
});

const messages = ref([]);
const matches = ref([]);
const currentUser = ref(null);
const newMessage = ref("");
const loading = ref(false);
const errorMessage = ref("");
const selectedMatch = ref(null);

let refreshInterval = null;

const formatName = (name) => {
  if (!name) return "Unknown";

  return name
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
};

const loadMessagesOnly = async () => {
  try {
    const numericUserId = Number(props.userId);
    messages.value = await getMessages(numericUserId);
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const loadPageData = async () => {
  loading.value = true;
  errorMessage.value = "";
  selectedMatch.value = null;
  messages.value = [];

  try {
    const numericUserId = Number(props.userId);

    const [matchesData, userData] = await Promise.all([
      getMatches(),
      getCurrentUser(),
    ]);

    matches.value = matchesData;
    currentUser.value = userData;
    selectedMatch.value =
      matchesData.find((match) => match.user_id === numericUserId) || null;

    if (!selectedMatch.value) {
      errorMessage.value = "Match not found.";
      return;
    }

    await loadMessagesOnly();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

const handleSend = async () => {
  if (!newMessage.value.trim()) return;

  try {
    const numericUserId = Number(props.userId);
    await sendMessage(numericUserId, { content: newMessage.value });
    newMessage.value = "";
    await loadMessagesOnly();
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const startAutoRefresh = () => {
  clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    if (selectedMatch.value) {
      loadMessagesOnly();
    }
  }, 3000);
};

onMounted(async () => {
  await loadPageData();
  startAutoRefresh();
});

watch(
  () => props.userId,
  async () => {
    await loadPageData();
    startAutoRefresh();
  },
);

onBeforeUnmount(() => {
  clearInterval(refreshInterval);
});
</script>

<template>
  <main class="dashboard">
    <aside class="sidebar">
      <nav>
        <RouterLink to="/dashboard">Browse</RouterLink>
        <RouterLink to="/matches">Matches</RouterLink>
      </nav>
    </aside>

    <div class="dash">
      <RouterLink to="/matches" class="back-btn">← Back to Matches</RouterLink>

      <div class="message-layout">
        <aside class="conversation-list">
          <h3>Conversations</h3>

          <RouterLink
            v-for="match in matches"
            :key="match.match_id"
            :to="`/message/${match.user_id}`"
            class="conversation-item"
            :class="{ active: Number(props.userId) === match.user_id }"
          >
            {{ formatName(match.display_name) }}
          </RouterLink>
        </aside>

        <section class="chat-panel">
          <h2 v-if="selectedMatch">
            Chat with {{ formatName(selectedMatch.display_name) }}
          </h2>

          <p v-if="errorMessage" class="error-text">
            {{ errorMessage }}
          </p>
          <p v-if="loading" class="loading-text">Loading conversation...</p>

          <section v-if="selectedMatch && !loading" class="chat-section">
            <div class="chat-header">
              <figure class="img-box">
                <img src="../assets/pics/default.webp" alt="profile picture" />
              </figure>

              <div class="match-info">
                <h3>
                  {{ formatName(selectedMatch.display_name) }}
                  <span v-if="selectedMatch.age"
                    >, {{ selectedMatch.age }}</span
                  >
                </h3>
                <p v-if="selectedMatch.location">
                  {{ selectedMatch.location }}
                </p>
              </div>
            </div>

            <div class="messages-box">
              <div
                v-for="message in messages"
                :key="message.id"
                :class="[
                  'message-bubble',
                  message.sender_id === currentUser?.id
                    ? 'my-message'
                    : 'their-message',
                ]"
              >
                {{ message.content }}
              </div>

              <p v-if="messages.length === 0" class="empty-text">
                No messages yet. Start the conversation.
              </p>
            </div>

            <form class="message-form" @submit.prevent="handleSend">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
              />
              <button class="reset-btn mess" type="submit">Send</button>
            </form>
          </section>
        </section>
      </div>
    </div>
  </main>
</template>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: 0.6fr 4fr;
  min-height: 100vh;
}

.dash {
  padding: 2.4rem;
}

.sidebar {
  padding: 2rem;
  background: var(--secondary-color);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar a {
  text-decoration: none;
  color: #ffffff;
  font-weight: 600;
}

.back-btn {
  display: inline-block;
  margin-bottom: 1rem;
  text-decoration: none;
  color: var(--primary-color);
  font-weight: 700;
}

.message-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 1.5rem;
  align-items: start;
}

.conversation-list {
  background: #ffffff;
  border-radius: 24px;
  padding: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.conversation-list h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  text-align: center;
}

.conversation-item {
  display: block;
  padding: 0.8rem 1rem;
  border-radius: 14px;
  text-decoration: none;
  color: #111827;
  margin-bottom: 0.6rem;
  background: #f3f4f6;
  font-weight: 600;
}

.conversation-item.active {
  background: var(--primary-color);
  color: white;
}

.chat-panel h2 {
  margin-bottom: 1rem;
  text-align: center;
}

.error-text {
  color: red;
  margin-top: 1rem;
  text-align: center;
}

.loading-text,
.empty-text {
  margin-top: 1rem;
  text-align: center;
}

.chat-section {
  max-width: 600px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.img-box {
  display: flex;
  justify-content: center;
  background-color: #f3f4f6;
  border-radius: 20px;
  width: 90px;
  height: 90px;
  overflow: hidden;
}

.img-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-info h3,
.match-info p {
  margin: 0;
}

.messages-box {
  min-height: 320px;
  max-height: 420px;
  overflow-y: auto;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.message-bubble {
  max-width: 70%;
  padding: 0.8rem 1rem;
  border-radius: 18px;
  font-size: 0.95rem;
  word-break: break-word;
}

.my-message {
  align-self: flex-end;
  background-color: var(--primary-color);
  color: white;
}

.their-message {
  align-self: flex-start;
  background-color: #e5e7eb;
  color: #111827;
}

.message-form {
  display: flex;
  gap: 0.8rem;
  margin-top: 1rem;
}

.message-form input {
  flex: 1;
  padding: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 12px;
}

.mess {
  background-color: var(--primary-color);
}

@media (max-width: 900px) {
  .dashboard {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .sidebar nav {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }

  .message-layout {
    grid-template-columns: 1fr;
  }

  .chat-header {
    flex-direction: column;
    text-align: center;
  }

  .message-form {
    flex-direction: column;
  }

  .message-bubble {
    max-width: 85%;
  }
}
</style>
