<template>
  <div>
    <h1>Sign Up</h1>
    <form @submit.prevent="createUser">
      <label>
        First Name:
        <input v-model="firstName" type="text" required />
      </label>
      <label>
        Last Name:
        <input v-model="lastName" type="text" required />
      </label>
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="userId">
      Your user ID is: {{ userId }}<br />Please use your ID to
      <button @click="goToLogin">login</button>.
    </p>
  </div>
</template>

<script>
import axios from "axios";
import secret from "./secret.json";

export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      userId: null,
    };
  },
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    async updateAccessToken() {
      try {
        const response = await axios.post(
          "https://late-glitter-4431.fly.dev/api/developers/v72/tokens",
          {},
          {
            headers: {
              "Content-Type": "application/json",
              "X-Developer-Key": secret.key,
              "X-Developer-Secret": secret.secret,
            },
          }
        );
        return response;
      } catch (error) {
        console.error(error);
      }
    },
    async createUser() {
      try {
        const response = await axios.post(
          "https://late-glitter-4431.fly.dev/api/v54/users",
          {
            data: {
              name: this.firstName,
              surname: this.lastName,
            },
          },
          {
            headers: {
              "Content-Type": "application/json",
              "X-Access-Token": secret.access,
            },
          }
        );
        this.userId = response.data.id;
      } catch (error) {
        if (error.response.status === 401) {
          this.updateAccessToken().then((response) => {
            const accessToken = response.data.token;
            axios
              .post(
                "https://late-glitter-4431.fly.dev/api/v54/users",
                {
                  data: {
                    name: this.firstName,
                    surname: this.lastName,
                  },
                },
                {
                  headers: {
                    "Content-Type": "application/json",
                    "X-Access-Token": accessToken,
                  },
                }
              )
              .then((response) => {
                this.userId = response.data.id;
              })
              .catch((error) => {
                console.log(error);
              });
          });
        } else {
          console.error(error);
        }
      }
    },
  },
};
</script>

<style>
</style>
