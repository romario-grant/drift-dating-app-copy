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
      <div class="container">
        <h2>Browse Potential Matches</h2>

        <div class="filters">
          <input type="text" placeholder="Search by name or bio..." />
          <select>
            <option>All Ages</option>
            <option>18-25</option>
            <option>26-35</option>
            <option>36-50</option>
          </select>
          <input type="text" placeholder="Filter by location..." />
        </div>
        <div class="fil">
          <button class="cta">Show Interest Filters</button>
          <button class="cta" data-cta-style="line">Reset Filters</button>
        </div>
      </div>

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

                <div class="rate-btns">
                  <button class="reset-btn like">Like</button>
                  <button class="reset-btn pass">Pass</button>
                </div>
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
  background: var(--secondary-color);
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
  color: #ffffff;
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

.rate-btns {
  display: flex;
  flex-direction: row;
  gap: 1.6rem;
}

.rate-btns .like {
  background-color: var(--primary-color);
}

.rate-btns .pass {
  border-radius: unset;
  border: unset;
  box-shadow: unset;
  color: var(--primary-color);
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
  .rate-btns button:hover {
    transform: translateY(-5px);
  }
  .rate-btns .like:hover {
    background-color: black;
  }

  .rate-btns .pass:hover {
    color: black;
    text-decoration: underline;
  }
}

.rate-btns button:active {
  transform: translateY(5px);
}
</style>
