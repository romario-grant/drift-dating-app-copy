<script setup>
import { ref, onMounted } from "vue";
import { getNotifications, markNotificationRead } from "../services/api";

const notifications = ref([]);
const loading = ref(false);
const errorMessage = ref("");

const loadNotifications = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    notifications.value = await getNotifications();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

const handleMarkRead = async (notificationId) => {
  try {
    await markNotificationRead(notificationId);
    notifications.value = notifications.value.map((item) =>
      item.id === notificationId ? { ...item, is_read: true } : item
    );
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleString();
};

onMounted(() => {
  loadNotifications();
});
</script>

<template>
  <main class="dashboard">
    <aside class="sidebar">
      <nav>
        <RouterLink to="/dashboard">Browse</RouterLink>
        <RouterLink to="/me/profile">My Profile</RouterLink>
        <RouterLink to="/matches">Matches</RouterLink>
        <RouterLink to="/favorites">Favorites</RouterLink>
        <RouterLink to="/notifications">Notifications</RouterLink>
      </nav>
    </aside>

    <div class="dash">
      <h2>Notifications</h2>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      <p v-if="loading" class="loading-text">Loading notifications...</p>

      <div v-if="!loading" class="notifications-list">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification-card"
          :class="{ unread: !notification.is_read }"
        >
          <div class="notification-body">
            <h3>{{ notification.type }}</h3>
            <p>{{ notification.message }}</p>
            <small>{{ formatDate(notification.created_at) }}</small>
          </div>

          <div class="notification-actions">
            <button
              v-if="!notification.is_read"
              class="mark-btn"
              @click="handleMarkRead(notification.id)"
            >
              Mark as Read
            </button>

            <RouterLink
              v-if="notification.related_user_id"
              :to="`/message/${notification.related_user_id}`"
              class="message-link"
            >
              Open
            </RouterLink>
          </div>
        </div>

        <p v-if="notifications.length === 0" class="empty-text">
          No notifications yet.
        </p>
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

h2 {
  margin-bottom: 1rem;
  text-align: center;
}

.error-text {
  color: red;
  text-align: center;
}

.loading-text,
.empty-text {
  text-align: center;
}

.notifications-list {
  max-width: 850px;
  margin: 2rem auto 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification-card {
  background: white;
  border-radius: 18px;
  padding: 1rem 1.2rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.notification-card.unread {
  border-left: 6px solid #7c3aed;
}

.notification-body h3,
.notification-body p,
.notification-body small {
  margin: 0.2rem 0;
}

.notification-actions {
  display: flex;
  gap: 0.7rem;
  align-items: center;
  flex-wrap: wrap;
}

.mark-btn {
  border: none;
  border-radius: 10px;
  padding: 0.6rem 0.9rem;
  background: #2563eb;
  color: white;
  cursor: pointer;
}

.message-link {
  text-decoration: none;
  background: var(--primary-color);
  color: white;
  padding: 0.6rem 0.9rem;
  border-radius: 10px;
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

  .notification-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>