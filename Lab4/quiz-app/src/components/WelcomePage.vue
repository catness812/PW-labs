<template>
  <div class="welcome">
    <div class="content">
      <button @click="logOut" id="logout">Log Out</button>
      <h1 id="header">Hi, {{ firstName }} {{ lastName }}!</h1>
      <div class="container">
        <div v-if="quizzes.length" class="quizzes">
          <div v-for="quiz in quizzes" :key="quiz.id" class="quiz">
            <button @click="goToQuiz(quiz.id)" class="quiz-card">
              <img src="@/assets/welcome/symbol.png" />
              <h2>{{ quiz.title }}</h2>
              <h4>
                {{ quiz.questions_count }}
                {{ quiz.questions_count === 1 ? "question" : "questions" }}
              </h4>
            </button>
          </div>
        </div>
        <div v-else id="empty">
          <p>No quizzes available.</p>
        </div>
      </div>
      <div id="pusheen">
        <h3 id="bubble">
          Ready to embark on an adventure? Hover over any symbol and let the fun begin!
        </h3>
        <img src="@/assets/welcome/pusheen.png" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import secret from "./secret.json";

export default {
  data() {
    return {
      quizzes: [],
      firstName: sessionStorage.getItem("firstName"),
      lastName: sessionStorage.getItem("lastName"),
    };
  },
  methods: {
    logOut() {
      this.$router.push("/");
      sessionStorage.clear();
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
    goToQuiz(id) {
      this.$router.push({
        name: "quiz",
        params: {
          id: id,
        },
      });
    },
  },
  mounted() {
    axios
      .get("https://late-glitter-4431.fly.dev/api/v54/quizzes", {
        headers: {
          "X-Access-Token": secret.access,
        },
      })
      .then((response) => {
        this.quizzes = response.data;
      })
      .catch((error) => {
        if (error.response.status === 401) {
          this.updateAccessToken().then((response) => {
            const accessToken = response.data.token;
            axios
              .get("https://late-glitter-4431.fly.dev/api/v54/quizzes", {
                headers: {
                  "X-Access-Token": accessToken,
                },
              })
              .then((response) => {
                this.quizzes = response.data;
              })
              .catch((error) => {
                console.log(error);
              });
          });
        } else {
          console.log(error);
        }
      });
  },
};
</script>

<style scoped>
.welcome {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: url("@/assets/welcome/background.png") no-repeat center center
    fixed;
  background-size: cover;
}

.content #logout {
  position: absolute;
  top: 28px;
  right: 30px;
  font-size: 20px;
  border: none;
  padding: 10px 9px 6px 9px;
  border-radius: 20px;
  color: #372e29;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.content #logout:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}

.content #pusheen {
  position: absolute;
  bottom: -15px;
}

.content #pusheen img {
  width: 300px;
  filter: brightness(70%);
  animation: float 2.5s linear infinite;
}

.content #pusheen #bubble {
  position: absolute;
  bottom: 100px;
  left: 120px;
  margin: 100px 0 0 200px;
  font-size: 1.4vw;
  letter-spacing: 1px;
  color: #372e29;
  width: 220px;
  background: rgba(255, 255, 255, .5);
  padding: 10px;
  border-radius: 15px;
  text-align: justify;
  text-align-last: center;
}

.content #pusheen #bubble:before {
  position: absolute;
  content: "";
  display: block;
  left: -4.1%;
  top: 17px;
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 10px solid rgba(255, 255, 255, .5);
  border-left: 10px solid rgba(255, 255, 255, .5);
  transform: rotate(45deg);
}

@keyframes float {
  from {
    transform: scaleX(-1) rotate(0deg) translateY(-12px) rotate(0deg);
  }
  to {
    transform: scaleX(-1) rotate(-360deg) translateY(-12px) rotate(360deg);
  }
}

.content #header {
  width: 100%;
  margin: 10px 0 40px 0;
  background: rgba(55, 46, 41, .3);
  padding: 20px 30px 20px 40px;
  color: rgba(255, 255, 255, .7);
  font-size: 34px;
  letter-spacing: 2px;
}

.content .container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.content .container .quizzes {
  display: flex;
  width: 70%;
  height: 57vh;
  overflow: scroll;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-evenly;
  border: 2px solid rgba(114, 98, 85, .4);
  border-radius: 30px;
  box-shadow: 0px 0px 20px 5px rgba(255, 255, 255, .1);
}

.content .container .quizzes .quiz {
  margin: 20px;
}

.quizzes .quiz .quiz-card {
  position: relative;
  cursor: pointer;
  padding: 40px;
  box-shadow: 5px 5px 30px rgba(154, 132, 114, .9);
  background: rgba(114, 98, 85, .5);
  border: none;
  border-radius: 20px;
  border-top: 1px solid rgba(154, 132, 114, .9);
  border-left: 1px solid rgba(154, 132, 114, .9);
  backdrop-filter: blur(5px);
  overflow: hidden;
  transition: .5s ease-in-out;
}

.quizzes .quiz .quiz-card img {
  max-width: 70%;
  position: absolute;
  opacity: .3;
  transition: .5s ease-in-out;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.quizzes .quiz .quiz-card h2,
.quizzes .quiz .quiz-card h4 {
  transform: translateY(100px);
  transition: .5s ease-in-out;
  opacity: 0;
  overflow-wrap: break-word;
  hyphens: auto;
}

.quizzes .quiz .quiz-card:hover {
  background: rgba(240, 199, 94, .6);
  box-shadow: 5px 5px 30px rgba(240, 199, 94, .7);
  border-top: 1px solid rgba(236, 185, 57, .3);
  border-left: 1px solid rgba(236, 185, 57, .3);
}

.quizzes .quiz .quiz-card:hover h2,
.quizzes .quiz .quiz-card:hover h4 {
  transform: translateY(0px);
  opacity: 1;
}

.quizzes .quiz .quiz-card:hover img {
  opacity: 0;
}

.quizzes .quiz .quiz-card h2 {
  color: rgba(255, 255, 255, .8);
  font-size: 1.5vw;
}

.quizzes .quiz .quiz-card h4 {
  color: #dbcba9;
  font-size: 1.2vw;
}

#empty {
  color: #fff;
  font-size: 3.3vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>