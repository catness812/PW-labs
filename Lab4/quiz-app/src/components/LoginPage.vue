<template>
  <div>
    <h1>Login Page</h1>
    <form @submit.prevent="login">
      <label>
        First Name:
        <input type="text" v-model="firstName" required />
      </label>
      <br />
      <label>
        Last Name:
        <input type="text" v-model="lastName" required />
      </label>
      <br />
      <label>
        User ID:
        <input type="text" v-model="userId" required />
      </label>
      <br />
      <button type="submit">Login</button>
    </form>
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
      userId: "",
      users: [],
    };
  },
  methods: {
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
    login() {
      axios
        .get("https://late-glitter-4431.fly.dev/api/v54/users", {
          headers: {
            "X-Access-Token": secret.access,
          },
        })
        .then((response) => {
          const user = response.data.find(
            (user) =>
              user.name === this.firstName &&
              user.surname === this.lastName &&
              user.id === parseInt(this.userId)
          );
          if (user) {
            sessionStorage.setItem("firstName", user.name);
            sessionStorage.setItem("lastName", user.surname);
            sessionStorage.setItem("id", this.userId);
            sessionStorage.setItem("isLogged", true);
            this.$router.push({
              name: "welcome",
              params: {
                id: this.userId,
              },
            });
          } else {
            alert("User not found");
          }
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.updateAccessToken().then((response) => {
              const accessToken = response.data.token;
              axios
                .get("https://late-glitter-4431.fly.dev/api/v54/users", {
                  headers: {
                    "X-Access-Token": accessToken,
                  },
                })
                .then((response) => {
                  const user = response.data.find(
                    (user) =>
                      user.name === this.firstName &&
                      user.surname === this.lastName &&
                      user.id === parseInt(this.userId)
                  );
                  if (user) {
                    sessionStorage.setItem("firstName", user.name);
                    sessionStorage.setItem("lastName", user.surname);
                    sessionStorage.setItem("id", this.userId);
                    sessionStorage.setItem("isLogged", true);
                    this.$router.push({
                      name: "welcome",
                      params: {
                        id: this.userId,
                      },
                    });
                  } else {
                    alert("User not found");
                  }
                })
                .catch((error) => {
                  console.error(error);
                  alert("An error occurred");
                });
            });
          } else {
            console.error(error);
            alert("An error occurred");
          }
        });
    },
  },
};
</script>
