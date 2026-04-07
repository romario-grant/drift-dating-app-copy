<script setup>
import { ref } from "vue";
</script>

<template>
  <main class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <nav>
        <RouterLink to="/dashboard"> Browse </RouterLink>
        <RouterLink to="/message"> Message </RouterLink>
        <RouterLink to="/matches"> Matches </RouterLink>
      </nav>
    </aside>

    <div class="dash">
      <section class="section-team">
        <div class="wrapper">
          <div class="team">
            <div class="lockup" v-for="n in 12" :key="n">
              <figure class="img-box">
                <img src="../assets/pics/default.webp" />
              </figure>
              <div class="info">
                <div class="left">
                  <h3>Person Name</h3>
                  <p>person description and role</p>
                  <p class="txt-p-clr">Match Score</p>
                </div>

                <button class="reset-btn mess">Message</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: 0.5fr 4fr;
}

.dash {
  padding: 2.4rem;
}

.sidebar {
  padding: 2rem;
  background: rgba(0, 102, 255, 0.15);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.logo {
  margin-bottom: 2rem;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar a {
  text-decoration: none;
  color: #222;
}

h2 {
  margin-bottom: 15px;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.filters input,
.filters select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.filters select {
  max-width: 150px;
}

.fil {
  display: flex;
}

.mess {
    width: 20%;
  background-color: var(--primary-color);
}


@media (max-width: 600px) {
  .filters {
    flex-direction: column;
  }

  .filters select {
    max-width: 100%;
  }
}

.team {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.team .info {
  display: flex;
  width: 100%;
  gap: 2.4rem;
  align-items: center;
  justify-content: space-between;
}

.team .info .left {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.team .img-box {
  display: flex;
  justify-content: center;
  background-color: var(--primary-color);
  border-radius: 15px;
  width: max-content;
}

.team .img-box img {
  width: 100%;
}

.team .lockup {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.team .lockup p {
  font-size: clamp(var(--fs-0), 5vw, var(--fs-1));
}

@media (width > 1028px) {
  .mess:hover {
    transform: translateY(-5px);
    background-color: black;
  }
}

.mess:active {
  transform: translateY(5px);
}
</style>
