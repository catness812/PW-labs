<template>
  <div>
    <h1>Welcome to My App</h1>
    <button @click="goToSignUp">Sign Up</button>
    <button @click="goToLogin">Log In</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToSignUp() {
      this.$router.push("/signup");
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>
