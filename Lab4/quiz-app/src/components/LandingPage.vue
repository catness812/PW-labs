<template>
  <div class="landing">
    <div class="content">
      <h1>Welcome to the Wizarding World!</h1>
      <div class="btns">
        <button @click="goToSignUp">Sign Up</button>
        <button @click="goToLogin">Log In</button>
      </div>
    </div>
    <div class="footer">
      <p>Press the music button for an experience even more magical.</p>
      <button @click.prevent="toggleMusic" id="music-btn">
        <img src="@/assets/music.png" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      audio: null,
    };
  },
  mounted() {
    if (window.audio) {
      this.audio = window.audio;
      this.isMusicPlaying = !this.audio.paused;
    } else {
      this.audio = new Audio(require("@/assets/harrypotter.mp3"));
      this.audio.loop = true;
      this.isMusicPlaying = true;
      window.audio = this.audio;
    }
  },
  methods: {
    goToSignUp() {
      this.$router.push("/signup");
    },
    goToLogin() {
      this.$router.push("/login");
    },
    toggleMusic() {
      if (this.audio.paused) {
        this.audio.play();
        this.isMusicPlaying = true;
      } else {
        this.audio.pause();
        this.isMusicPlaying = false;
      }
    },
  },
};
</script>

<style scoped>
@font-face {
  font-family: "HarryPotter";
  src: url("@/assets/harry_potter/harryp-webfont.woff2") format("woff2"),
    url("@/assets/harry_potter/harryp-webfont.woff2") format("woff");
}

* {
  font-family: "HarryPotter", Arial, sans-serif;
}

.landing {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: url("@/assets/background.gif") no-repeat center center fixed;
  background-size: cover;
}

.content {
  margin: 50px 17% 0 17%;
  padding: 5vw 6vw 4vw 6vw;
  color: #d9d9d9;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 50px;
}

.content h1,
.btns {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.content h1 {
  font-size: 7vw;
}

.btns button {
  margin: 20px;
  font-size: 2vw;
  border: none;
  padding: 10px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.5);
  transition: 0.2s ease-in-out;
  border: 2px solid transparent;
  cursor: pointer;
}

.btns button:hover {
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid #d3d1d1;
  color: #d3d1d1;
}

.footer {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.footer p {
  color: #fff;
  font-size: 24px;
}

.footer #music-btn {
  background: none;
  border: none;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.footer #music-btn img {
  width: 25%;
}

.footer #music-btn:hover {
  transform: scale(1.3);
}
</style>
