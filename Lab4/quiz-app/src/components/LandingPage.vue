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
      <p>Press the music button for an experience that's even more magical.</p>
      <button @click.prevent="toggleMusic" id="music-btn">
        <img src="@/assets/landing/music.png" />
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
.landing {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: url("@/assets/landing/background.gif") no-repeat center center
    fixed;
  background-size: cover;
}

.content {
  margin: 50px 17% 0 17%;
  padding: 5vw 6vw 4vw 6vw;
}

.content h1,
.btns {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.content h1 {
  color: #b68439;
  font-size: 7vw;
  text-shadow: -3px 0 #372e29, 0 3px #372e29, 3px 0 #372e29, 0 -3px #372e29;
}

.btns button {
  margin: 20px;
  font-size: 2vw;
  border: none;
  padding: 10px;
  border-radius: 20px;
  color: #392c22;
  background: rgba(255, 255, 255, .35);
  transition: .2s ease-in-out;
  cursor: pointer;
}

.btns button:hover {
  background: rgba(240, 199, 94, .8);
  box-shadow: 0 0 5px rgba(240, 199, 94, .8), 0 0 25px rgba(240, 199, 94, .8),
    0 0 50px rgba(240, 199, 94, .8), 0 0 200px rgba(240, 199, 94, .8);
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
  transition: .3s ease-in-out;
}

.footer #music-btn img {
  width: 25%;
}

.footer #music-btn:hover {
  transform: scale(1.3);
}
</style>