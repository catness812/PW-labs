<template>
  <div class="quiz-page">
    <button @click="goBack" id="back">
      <img src="@/assets/quiz/back.png" />
    </button>
    <h1>{{ quizTitle }}</h1>
    <div class="content">
      <div id="quiz-played-message">
        <p>You have already completed this quiz!</p>
        <p>
          Your score is
          <span id="score">{{ score }}/{{ questions.length }}</span>
        </p>
        <p>
          Total time:
          <span id="time"
            >{{ Math.floor(time / 60) }}:{{ time % 60 < 10 ? "0" : ""
            }}{{ time % 60 }}</span
          >
        </p>
      </div>
      <div id="quiz-start" v-if="!started">
        <button @click="startQuiz" id="start-btn">Start Quiz</button>
      </div>
      <div v-else id="questions">
        <div v-if="currentQuestion !== null">
          <h3>{{ currentQuestionNumber }} / {{ questions.length }}</h3>
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
          <span class="elapsed"
            ><p>
              Elapsed time: {{ Math.floor(timer / 60) }}:{{
                timer % 60 < 10 ? "0" : ""
              }}{{ timer % 60 }}
            </p></span
          >
          <div v-if="answerSubmitted" id="feedback">
            <p v-if="answerSubmitted === 'correct'">Correct!</p>
            <p v-else>Oh no, that's wrong!</p>
            <button @click="nextQuestion">Next</button>
          </div>
        </div>
        <div v-else id="finish">
          <p>
            Your score is
            <span id="score">{{ score }}/{{ questions.length }}</span>
          </p>
          <p v-if="score / questions.length <= 0.4">
            Uh oh... you better start revising!
            <br />
            <img src="@/assets/quiz/snape.gif" />
          </p>
          <p v-else-if="score / questions.length <= 0.7">
            Well done, but could've been better!
            <br />
            <img src="@/assets/quiz/hermione.gif" />
          </p>
          <p v-else-if="score / questions.length > 0.7">
            Great job! You're a prodigy!
            <br />
            <img src="@/assets/quiz/brilliant.gif" />
          </p>
        </div>
      </div>
    </div>
    <svg>
      <filter id="wavy">
        <feTurbulence
          x="0"
          y="0"
          id="turbulence"
          baseFrequency="0.01"
          numOctaves="5"
          seed="2"
        ></feTurbulence>
        <feDisplacementMap in="SourceGraphic" scale="30" />
      </filter>
    </svg>
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
  computed: {
    currentQuestionNumber() {
      if (this.currentQuestion !== null) {
        return this.questions.indexOf(this.currentQuestion) + 1;
      } else {
        return 0;
      }
    },
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

<style scoped>
.quiz-page {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #0a0703;
}

.quiz-page .content {
  position: absolute;
  top: 53%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  height: 80%;
  background: url("@/assets/quiz/background.jpeg") no-repeat center center fixed;
  background-size: cover;
  border-radius: 20px;
  box-shadow: 0 0 5px #35201c, 0 0 25px #35201c, 0 0 50px #35201c,
    0 0 200px #35201c;
}

.quiz-page #back {
  position: absolute;
  border: none;
  margin: 20px 0 0 30px;
  padding: 10px 9px 6px 9px;
  border-radius: 20px;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.quiz-page #back img {
  width: 24px;
}

.quiz-page #back:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}

.quiz-page h1 {
  margin-top: 25px;
  text-align: center;
  color: rgba(255, 255, 255, .7);
  font-size: 3.5vw;
  text-shadow: -3px 0 #35201c, 0 3px #35201c, 3px 0 #35201c, 0 -3px #35201c;
}

.quiz-page #quiz-played-message {
  position: relative;
  top: 45%;
  left: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transform: translate(-50%, -50%);
  width: fit-content;
  padding: 40px;
  border-radius: 200px;
}

#finish {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: fit-content;
  padding: 40px;
  border-radius: 200px;
}

.quiz-page #quiz-played-message:before {
  position: absolute;
  z-index: -1;
  border-radius: 200px;
  content: "";
  display: block;
  width: 110%;
  height: 110%;
  left: -30px;
  top: -40px;
  background: rgba(228, 189, 111, .3);
  border: 10px solid rgba(159, 126, 77, .8);
  filter: url(#wavy);
  box-shadow: 0 0 2px rgba(240, 199, 94, .5), 0 0 25px rgba(240, 199, 94, 1),
    0 0 10px rgba(240, 199, 94, .8), 0 0 100px rgba(240, 199, 94, .5);
}

.quiz-page #quiz-played-message p {
  color: #fff;
  font-size: 2.2vw;
}

#score,
.quiz-page #quiz-played-message #time,
#questions h3 {
  color: #35201c;
  background: rgba(255, 255, 255, .4);
  padding: 5px;
  border-radius: 10px;
  width: fit-content;
}

#questions h3 {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

.quiz-page #quiz-start button {
  margin: 20% 0 0 50%;
  transform: translateX(-50%);
  font-size: 48px;
  border: none;
  padding: 10px 9px 6px 9px;
  border-radius: 20px;
  color: #372e29;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.quiz-page #quiz-start button:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}

.quiz-page #questions {
  position: relative;
  color: #fff;
  font-size: 2vw;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: fit-content;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%);
}

#questions h2 {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  max-width: 70%;
}

#questions ul {
  position: relative;
  padding-left: 0;
  max-width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  flex-wrap: wrap;
  left: 50%;
  transform: translateX(-50%);
}

#questions li {
  position: relative;
  list-style: none;
  font-size: 1.7vw;
  margin: 50px 20px 50px 20px;
  padding: 10px 20px 10px 20px;
  transition: .2s ease-in-out;
  width: fit-content;
  text-align: center;
}

#questions li:before {
  position: absolute;
  z-index: -1;
  border-radius: 200px;
  content: "";
  display: block;
  width: 110%;
  height: 110%;
  left: -30px;
  top: -15px;
  background: rgba(228, 189, 111, .3);
  border: 10px solid rgba(159, 126, 77, .8);
  filter: url(#wavy);
  box-shadow: 0 0 2px rgba(240, 199, 94, .5), 0 0 25px rgba(240, 199, 94, 1),
    0 0 10px rgba(240, 199, 94, .8), 0 0 100px rgba(240, 199, 94, .5);
}

#questions li:hover {
  transform: scale(1.1);
}

#feedback {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
}

#feedback p,
#feedback button {
  margin: 0 20px 0 20px;
}

#feedback button {
  font-size: 24px;
  border: none;
  padding: 10px 9px 6px 9px;
  border-radius: 20px;
  color: #372e29;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

#feedback button:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
}

.elapsed {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
</style>