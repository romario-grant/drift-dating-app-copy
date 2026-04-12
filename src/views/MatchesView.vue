<script setup>
import { ref, onMounted } from "vue";
import { getMatches } from "../services/api";

const matches = ref([]);
const loading = ref(false);
const errorMessage = ref("");

const formatName = (name) => {
  if (!name) return "Unknown";

  return name
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
};

const loadMatches = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const data = await getMatches();
    matches.value = data;
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadMatches();
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
      <h2>Your Matches</h2>

      <p v-if="errorMessage" class="error-text">
        {{ errorMessage }}
      </p>
      <p v-if="loading" class="loading-text">Loading matches...</p>

      <section class="section-team">
        <div class="wrapper">
          <div class="team">
            <div
              class="profile-card"
              v-for="match in matches"
              :key="match.match_id"
            >
              <figure class="img-box">
                <img src="../assets/pics/default.webp" alt="profile picture" />
              </figure>

              <div class="info">
                <div class="left">
                  <h3>
                    {{ formatName(match.display_name) }}
                    <span v-if="match.age">, {{ match.age }}</span>
                  </h3>

                  <p v-if="match.bio">{{ match.bio }}</p>
                  <p v-if="match.location">{{ match.location }}</p>
                </div>

                <RouterLink
                  :to="`/message/${match.user_id}`"
                  class="reset-btn mess"
                >
                  Message
                </RouterLink>
              </div>
            </div>

            <p v-if="!loading && matches.length === 0" class="empty-text">
              No matches yet.
            </p>
          </div>
        </div>
      </section>
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

.mess {
  width: max-content;
  background-color: var(--primary-color);
  text-decoration: none;
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
