<template>
  <div>
    <button @click="goBack">Back</button>
    <h1>{{ quizTitle }}</h1>
    <div id="quiz-played-message">
      <p>You have already completed this quiz!</p>
      <p>Your score is {{ score }}/{{ questions.length }}.</p>
      <p>
        Total time: {{ Math.floor(time / 60) }}:{{ time % 60 < 10 ? "0" : ""
        }}{{ time % 60 }}
      </p>
    </div>
    <div id="quiz-start" v-if="!started">
      <button @click="startQuiz" id="start-btn">Start Quiz</button>
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
        <p>Congrats! You have completed the quiz!</p>
        <p>Your score is {{ score }}/{{ questions.length }}.</p>
      </div>
      <p>
        Elapsed time: {{ Math.floor(timer / 60) }}:{{
          timer % 60 < 10 ? "0" : ""
        }}{{ timer % 60 }}
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
      quizId: this.$route.params.id,
      quizTitle: "",
      questions: [],
      started: false,
      currentQuestion: null,
      answerSubmitted: null,
      score: "loading",
      timer: 0,
      timerInterval: null,
      time: 0,
      accessToken: secret.access,
    };
  },
  methods: {
    goBack() {
      const userId = sessionStorage.getItem("id");
      this.$router.push({
        name: "welcome",
        params: {
          id: userId,
        },
      });
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
        return response.data.token;
      } catch (error) {
        console.error(error);
      }
    },
    startQuiz() {
      this.started = true;
      const userId = sessionStorage.getItem("id");
      const timerKey = `timer-${this.quizId}-${userId}`;
      if (localStorage.getItem(timerKey) !== null) {
        this.timer = parseInt(localStorage.getItem(timerKey));
      } else {
        this.timer = 0;
        localStorage.setItem(timerKey, this.timer);
      }
      this.timerInterval = setInterval(() => {
        this.timer++;
        localStorage.setItem(
          `timer-${this.quizId}-${sessionStorage.getItem("id")}`,
          this.timer
        );
      }, 1000);
      const unansweredQuestion = this.questions.find(
        (question) => question.submitted_answer === null
      );
      if (unansweredQuestion) {
        this.currentQuestion = unansweredQuestion;
      } else {
        this.currentQuestion = this.questions[0];
      }
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
        clearInterval(this.timerInterval);
        this.getScore().then((score) => {
          this.score = score;
        });
      }
    },
    async getScore() {
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
        this.questions = quizData.questions;
        const correctAnswers = quizData.questions.reduce((count, question) => {
          return question.answered_correctly ? count + 1 : count;
        }, 0);
        return correctAnswers;
      } catch (error) {
        if (error.response.status === 401) {
          this.accessToken = await this.updateAccessToken();
          return await this.getScore();
        } else {
          console.error(error);
          return 0;
        }
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
        const unansweredQuestions = quizData.questions.filter(
          (question) => question.submitted_answer === null
        );
        const quizStart = document.getElementById("quiz-start");
        const quizPlayedMessage = document.getElementById(
          "quiz-played-message"
        );
        if (unansweredQuestions.length === this.questions.length) {
          quizStart.style.display = "block";
          quizPlayedMessage.style.display = "none";
        } else if (unansweredQuestions.length > 0) {
          const startBtn = document.getElementById("start-btn");
          startBtn.textContent = "Resume Quiz";
          quizStart.style.display = "block";
          quizPlayedMessage.style.display = "none";
        } else {
          quizStart.style.display = "none";
          clearInterval(this.timerInterval);
          this.getScore().then((score) => {
            this.score = score;
          });
          const timerKey = `timer-${this.quizId}-${userId}`;
          this.time = localStorage.getItem(timerKey);
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
