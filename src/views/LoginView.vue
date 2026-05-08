<template>
  <div class="form-container">
    <h2>Login</h2>

    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">Login</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;

      try {
        const res = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          this.error = data.error || "Login failed";
          return;
        }

        this.$router.push("/dashboard");
      } catch (err) {
        this.error = "Server error. Try again.";
        console.error(err);
      }
    },
  },
};
</script>

<style scoped src="../assets/css/form.css"></style>
