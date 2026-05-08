<script setup>
import { ref, onMounted } from "vue";
import {
  getProfiles,
  likeUser,
  passUser,
  getSingleProfile,
  addFavorite
} from "../services/api";

const profiles = ref([]);
const errorMessage = ref("");
const loading = ref(false);

const selectedProfile = ref(null);
const modalLoading = ref(false);

const filters = ref({
  search: "",
  location: "",
  min_age: "",
  max_age: "",
  interest: "",
});

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

const loadProfiles = async () => {
  errorMessage.value = "";
  loading.value = true;

  try {
    profiles.value = await getProfiles(filters.value);
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

const resetFilters = async () => {
  filters.value = {
    search: "",
    location: "",
    min_age: "",
    max_age: "",
    interest: "",
  };
  await loadProfiles();
};

const handleLike = async (userId) => {
  try {
    const result = await likeUser(userId);
    profiles.value = profiles.value.filter((profile) => profile.user_id !== userId);

    if (result.match_created) {
      alert("It's a match!");
    }
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const handlePass = async (userId) => {
  try {
    await passUser(userId);
    profiles.value = profiles.value.filter((profile) => profile.user_id !== userId);
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const handleFavorite = async (userId) => {
  try {
    await addFavorite(userId);
    alert("Added to favorites.");
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
  loadProfiles();
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
      <div class="container">
        <h2>Browse Potential Matches</h2>

        <div class="filters">
          <input
            v-model="filters.search"
            type="text"
            placeholder="Search by name or bio..."
          />
          <input
            v-model="filters.location"
            type="text"
            placeholder="Filter by location..."
          />
          <input
            v-model="filters.min_age"
            type="number"
            placeholder="Min age"
          />
          <input
            v-model="filters.max_age"
            type="number"
            placeholder="Max age"
          />
          <input
            v-model="filters.interest"
            type="text"
            placeholder="Interest..."
          />
        </div>

        <div class="fil">
          <button class="cta" @click="loadProfiles" type="button">
            Apply Filters
          </button>
          <button class="cta" data-cta-style="line" @click="resetFilters" type="button">
            Reset Filters
          </button>
        </div>

        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
        <p v-if="loading" class="loading-text">Loading profiles...</p>
      </div>

      <section class="section-team">
        <div class="wrapper">
          <div class="team">
            <div class="profile-card" v-for="profile in profiles" :key="profile.id">
              <figure class="img-box clickable" @click="openProfileModal(profile.user_id)">
                <img :src="imageUrl(profile.profile_picture)" alt="profile picture" />
              </figure>

              <div class="info">
                <div class="left clickable" @click="openProfileModal(profile.user_id)">
                  <h3>
                    {{ formatName(profile.display_name) }}
                    <span v-if="profile.age">, {{ profile.age }}</span>
                  </h3>

                  <p v-if="profile.bio">{{ profile.bio }}</p>
                  <p v-if="profile.location">{{ profile.location }}</p>

                  <p
                    v-if="profile.interests && profile.interests.length"
                    class="interests-text"
                  >
                    Interests: {{ profile.interests.join(", ") }}
                  </p>

                  <p
                    v-if="profile.shared_interest_count > 0"
                    class="shared-interest"
                  >
                    Shared interests: {{ profile.shared_interest_count }}
                  </p>

                  <p v-if="profile.looking_for" class="txt-p-clr">
                    Looking for: {{ profile.looking_for }}
                  </p>

                  <p class="match-score">
                    Match Score: {{ profile.match_score }}%
                  </p>
                </div>

                <div class="rate-btns">
                  <button
                    class="reset-btn favorite"
                    type="button"
                    @click="handleFavorite(profile.user_id)"
                  >
                    Favorite
                  </button>
                  <button
                    class="reset-btn like"
                    type="button"
                    @click="handleLike(profile.user_id)"
                  >
                    Like
                  </button>
                  <button
                    class="reset-btn pass"
                    type="button"
                    @click="handlePass(profile.user_id)"
                  >
                    Pass
                  </button>
                </div>
              </div>
            </div>

            <p v-if="!loading && profiles.length === 0" class="empty-text">
              No profiles found.
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

.filters {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.filters input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 14px;
}

.fil {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
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

.interests-text {
  color: #374151;
  font-size: 0.95rem;
}

.shared-interest {
  font-weight: 700;
  color: #2563eb;
}

.match-score {
  font-weight: 700;
  color: #f59e0b;
}

.rate-btns {
  display: flex;
  justify-content: center;
  gap: 0.7rem;
  flex-wrap: wrap;
}

.rate-btns .favorite {
  background-color: #7c3aed;
}

.rate-btns .like {
  background-color: var(--primary-color);
}

.rate-btns .pass {
  border-radius: unset;
  border: unset;
  box-shadow: unset;
  color: var(--primary-color);
  background: transparent;
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

  .filters {
    grid-template-columns: 1fr;
  }
}
</style>