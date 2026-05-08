<template>
  <div class="form-container">
    <h2>Sign Up</h2>

    <form @submit.prevent="handleSignup">
      <input v-model="email" type="email" placeholder="Email" required />
      <input
        v-model="phone_number"
        type="text"
        placeholder="Phone Number"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">Sign Up</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      phone_number: "",
      password: "",
      error: null,
      success: null,
    };
  },
  methods: {
    async handleSignup() {
      this.error = null;
      this.success = null;

      try {
        const res = await fetch("http://localhost:5000/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            email: this.email,
            phone_number: this.phone_number,
            password: this.password,
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          this.error = data.error || "Signup failed";
          return;
        }

        this.success = "Account created successfully!";

        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);
      } catch (err) {
        this.error = "Server error. Try again.";
        console.error(err);
      }
    },
  },
};
</script>

<style scoped src="../assets/css/form.css"></style>
