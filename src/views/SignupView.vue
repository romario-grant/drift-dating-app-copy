<script setup>
import { ref } from "vue";
</script>

<template>
  <section class="section-authentication">
    <div class="authentication">
      <div class="company">
        <div class="wrapper">
          <div class="lockup">
           <h1>No pressure. No games. Just real connections.</h1>
            <p>
              By logging in to Drift Dating, you agree to our Terms of use and
              Privacy Policy.
            </p>
          </div>
        </div>
      </div>
      <div class="form">
        <div class="wrapper">
          <div class="box">
            <h2>Sign Up</h2>

            <div class="inputs">
              <p>
                <span style="color: red">*</span>Indicates a required field.
              </p>
              <div class="field">
                <label>Phone Number <span style="color: red">*</span></label>
                <input id="telephone" type="text" />
              </div>
              <div class="field">
                <label>Email <span style="color: red">*</span></label>
                <input id="email" type="email" />
              </div>

              <div class="field">
                <label>Password <span style="color: red">*</span></label>
                <input id="password" type="password" />
              </div>
            </div>

            <div class="buttons">
              <a id="signupBtn" class="cta">Sign Up</a>
            </div>

            <p class="sub-text">
              <RouterLink to="/login" class="account">
                Already have an account?
              </RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped src="../assets/css/form.css"></style>
