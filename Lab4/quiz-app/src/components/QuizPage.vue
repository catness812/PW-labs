<template>
  <div>
    <h1>{{ quizTitle }}</h1>
    <p id="quiz-played-message"></p>
    <div id="quiz-start" v-if="!started">
      <button @click="startQuiz">Start Quiz</button>
    </div>
    <div v-else>
      <div v-if="currentQuestion !== null">
        <h2>{{ currentQuestion.question }}</h2>
        <ul>
          <li
            v-for="(answer, index) in currentQuestion.answers"
            :key="index"
            @click="submitAnswer(answer)"
          >
            {{ answer }}
          </li>
        </ul>
        <div v-if="answerSubmitted">
          <p v-if="answerSubmitted === 'correct'">Correct!</p>
          <p v-else>Incorrect!</p>
          <button @click="nextQuestion">Next</button>
        </div>
      </div>
      <div v-else>
        <p>You have completed the quiz!</p>
        <p>Your score is {{ score }}/{{ questions.length }}.</p>
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
      quizId: this.$route.params.id,
      quizTitle: "",
      questions: [],
      started: false,
      currentQuestion: null,
      answerSubmitted: null,
      score: 0,
      accessToken: secret.access,
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
        return response.data.token;
      } catch (error) {
        console.error(error);
      }
    },
    startQuiz() {
      this.started = true;
      this.currentQuestion = this.questions[0];
      window.addEventListener("beforeunload", this.showWarning);
    },
    showWarning(event) {
      event.preventDefault();
    },
    async submitAnswer(answer) {
      if (this.answerSubmitted !== null) {
        return;
      }
      const questionId = this.currentQuestion.id;
      const userId = sessionStorage.getItem("id");
      const requestBody = {
        data: {
          question_id: questionId,
          answer,
          user_id: userId,
        },
      };
      try {
        const response = await axios.post(
          `https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quizId}/submit`,
          requestBody,
          {
            headers: {
              "X-Access-Token": this.accessToken,
              "Content-Type": "application/json",
            },
          }
        );
        const isCorrect = response.data.correct;
        this.answerSubmitted = isCorrect ? "correct" : "incorrect";
        if (isCorrect) {
          this.score++;
        }
      } catch (error) {
        if (error.response.status === 401) {
          this.accessToken = await this.updateAccessToken();
          this.submitAnswer(answer);
        } else {
          console.error(error);
        }
      }
    },
    nextQuestion() {
      const currentQuestionIndex = this.questions.indexOf(this.currentQuestion);
      if (currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestion = this.questions[currentQuestionIndex + 1];
        this.answerSubmitted = null;
      } else {
        this.currentQuestion = null;
      }
    },
    async checkIfQuizPlayed() {
      const userId = sessionStorage.getItem("id");
      try {
        const response = await axios.get(
          `https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quizId}`,
          {
            headers: {
              "X-Access-Token": this.accessToken,
            },
            params: {
              user_id: userId,
            },
          }
        );
        const quizData = response.data;
        this.quizTitle = quizData.title;
        this.questions = quizData.questions;
        const answeredQuestions = quizData.questions.filter(
          (question) => question.submitted_answer !== null
        );
        if (answeredQuestions.length > 0) {
          const quizStart = document.getElementById("quiz-start");
          const quizPlayedMessage = document.getElementById(
            "quiz-played-message"
          );
          quizPlayedMessage.textContent = "This quiz has already been played.";
          quizStart.style.display = "none";
        }
      } catch (error) {
        if (error.response.status === 401) {
          this.accessToken = await this.updateAccessToken();
          this.checkIfQuizPlayed();
        } else {
          console.error(error);
        }
      }
    },
  },
  mounted() {
    this.checkIfQuizPlayed();
    const userId = sessionStorage.getItem("id");
    axios
      .get(`https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quizId}`, {
        headers: {
          "X-Access-Token": secret.access,
        },
        params: {
          user_id: userId,
        },
      })
      .then((response) => {
        this.quizTitle = response.data.title;
        this.questions = response.data.questions;
      })
      .catch((error) => {
        if (error.response.status === 401) {
          this.updateAccessToken().then((response) => {
            const accessToken = response.data.token;
            axios
              .get(
                `https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quizId}`,
                {
                  headers: {
                    "X-Access-Token": accessToken,
                  },
                  params: {
                    user_id: userId,
                  },
                }
              )
              .then((response) => {
                this.quizTitle = response.data.title;
                this.questions = response.data.questions;
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
