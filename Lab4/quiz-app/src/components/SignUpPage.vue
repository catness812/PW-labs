<template>
  <div class="sign-up">
    <div class="content">
      <h1>Sign Up</h1>
      <form @submit.prevent="createUser">
        <input
          v-model="firstName"
          type="text"
          placeholder="First Name"
          required
        />
        <input
          v-model="lastName"
          type="text"
          placeholder="Last Name"
          required
        />
        <button type="submit">
          <img src="@/assets/signup-login/submit.png" />
        </button>
      </form>
      <p v-if="userId">
        Your user ID is <span id="user-id">{{ userId }}</span>
        <span>
          Please use your ID to <button @click="goToLogin">login</button>
        </span>
      </p>
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
        } else if (error.response.status === 400) {
          alert(error.response.data.message[0]);
        } else {
          console.error(error);
        }
      }
    },
  },
};
</script>

<style scoped>
.sign-up {
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
.content form,
.content p {
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

.content p {
  font-size: 2vw;
  color: rgba(255, 255, 255, .6);
  flex-direction: column;
}

.content #user-id {
  text-shadow: -1px 0 #372e29, 0 1px #372e29, 1px 0 #372e29, 0 -1px #372e29;
  padding: 5px;
  border-radius: 5px;
  background: rgba(255, 255, 255, .3);
  margin: 5px 0 15px 0;
}

.content p button {
  border: none;
  padding: 5px;
  font-size: 2vw;
  border-radius: 10px;
  color: rgba(255, 255, 255, .6);
  background: rgba(255, 255, 255, .3);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.content p button:hover {
  color: rgba(255, 255, 255, .9);
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}
</style>