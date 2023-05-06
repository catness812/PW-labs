<template>
  <div>
    <h1>Welcome, {{ firstName }} {{ lastName }}!</h1>
    <h3>Choose a quiz and let the game begin!</h3>
    <div v-if="quizzes.length">
      <div v-for="quiz in quizzes" :key="quiz.id">
        <button @click="goToQuiz(quiz.id)">{{ quiz.title }}</button>
        <p>
          {{ quiz.questions_count }}
          {{ quiz.questions_count === 1 ? "question" : "questions" }}
        </p>
      </div>
    </div>
    <div v-else>
      <p>No quizzes available.</p>
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