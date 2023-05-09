<template>
  <div class="login">
    <div class="content">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input
          type="text"
          v-model="firstName"
          placeholder="First Name"
          required
        />
        <input
          type="text"
          v-model="lastName"
          placeholder="Last Name"
          required
        />
        <input type="text" v-model="userId" placeholder="User ID" required />
        <button type="submit">
          <img src="@/assets/signup-login/submit.png" />
        </button>
      </form>
    </div>
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
          const userIdRegex = /^[0-9]+$/;
          const isValidUserId = userIdRegex.test(this.userId);
          if (!isValidUserId) {
            alert("User ID must be a numeric value");
            return;
          }
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

<style scoped>
.login {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: url("@/assets/signup-login/background.png") no-repeat center
    center fixed;
  background-size: cover;
}

.content {
  margin: 10% 35% 0 35%;
  padding: 15px 0 20px 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, .2), transparent);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0px 0px 20px 5px rgba(0, 0, 0, .3);
}

.content h1,
.content form {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content form {
  display: flex;
  flex-direction: column;
}

.content form button {
  margin: 30px 0 15px 0;
  border: none;
  padding: 10px 9px 6px 9px;
  border-radius: 20px;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.content form button:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}

.content img {
  width: 30px;
  height: 30px;
  opacity: .7;
}

.content h1 {
  color: rgba(255, 255, 255, .6);
  font-size: 5.5vw;
  text-shadow: -3px 0 #372e29, 0 3px #372e29, 3px 0 #372e29, 0 -3px #372e29;
  margin-bottom: 60px;
}

.content input {
  width: 20vw;
  height: 5vh;
  font-size: 2vw;
  background: none;
  border: 2px solid rgba(255, 255, 255, .5);
  border-radius: 15px;
  text-indent: 8px;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, .8);
}

.content input::placeholder {
  text-align: center;
  color: rgba(0, 0, 0, .8);
}
</style>