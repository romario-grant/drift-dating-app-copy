<script setup>
import { ref, onMounted } from "vue";
import { getFavorites, removeFavorite, getSingleProfile } from "../services/api";

const favorites = ref([]);
const loading = ref(false);
const errorMessage = ref("");

const selectedProfile = ref(null);
const modalLoading = ref(false);

const formatName = (name) => {
  if (!name) return "Unknown";
  return name
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
};

const imageUrl = (path) => {
  if (!path) return new URL("../assets/pics/default.webp", import.meta.url).href;
  return `http://localhost:5000${path}`;
};

const loadFavorites = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    favorites.value = await getFavorites();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

const handleRemove = async (userId) => {
  try {
    await removeFavorite(userId);
    favorites.value = favorites.value.filter((item) => item.user_id !== userId);
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const openProfileModal = async (userId) => {
  modalLoading.value = true;
  selectedProfile.value = null;

  try {
    selectedProfile.value = await getSingleProfile(userId);
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    modalLoading.value = false;
  }
};

const closeProfileModal = () => {
  selectedProfile.value = null;
};

onMounted(() => {
  loadFavorites();
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
      </nav>
    </aside>

    <div class="dash">
      <h2>My Favorites</h2>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      <p v-if="loading" class="loading-text">Loading favorites...</p>

      <section class="section-team">
        <div class="wrapper">
          <div class="team">
            <div class="profile-card" v-for="favorite in favorites" :key="favorite.id">
              <figure class="img-box clickable" @click="openProfileModal(favorite.user_id)">
                <img :src="imageUrl(favorite.profile_picture)" alt="profile picture" />
              </figure>

              <div class="info">
                <div class="left clickable" @click="openProfileModal(favorite.user_id)">
                  <h3>
                    {{ formatName(favorite.display_name) }}
                    <span v-if="favorite.age">, {{ favorite.age }}</span>
                  </h3>
                  <p v-if="favorite.bio">{{ favorite.bio }}</p>
                  <p v-if="favorite.location">{{ favorite.location }}</p>
                </div>

                <div class="action-row">
                  <RouterLink :to="`/message/${favorite.user_id}`" class="reset-btn message-btn">
                    Message
                  </RouterLink>
                  <button class="reset-btn remove-btn" @click="handleRemove(favorite.user_id)">
                    Remove
                  </button>
                </div>
              </div>
            </div>

            <p v-if="!loading && favorites.length === 0" class="empty-text">
              No favorites yet.
            </p>
          </div>
        </div>
      </section>
    </div>

    <div
      v-if="selectedProfile || modalLoading"
      class="modal-overlay"
      @click.self="closeProfileModal"
    >
      <div class="modal-card">
        <button class="close-btn" @click="closeProfileModal">×</button>

        <p v-if="modalLoading">Loading profile...</p>

        <template v-if="selectedProfile">
          <img
            class="modal-image"
            :src="imageUrl(selectedProfile.profile_picture)"
            alt="profile picture"
          />
          <h2>
            {{ formatName(selectedProfile.display_name) }}
            <span v-if="selectedProfile.age">, {{ selectedProfile.age }}</span>
          </h2>

          <p v-if="selectedProfile.bio">{{ selectedProfile.bio }}</p>
          <p v-if="selectedProfile.location">Location: {{ selectedProfile.location }}</p>
          <p v-if="selectedProfile.gender">Gender: {{ selectedProfile.gender }}</p>
          <p v-if="selectedProfile.looking_for">Looking for: {{ selectedProfile.looking_for }}</p>

          <p
            v-if="selectedProfile.interests && selectedProfile.interests.length"
            class="interests-text"
          >
            Interests: {{ selectedProfile.interests.join(", ") }}
          </p>

          <p class="match-score">Match Score: {{ selectedProfile.match_score }}%</p>
        </template>
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
  margin-top: 1rem;
  text-align: center;
}

.loading-text,
.empty-text {
  margin-top: 1rem;
  text-align: center;
}

.team {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 340px));
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}

.profile-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.2rem;
}

.img-box {
  display: flex;
  justify-content: center;
  background-color: #f3f4f6;
  border-radius: 20px;
  width: 160px;
  height: 160px;
  overflow: hidden;
}

.img-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clickable {
  cursor: pointer;
}

.info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.left h3,
.left p {
  margin: 0;
}

.action-row {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  justify-content: center;
}

.message-btn {
  background: var(--primary-color);
  text-decoration: none;
}

.remove-btn {
  background: #dc2626;
}

.interests-text {
  color: #374151;
  font-size: 0.95rem;
}

.match-score {
  font-weight: 700;
  color: #f59e0b;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-card {
  background: white;
  width: 90%;
  max-width: 450px;
  border-radius: 24px;
  padding: 2rem;
  position: relative;
  text-align: center;
}

.modal-image {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 20px;
  margin-bottom: 1rem;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 16px;
  border: none;
  background: transparent;
  font-size: 2rem;
  cursor: pointer;
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
}
</style>