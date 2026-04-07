<template>
  <footer id="footer">
    <div class="footer-cnt">
      <div class="top">
        <div class="wrapper top-cnt">
          <div class="company-info">
            <a href="index.html"
              ><img src="@/assets/icons/m-logo.svg" alt="logo"
            /></a>
            <p>
              Help people connect without pressure, without pretending, and
              without the noise.
            </p>
          </div>
        </div>
      </div>

      <div class="btm">
        <p>&copy;2026 Drift Dating all rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from "vue";

const year = new Date().getFullYear();
</script>

<style src="../assets/css/footer.css"></style>
