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
                <h5>Name</h5>
                <img src="../assets/pics/default.webp" />
              </figure>
              <div class="info">
                <div class="left">
                  <div class="person-message">Whats UP?</div>
                  <div class="user-message">HEEYY</div>
                </div>

                <form>
                  <input id="text" type="text" />
                  <button class="reset-btn mess">Send</button>
                </form>
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
  width: max-content;
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
  flex-direction: column;
  width: 100%;
  gap: 2.4rem;
  align-items: center;
  justify-content: space-between;
}

.team .info form {
  display: flex;
  width: 100%;
  gap: 0.6rem;
}

.team .info form input {
    width: 100%;
    padding: 0.4rem;
}

.team .info .left {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
  padding: 0.4rem;
}

.person-message,
.user-message {
  max-width: 60%;
  padding: 10px 14px;
  border-radius: 15px;
  font-size: 14px;
}

.person-message {
  align-self: flex-start;
  background-color: #e5e5ea;
  color: #000;
  border-bottom-left-radius: 0;
}

.user-message {
  align-self: flex-end;
  background-color: #007bff;
  color: #fff;
  border-bottom-right-radius: 0;
}

.team .img-box {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: max-content;
  text-align: left;
  border-right: 3px solid grey;
  padding: 0.8rem;
}

.team .img-box img {
  width: 100%;
}

.team .lockup {
  display: flex;
  flex-direction: row;
  align-items: center;
  border: 3px solid grey;
  border-radius: 0.6rem;
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
