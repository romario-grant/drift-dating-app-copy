<template>
  <header class="main-header" id="nav-bar">
    <div class="wrapper" data-width="wide">
      <!-- Logo (Home) -->
      <RouterLink to="/" class="logo" id="logo-box">
        <img src="@/assets/icons/m-logo.svg" alt="logo" />
      </RouterLink>

      <nav
        class="main-navigation"
        id="nav-container"
        :class="{ active: menuOpen }"
      >

        <ul class="nav-list left" v-if="!$route.meta.hideAuthButtons">
          <li>
            <RouterLink to="/about" class="nav-link"> About </RouterLink>
          </li>
        </ul>


        <ul class="nav-list right" v-if="!$route.meta.hideAuthButtons">
          <li>
            <RouterLink to="/login" class="nav-link log" data-cta-style="line">
              Log In
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/signup" class="nav-link sign">
              Sign Up
            </RouterLink>
          </li>
        </ul>
    
      </nav>

      <!-- Mobile Menu Button -->
      <button @click="toggleMenu" class="mobile-navigation" id="menu-container">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </button>

      <!-- Overlay -->
      <div
        class="black"
        id="black-box"
        @click="toggleMenu"
        v-if="menuOpen"
      ></div>
    </div>
  </header>
</template>

<script>

export default {
  computed: {
    isDashboard() {
      return this.$route.name === "dashboard";
    }
  }
};
</script>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style src="../assets/css/nav.css"></style>
